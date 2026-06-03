import colorsys
import re
from typing import Dict, List, Optional, Tuple

import streamlit as st


HEX_PATTERN = re.compile(r"^#?[0-9a-fA-F]{6}$")
AA_NORMAL = 4.5
AA_LARGE = 3.0
AAA_NORMAL = 7.0


def normalize_hex(value: str) -> Optional[str]:
    """Validate a 6-digit HEX color and return it in #RRGGBB format."""
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not HEX_PATTERN.fullmatch(cleaned):
        return None
    if not cleaned.startswith("#"):
        cleaned = f"#{cleaned}"
    return cleaned.upper()


def is_valid_hex(value: str) -> bool:
    """Check whether a string is a valid 6-digit HEX color."""
    return normalize_hex(value) is not None


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert #RRGGBB HEX to an RGB tuple."""
    normalized = normalize_hex(hex_color)
    if normalized is None:
        raise ValueError(f"Invalid HEX color: {hex_color}")
    return (
        int(normalized[1:3], 16),
        int(normalized[3:5], 16),
        int(normalized[5:7], 16),
    )


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert an RGB tuple to #RRGGBB HEX."""
    r, g, b = [max(0, min(255, int(round(channel)))) for channel in rgb]
    return f"#{r:02X}{g:02X}{b:02X}"


def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calculate WCAG relative luminance for an RGB color."""
    linear_channels = []
    for channel in rgb:
        value = channel / 255
        if value <= 0.03928:
            linear_channels.append(value / 12.92)
        else:
            linear_channels.append(((value + 0.055) / 1.055) ** 2.4)
    r, g, b = linear_channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(foreground_hex: str, background_hex: str) -> float:
    """Calculate WCAG contrast ratio between foreground and background colors."""
    fg_luminance = relative_luminance(hex_to_rgb(foreground_hex))
    bg_luminance = relative_luminance(hex_to_rgb(background_hex))
    lighter = max(fg_luminance, bg_luminance)
    darker = min(fg_luminance, bg_luminance)
    return (lighter + 0.05) / (darker + 0.05)


def rgb_to_hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    """Convert RGB to HSL as hue degrees, saturation, and lightness."""
    r, g, b = [channel / 255 for channel in rgb]
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    return hue * 360, saturation, lightness


def hex_to_hsl(hex_color: str) -> Tuple[float, float, float]:
    """Convert HEX to HSL as hue degrees, saturation, and lightness."""
    return rgb_to_hsl(hex_to_rgb(hex_color))


def hsl_to_rgb(hue: float, saturation: float, lightness: float) -> Tuple[int, int, int]:
    """Convert HSL values to an RGB tuple."""
    hue = (hue % 360) / 360
    lightness = max(0.0, min(1.0, lightness))
    saturation = max(0.0, min(1.0, saturation))
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return round(r * 255), round(g * 255), round(b * 255)


def hsl_to_hex(hue: float, saturation: float, lightness: float) -> str:
    """Convert HSL values to #RRGGBB HEX."""
    return rgb_to_hex(hsl_to_rgb(hue, saturation, lightness))


def find_related_color_for_target(
    original_hex: str,
    background_hex: str,
    target_ratio: float,
    step: float = 0.001,
) -> Optional[Dict[str, object]]:
    """Keep hue/saturation and adjust lightness to find the closest passing color."""
    hue, saturation, original_lightness = hex_to_hsl(original_hex)
    best_match = None
    steps = int(1 / step)

    for index in range(steps + 1):
        lightness = index * step
        candidate_hex = hsl_to_hex(hue, saturation, lightness)
        ratio = contrast_ratio(candidate_hex, background_hex)
        if ratio >= target_ratio:
            lightness_change = abs(lightness - original_lightness)
            if best_match is None or lightness_change < best_match["lightness_change"]:
                best_match = {
                    "hex": candidate_hex,
                    "ratio": ratio,
                    "lightness_change": lightness_change,
                    "target_met": True,
                }

    return best_match


def find_best_related_contrast(
    original_hex: str,
    background_hex: str,
    step: float = 0.001,
) -> Dict[str, object]:
    """Find the strongest contrast available while preserving hue/saturation."""
    hue, saturation, original_lightness = hex_to_hsl(original_hex)
    best_match = None
    steps = int(1 / step)

    for index in range(steps + 1):
        lightness = index * step
        candidate_hex = hsl_to_hex(hue, saturation, lightness)
        ratio = contrast_ratio(candidate_hex, background_hex)
        lightness_change = abs(lightness - original_lightness)
        if best_match is None or ratio > best_match["ratio"]:
            best_match = {
                "hex": candidate_hex,
                "ratio": ratio,
                "lightness_change": lightness_change,
                "target_met": False,
            }

    return best_match


def generate_accessible_recommendations(
    foreground_hex: str,
    background_hex: str,
) -> List[Dict[str, object]]:
    """Generate three accessible foreground recommendations for a background."""
    current_ratio = contrast_ratio(foreground_hex, background_hex)
    closest = find_related_color_for_target(foreground_hex, background_hex, AA_NORMAL)
    stronger = find_related_color_for_target(foreground_hex, background_hex, AAA_NORMAL)
    if stronger is None:
        stronger = find_best_related_contrast(foreground_hex, background_hex)

    black_ratio = contrast_ratio("#000000", background_hex)
    white_ratio = contrast_ratio("#FFFFFF", background_hex)
    fallback_hex = "#000000" if black_ratio >= white_ratio else "#FFFFFF"
    fallback_ratio = max(black_ratio, white_ratio)

    if closest is None:
        closest = {
            "hex": fallback_hex,
            "ratio": fallback_ratio,
            "lightness_change": 1,
            "target_met": True,
        }

    closest_label = (
        "Recommended: no change needed"
        if current_ratio >= AA_NORMAL and closest["hex"] == foreground_hex
        else "Recommended: closest passing color"
    )

    stronger_label = (
        "Recommended: stronger readability"
        if stronger["ratio"] >= AAA_NORMAL
        else "Recommended: best related option available"
    )

    return [
        {
            "title": (
                "Keep current color"
                if current_ratio >= AA_NORMAL and closest["hex"] == foreground_hex
                else "Closest accessible alternative"
            ),
            "tradeoff": closest_label,
            "hex": closest["hex"],
            "background": background_hex,
            "ratio": closest["ratio"],
            "target": "AA normal text",
        },
        {
            "title": "Optional stronger alternative",
            "tradeoff": stronger_label,
            "hex": stronger["hex"],
            "background": background_hex,
            "ratio": stronger["ratio"],
            "target": "AAA normal text when possible",
        },
        {
            "title": "High contrast fallback",
            "tradeoff": "Recommended: most dependable contrast",
            "hex": fallback_hex,
            "background": background_hex,
            "ratio": fallback_ratio,
            "target": "Maximum black/white contrast",
        },
    ]


def sync_picker_to_hex(picker_key: str, hex_key: str) -> None:
    st.session_state[hex_key] = normalize_hex(st.session_state[picker_key])


def sync_hex_to_picker(hex_key: str, picker_key: str) -> None:
    normalized = normalize_hex(st.session_state[hex_key])
    if normalized:
        st.session_state[hex_key] = normalized
        st.session_state[picker_key] = normalized


def ratio_text(ratio: float) -> str:
    return f"{ratio:.2f}:1"


def status_label(ratio: float, threshold: float, pass_text: str) -> Tuple[str, str]:
    if ratio >= threshold:
        return pass_text, "pass"
    return "Needs more contrast", "fail"


def render_result_pill(label: str, status: str, threshold: str, explanation: str) -> None:
    st.markdown(
        f"""
        <div class="result-pill {status}">
            <div class="result-label">{label}</div>
            <div class="result-threshold">{threshold}</div>
            <div class="result-explanation">{explanation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation_card(recommendation: Dict[str, object], index: int) -> None:
    swatch = recommendation["hex"]
    background = recommendation["background"]
    copy_key = f"copy_hex_{index}_{swatch}_{background}"
    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="card-row">
                <div class="swatch" style="background:{swatch};"></div>
                <div>
                    <div class="card-title">{recommendation["title"]}</div>
                    <div class="card-subtitle">{recommendation["tradeoff"]}</div>
                </div>
            </div>
            <div class="mini-pairing" style="color:{swatch}; background:{background};">
                Sample accessible text
            </div>
            <div class="metric-row"><span>Foreground</span><strong>{swatch}</strong></div>
            <div class="metric-row"><span>Background</span><strong>{background}</strong></div>
            <div class="metric-row"><span>Contrast</span><strong>{ratio_text(recommendation["ratio"])}</strong></div>
            <div class="target-note">Goal: {recommendation["target"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_input(
        "Copy foreground HEX",
        value=str(recommendation["hex"]),
        key=copy_key,
        label_visibility="collapsed",
    )


def render_preview_card(
    title: str,
    foreground: str,
    background: str,
    label: str,
    helper: str,
) -> None:
    st.markdown(
        f"""
        <div class="preview-card" style="color:{foreground}; background:{background};">
            <div>
                <div class="preview-kicker">{label}</div>
                <h3>{title}</h3>
                <div class="preview-helper">{helper}</div>
            </div>
            <p>
                Accessible color choices help students and teams make interface text easier to read
                across devices, lighting conditions, and visual abilities.
            </p>
            <button style="color:{background}; background:{foreground}; border-color:{foreground};">
                Button preview
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="AccessiPair",
    page_icon="AP",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --page: #F7F8FA;
        --card: #FFFFFF;
        --ink: #17202A;
        --muted: #5F6B7A;
        --line: #DDE3EA;
        --green: #1F7A4D;
        --green-bg: #E7F6EE;
        --red: #B42318;
        --red-bg: #FCEBE9;
        --blue: #276EF1;
    }

    .stApp {
        background: var(--page);
        color: var(--ink);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    h1, h2, h3 {
        letter-spacing: 0;
    }

    .hero {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 12px 30px rgba(23, 32, 42, 0.06);
    }

    .hero h1 {
        margin: 0 0 0.35rem 0;
        font-size: clamp(2rem, 4vw, 3.1rem);
    }

    .hero p {
        margin: 0.35rem 0 0 0;
        max-width: 760px;
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.55;
    }

    .section-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 10px 24px rgba(23, 32, 42, 0.045);
        margin-bottom: 1rem;
    }

    .ratio-number {
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        line-height: 1;
        margin: 0.25rem 0 0.8rem 0;
    }

    .result-pill {
        border-radius: 8px;
        padding: 0.85rem;
        border: 1px solid var(--line);
        min-height: 88px;
    }

    .result-pill.pass {
        background: var(--green-bg);
        border-color: #B7E2CA;
    }

    .result-pill.fail {
        background: var(--red-bg);
        border-color: #F3B7B2;
    }

    .result-label {
        font-weight: 750;
        color: var(--ink);
        line-height: 1.25;
    }

    .result-threshold {
        color: var(--muted);
        font-size: 0.9rem;
        margin-top: 0.35rem;
    }

    .result-explanation {
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.38;
        margin-top: 0.35rem;
    }

    .learning-strip, .recommendation-intro, .comparison-note {
        background: #F2F6FB;
        border: 1px solid #D8E4F2;
        border-radius: 8px;
        color: #304255;
        line-height: 1.55;
        padding: 0.85rem 1rem;
        margin: 0.85rem 0 1rem 0;
    }

    .recommendation-intro strong {
        color: var(--ink);
    }

    .recommendation-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem;
        min-height: 280px;
        box-shadow: 0 10px 24px rgba(23, 32, 42, 0.045);
    }

    .card-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.85rem;
    }

    .swatch {
        width: 52px;
        height: 52px;
        border-radius: 8px;
        border: 1px solid rgba(23, 32, 42, 0.18);
        flex: 0 0 auto;
    }

    .card-title {
        font-weight: 800;
        line-height: 1.2;
    }

    .card-subtitle {
        color: var(--muted);
        font-size: 0.92rem;
        margin-top: 0.2rem;
    }

    .target-note {
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.35;
        margin-top: 0.35rem;
    }

    .mini-pairing {
        border-radius: 8px;
        padding: 0.8rem;
        font-weight: 750;
        border: 1px solid rgba(23, 32, 42, 0.12);
        margin: 0.75rem 0;
    }

    .metric-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        border-top: 1px solid #EEF1F5;
        padding: 0.48rem 0;
        color: var(--muted);
        font-size: 0.92rem;
    }

    .metric-row strong {
        color: var(--ink);
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    .preview-card {
        border-radius: 8px;
        padding: 1.2rem;
        min-height: 275px;
        border: 1px solid rgba(23, 32, 42, 0.14);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .preview-card h3 {
        font-size: 1.35rem;
        line-height: 1.2;
        margin: 0.5rem 0;
    }

    .preview-card p {
        max-width: 52ch;
        line-height: 1.55;
        margin: 0 0 1rem 0;
    }

    .preview-kicker {
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0;
        opacity: 0.74;
    }

    .preview-helper {
        font-weight: 750;
        line-height: 1.35;
        margin-bottom: 0.75rem;
    }

    .preview-card button {
        border-radius: 8px;
        border: 1px solid;
        padding: 0.68rem 1rem;
        font-weight: 800;
        width: fit-content;
    }

    .note {
        color: var(--muted);
        line-height: 1.6;
    }

    @media (max-width: 640px) {
        .hero, .section-card, .recommendation-card, .preview-card {
            padding: 0.9rem;
        }

        .metric-row {
            align-items: flex-start;
            flex-direction: column;
            gap: 0.15rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "fg_picker" not in st.session_state:
    st.session_state.fg_picker = "#2F5D8C"
if "bg_picker" not in st.session_state:
    st.session_state.bg_picker = "#F7F8FA"
if "fg_hex" not in st.session_state:
    st.session_state.fg_hex = st.session_state.fg_picker
if "bg_hex" not in st.session_state:
    st.session_state.bg_hex = st.session_state.bg_picker

st.markdown(
    """
    <div class="hero">
        <h1>AccessiPair</h1>
        <p><strong>Create readable, accessible color pairings for interface design.</strong></p>
        <p>
            Color contrast affects readability, accessibility, and usability. AccessiPair helps
            designers check a text/background pairing and find related alternatives that are easier
            for more people to read.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Color Input")
st.caption(
    "Choose a text color and the color behind it. You can use the picker or type a 6-digit HEX value such as #2F5D8C."
)
input_col_1, input_col_2 = st.columns(2)

with input_col_1:
    with st.container(border=True):
        st.color_picker(
            "Foreground/text color",
            key="fg_picker",
            on_change=sync_picker_to_hex,
            args=("fg_picker", "fg_hex"),
            help="Choose the color used for text or icons.",
        )
        st.text_input(
            "Editable foreground HEX",
            key="fg_hex",
            on_change=sync_hex_to_picker,
            args=("fg_hex", "fg_picker"),
            help="Use a 6-digit HEX value like #2F5D8C.",
        )

with input_col_2:
    with st.container(border=True):
        st.color_picker(
            "Background color",
            key="bg_picker",
            on_change=sync_picker_to_hex,
            args=("bg_picker", "bg_hex"),
            help="Choose the color behind the text.",
        )
        st.text_input(
            "Editable background HEX",
            key="bg_hex",
            on_change=sync_hex_to_picker,
            args=("bg_hex", "bg_picker"),
            help="Use a 6-digit HEX value like #F7F8FA.",
        )

foreground = normalize_hex(st.session_state.fg_hex)
background = normalize_hex(st.session_state.bg_hex)

if foreground is None:
    st.error(
        "Foreground HEX is not ready yet. Use exactly six HEX characters using 0-9 and A-F, with or without #. Example: #2F5D8C."
    )
if background is None:
    st.error(
        "Background HEX is not ready yet. Use exactly six HEX characters using 0-9 and A-F, with or without #. Example: #F7F8FA."
    )

if foreground and background:
    current_ratio = contrast_ratio(foreground, background)
    aa_normal_label, aa_normal_status = status_label(
        current_ratio, AA_NORMAL, "Passes for normal text"
    )
    aa_large_label, aa_large_status = status_label(
        current_ratio, AA_LARGE, "Passes for large text"
    )
    aaa_normal_label, aaa_normal_status = status_label(
        current_ratio, AAA_NORMAL, "Passes AAA for normal text"
    )
    recommendations = generate_accessible_recommendations(foreground, background)

    st.markdown("## Contrast Results")
    with st.container(border=True):
        st.caption("WCAG contrast ratio for your selected foreground and background colors.")
        st.markdown(
            '<div class="ratio-number">' + ratio_text(current_ratio) + "</div>",
            unsafe_allow_html=True,
        )

        result_cols = st.columns(3)
        with result_cols[0]:
            render_result_pill(
                aa_normal_label,
                aa_normal_status,
                "AA normal text requires 4.5:1",
                "Use this for most body text, labels, links, and form text.",
            )
        with result_cols[1]:
            render_result_pill(
                aa_large_label,
                aa_large_status,
                "AA large text requires 3:1",
                "Large text is easier to read, so WCAG allows a lower ratio.",
            )
        with result_cols[2]:
            render_result_pill(
                aaa_normal_label,
                aaa_normal_status,
                "AAA normal text requires 7:1",
                "AAA is a stronger target when readability needs extra support.",
            )

        st.markdown(
            """
            <div class="learning-strip">
                <strong>Quick guide:</strong> normal text means everyday interface text such as
                paragraphs, buttons, captions, and labels. Large text usually means at least
                18 pt regular text or 14 pt bold text, so it can be readable at a lower contrast
                threshold.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("## Accessible Alternatives")
    if current_ratio >= AA_NORMAL:
        st.success(
            "Your current pairing passes WCAG AA for normal text. No change is required. The alternatives below are optional if you want even stronger readability."
        )
        st.markdown(
            """
            <div class="recommendation-intro">
                <strong>System recommendation:</strong> keep your current color if it fits the
                design. The optional alternatives show what stronger contrast would look like.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            "Your current pairing needs more contrast for WCAG AA normal text. Use one of the recommended foreground colors below for body text and labels."
        )
        st.markdown(
            """
            <div class="recommendation-intro">
                <strong>System recommendation:</strong> start with the closest accessible
                alternative. It keeps the original hue and saturation as much as possible, then
                adjusts lightness until the pairing passes.
            </div>
            """,
            unsafe_allow_html=True,
        )

    recommendation_cols = st.columns(3)
    for index, recommendation in enumerate(recommendations):
        with recommendation_cols[index]:
            render_recommendation_card(recommendation, index)

    best_recommendation = recommendations[0]
    if current_ratio >= AA_NORMAL:
        stronger_options = [
            item for item in recommendations[1:] if item["ratio"] > current_ratio + 0.01
        ]
        if stronger_options:
            best_recommendation = stronger_options[0]

    st.markdown("## Live Preview")
    st.markdown(
        """
        <div class="comparison-note">
            Compare the original pairing with the recommended version in the same small interface
            pattern: heading, paragraph, and button.
        </div>
        """,
        unsafe_allow_html=True,
    )
    preview_cols = st.columns(2)
    with preview_cols[0]:
        render_preview_card(
            "Original pairing",
            foreground,
            background,
            f"Original choice - {ratio_text(current_ratio)}",
            "This is the color pairing currently selected above.",
        )
    with preview_cols[1]:
        render_preview_card(
            "Recommended pairing",
            str(best_recommendation["hex"]),
            background,
            f"Recommended version - {ratio_text(best_recommendation['ratio'])}",
            "This version uses the foreground color suggested by AccessiPair.",
        )

    st.markdown("## Educational Note")
    st.markdown(
        """
        <div class="section-card">
            <p class="note">
                Contrast ratio compares how bright the foreground color is against the background
                color. A higher ratio usually means text is easier to distinguish. In
                human-centered design, accessible color pairing matters because readability is not
                only a visual preference; it affects whether people can comfortably understand and
                use an interface. AccessiPair supports more inclusive design decisions by turning
                WCAG thresholds into immediate feedback and related color options that preserve the
                designer's intent when possible.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info(
        "Fix the HEX value above to see contrast results and recommendations. HEX colors use six characters, like #2F5D8C or F7F8FA."
    )
