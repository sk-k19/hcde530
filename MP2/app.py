import colorsys
import html
import json
import re
import textwrap
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import streamlit as st


HEX_PATTERN = re.compile(r"^#?[0-9a-fA-F]{6}$")
EXTRACT_HEX_PATTERN = re.compile(r"(?<![0-9A-Fa-f])#?[0-9A-Fa-f]{6}(?![0-9A-Fa-f])")

TARGETS = {
    "ui": {
        "label": "Large UI text / graphics",
        "short_label": "Large UI / graphics",
        "threshold": 3.0,
        "standard": "3:1",
        "explanation": "For large text, thick icons, and graphical UI elements. This is a lower threshold because larger/heavier elements are easier to see.",
    },
    "body": {
        "label": "Body text",
        "short_label": "Body text",
        "threshold": 4.5,
        "standard": "4.5:1",
        "explanation": "For normal paragraph text, labels, descriptions, and helper text. This is the default recommended target.",
    },
    "high": {
        "label": "High readability",
        "short_label": "High readability",
        "threshold": 7.0,
        "standard": "7:1",
        "explanation": "A stricter target for body text and critical information when readability matters more.",
    },
}

SOURCE_LABELS = {
    "custom": "Custom pair",
    "audit_failed": "Failed pair from audit",
    "audit_passing": "Passing pair from audit",
    "saved": "Saved pair",
    "recommendation": "Recommended repair",
}

SAMPLE_PALETTE = """/* Paste design tokens, CSS, or notes. AccessiPair extracts HEX colors. */
--brand-ink: #17202A;
--brand-blue: #2457D6;
--brand-sky: #CFE3FF;
--brand-coral: #FF6B5F;
--brand-mint: #DDF7EC;
--surface: #F7F8FA;
--panel: #FFFFFF;
--warning: #F6C85F;
--success: #197A4D;
--muted-text: #6B7280;
"""


def normalize_hex(value: str) -> Optional[str]:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not HEX_PATTERN.fullmatch(cleaned):
        return None
    if not cleaned.startswith("#"):
        cleaned = f"#{cleaned}"
    return cleaned.upper()


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    normalized = normalize_hex(hex_color)
    if normalized is None:
        raise ValueError(f"Invalid HEX color: {hex_color}")
    return (
        int(normalized[1:3], 16),
        int(normalized[3:5], 16),
        int(normalized[5:7], 16),
    )


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    r, g, b = [max(0, min(255, int(round(channel)))) for channel in rgb]
    return f"#{r:02X}{g:02X}{b:02X}"


def relative_luminance(rgb: Tuple[int, int, int]) -> float:
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
    fg_luminance = relative_luminance(hex_to_rgb(foreground_hex))
    bg_luminance = relative_luminance(hex_to_rgb(background_hex))
    lighter = max(fg_luminance, bg_luminance)
    darker = min(fg_luminance, bg_luminance)
    return (lighter + 0.05) / (darker + 0.05)


def rgb_to_hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r, g, b = [channel / 255 for channel in rgb]
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    return hue * 360, saturation, lightness


def hex_to_hsl(hex_color: str) -> Tuple[float, float, float]:
    return rgb_to_hsl(hex_to_rgb(hex_color))


def hsl_to_rgb(hue: float, saturation: float, lightness: float) -> Tuple[int, int, int]:
    hue = (hue % 360) / 360
    lightness = max(0.0, min(1.0, lightness))
    saturation = max(0.0, min(1.0, saturation))
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return round(r * 255), round(g * 255), round(b * 255)


def hsl_to_hex(hue: float, saturation: float, lightness: float) -> str:
    return rgb_to_hex(hsl_to_rgb(hue, saturation, lightness))


def ratio_text(ratio: float) -> str:
    return f"{ratio:.2f}:1"


def valid_target_key(value: object = None) -> str:
    key = value if isinstance(value, str) else st.session_state.get("target_key")
    return key if key in TARGETS else "body"


def sync_target_choice() -> None:
    st.session_state.target_key = valid_target_key(st.session_state.get("target_choice"))
    st.session_state.target_choice = st.session_state.target_key


def valid_audit_filter(value: object = None) -> str:
    options = {"All", "Passing", "Needs repair"}
    selected = value if isinstance(value, str) else st.session_state.get("audit_filter")
    return selected if selected in options else "Needs repair"


def sync_audit_filter() -> None:
    st.session_state.audit_filter = valid_audit_filter(st.session_state.get("audit_filter_choice"))
    st.session_state.audit_filter_choice = st.session_state.audit_filter


def valid_component_type(value: object = None) -> str:
    options = {"Card", "Button", "Alert", "Form field", "Badge", "Navigation item"}
    selected = value if isinstance(value, str) else st.session_state.get("component_type")
    return selected if selected in options else "Card"


def sync_component_type() -> None:
    st.session_state.component_type = valid_component_type(
        st.session_state.get("component_type_choice")
    )
    st.session_state.component_type_choice = st.session_state.component_type


def ensure_state_integrity() -> None:
    st.session_state.target_key = valid_target_key()
    st.session_state.target_choice = st.session_state.target_key
    st.session_state.audit_filter = valid_audit_filter()
    st.session_state.audit_filter_choice = st.session_state.audit_filter
    st.session_state.component_type = valid_component_type()
    st.session_state.component_type_choice = st.session_state.component_type


def target() -> Dict[str, object]:
    return TARGETS[valid_target_key()]


def passes_target(foreground: str, background: str, target_key: Optional[str] = None) -> bool:
    key = valid_target_key(target_key)
    return contrast_ratio(foreground, background) >= TARGETS[key]["threshold"]


def status_for_pair(foreground: str, background: str, target_key: Optional[str] = None) -> str:
    return "Passes" if passes_target(foreground, background, target_key) else "Needs repair"


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def clean_html(markup: str) -> str:
    return textwrap.dedent(markup).strip()


def extract_hex_colors(text: str) -> List[str]:
    seen = set()
    colors = []
    for match in EXTRACT_HEX_PATTERN.findall(text or ""):
        normalized = normalize_hex(match)
        if normalized and normalized not in seen:
            seen.add(normalized)
            colors.append(normalized)
    return colors


def find_related_color_for_target(
    original_hex: str,
    fixed_hex: str,
    target_ratio: float,
    step: float = 0.005,
) -> Optional[Dict[str, object]]:
    hue, saturation, original_lightness = hex_to_hsl(original_hex)
    best_match = None
    steps = int(1 / step)
    for index in range(steps + 1):
        lightness = index * step
        candidate_hex = hsl_to_hex(hue, saturation, lightness)
        ratio = contrast_ratio(candidate_hex, fixed_hex)
        lightness_change = abs(lightness - original_lightness)
        if ratio >= target_ratio and (
            best_match is None or lightness_change < best_match["change"]
        ):
            best_match = {
                "hex": candidate_hex,
                "ratio": ratio,
                "change": lightness_change,
            }
    return best_match


def find_background_for_target(
    fixed_foreground: str,
    original_background: str,
    target_ratio: float,
    step: float = 0.005,
) -> Optional[Dict[str, object]]:
    hue, saturation, original_lightness = hex_to_hsl(original_background)
    best_match = None
    steps = int(1 / step)
    for index in range(steps + 1):
        lightness = index * step
        candidate_hex = hsl_to_hex(hue, saturation, lightness)
        ratio = contrast_ratio(fixed_foreground, candidate_hex)
        lightness_change = abs(lightness - original_lightness)
        if ratio >= target_ratio and (
            best_match is None or lightness_change < best_match["change"]
        ):
            best_match = {
                "hex": candidate_hex,
                "ratio": ratio,
                "change": lightness_change,
            }
    return best_match


def find_balanced_repair(
    foreground: str,
    background: str,
    target_ratio: float,
    step: float = 0.025,
) -> Optional[Dict[str, object]]:
    fg_hue, fg_sat, fg_light = hex_to_hsl(foreground)
    bg_hue, bg_sat, bg_light = hex_to_hsl(background)
    best_match = None
    steps = int(1 / step)
    for fg_index in range(steps + 1):
        candidate_fg_light = fg_index * step
        candidate_fg = hsl_to_hex(fg_hue, fg_sat, candidate_fg_light)
        fg_change = abs(candidate_fg_light - fg_light)
        for bg_index in range(steps + 1):
            candidate_bg_light = bg_index * step
            candidate_bg = hsl_to_hex(bg_hue, bg_sat, candidate_bg_light)
            ratio = contrast_ratio(candidate_fg, candidate_bg)
            if ratio < target_ratio:
                continue
            bg_change = abs(candidate_bg_light - bg_light)
            total_change = fg_change + bg_change
            spread_penalty = abs(fg_change - bg_change) * 0.2
            score = total_change + spread_penalty
            if best_match is None or score < best_match["score"]:
                best_match = {
                    "foreground": candidate_fg,
                    "background": candidate_bg,
                    "ratio": ratio,
                    "score": score,
                    "change": total_change,
                }
    return best_match


def maximum_readability_pair(foreground: str, background: str) -> Dict[str, object]:
    original_with_black = contrast_ratio("#111111", background)
    original_with_white = contrast_ratio("#FFFFFF", background)
    bg_with_black = contrast_ratio(foreground, "#111111")
    bg_with_white = contrast_ratio(foreground, "#FFFFFF")
    options = [
        {"foreground": "#111111", "background": background, "ratio": original_with_black},
        {"foreground": "#FFFFFF", "background": background, "ratio": original_with_white},
        {"foreground": foreground, "background": "#111111", "ratio": bg_with_black},
        {"foreground": foreground, "background": "#FFFFFF", "ratio": bg_with_white},
    ]
    return max(options, key=lambda item: item["ratio"])


def recommendation_key(recommendation: Dict[str, object]) -> str:
    return f"{recommendation['strategy']}|{recommendation['foreground']}|{recommendation['background']}"


def generate_recommendations(
    foreground: str,
    background: str,
    target_key: Optional[str] = None,
    include_stronger: bool = False,
) -> List[Dict[str, object]]:
    key = valid_target_key(target_key)
    selected_target = TARGETS[key]
    threshold = selected_target["threshold"]
    current_ratio = contrast_ratio(foreground, background)
    if include_stronger:
        threshold = max(threshold, 7.0)

    recommendations: List[Dict[str, object]] = []

    balanced = find_balanced_repair(foreground, background, threshold)
    if balanced:
        recommendations.append(
            {
                "strategy": "Best choice",
                "badge": "Recommended",
                "when": "Use this when both colors can move a little and you want the smallest overall visual change.",
                "foreground": balanced["foreground"],
                "background": balanced["background"],
                "ratio": balanced["ratio"],
                "passes": balanced["ratio"] >= threshold,
                "is_best": True,
                "change": balanced["change"],
            }
        )

    adjusted_text = find_related_color_for_target(foreground, background, threshold)
    if adjusted_text:
        recommendations.append(
            {
                "strategy": "Preserve background",
                "badge": "Fixed surface",
                "when": "Use this when the surface, card, or component background is locked by a brand token.",
                "foreground": adjusted_text["hex"],
                "background": background,
                "ratio": adjusted_text["ratio"],
                "passes": adjusted_text["ratio"] >= threshold,
                "is_best": False,
                "change": adjusted_text["change"],
            }
        )

    adjusted_background = find_background_for_target(foreground, background, threshold)
    if adjusted_background:
        recommendations.append(
            {
                "strategy": "Preserve text color",
                "badge": "Fixed text",
                "when": "Use this when the text color is important and the background can change.",
                "foreground": foreground,
                "background": adjusted_background["hex"],
                "ratio": adjusted_background["ratio"],
                "passes": adjusted_background["ratio"] >= threshold,
                "is_best": False,
                "change": adjusted_background["change"],
            }
        )

    max_pair = maximum_readability_pair(foreground, background)
    recommendations.append(
        {
            "strategy": "Maximum readability",
            "badge": "Fallback",
            "when": "Use this for critical labels, dense data, or moments where readability matters more than palette preservation.",
            "foreground": max_pair["foreground"],
            "background": max_pair["background"],
            "ratio": max_pair["ratio"],
            "passes": max_pair["ratio"] >= threshold,
            "is_best": False,
            "change": 1,
        }
    )

    deduped = []
    seen = set()
    for item in recommendations:
        key_value = recommendation_key(item)
        if key_value not in seen:
            seen.add(key_value)
            deduped.append(item)

    if current_ratio >= TARGETS[key]["threshold"] and not include_stronger:
        return deduped

    deduped.sort(key=lambda item: (not item["is_best"], item["change"], -item["ratio"]))
    return deduped


def audit_palette(colors: List[str], target_key: str) -> List[Dict[str, object]]:
    results = []
    target_key = valid_target_key(target_key)
    threshold = TARGETS[target_key]["threshold"]
    for foreground in colors:
        for background in colors:
            if foreground == background:
                continue
            ratio = contrast_ratio(foreground, background)
            results.append(
                {
                    "foreground": foreground,
                    "background": background,
                    "ratio": ratio,
                    "passes": ratio >= threshold,
                    "target_key": target_key,
                }
            )
    results.sort(key=lambda item: (item["passes"], -item["ratio"]))
    return results


def set_current_pair(
    foreground: str,
    background: str,
    source: str,
    page: Optional[str] = None,
    original_pair: Optional[Dict[str, str]] = None,
    selected_recommendation: Optional[Dict[str, object]] = None,
) -> None:
    st.session_state.foreground = normalize_hex(foreground) or st.session_state.foreground
    st.session_state.background = normalize_hex(background) or st.session_state.background
    st.session_state.source = source
    st.session_state.original_pair = original_pair or {
        "foreground": st.session_state.foreground,
        "background": st.session_state.background,
        "source": source,
    }
    st.session_state.selected_recommendation = selected_recommendation
    if page:
        set_page(page)


def set_page(page: str) -> None:
    st.session_state.page = page
    st.session_state.pending_page = page


def save_pair(
    foreground: str,
    background: str,
    source: str,
    target_key: Optional[str] = None,
    note: str = "",
) -> None:
    key = valid_target_key(target_key)
    ratio = contrast_ratio(foreground, background)
    existing_key = f"{foreground}|{background}|{key}"
    for saved in st.session_state.saved_pairings:
        if saved["dedupe_key"] == existing_key:
            return
    st.session_state.saved_pairings.insert(
        0,
        {
            "id": str(uuid.uuid4()),
            "foreground": foreground,
            "background": background,
            "ratio": ratio,
            "source": source,
            "target_key": key,
            "target_label": TARGETS[key]["label"],
            "saved_at": datetime.now().strftime("%b %d, %Y %I:%M %p"),
            "note": note,
            "dedupe_key": existing_key,
        },
    )


def load_saved_pairing(saved: Dict[str, object], page: str) -> None:
    st.session_state.target_key = valid_target_key(str(saved["target_key"]))
    st.session_state.target_choice = st.session_state.target_key
    set_current_pair(
        str(saved["foreground"]),
        str(saved["background"]),
        "saved",
        page=page,
        original_pair={
            "foreground": str(saved["foreground"]),
            "background": str(saved["background"]),
            "source": "saved",
        },
    )


def choose_audit_pair(
    foreground: str,
    background: str,
    source: str,
    page: str,
    needs_repair: bool = False,
) -> None:
    set_current_pair(
        foreground,
        background,
        source,
        page=page,
        original_pair={"foreground": foreground, "background": background, "source": source},
    )
    if page == "Component Lab" and needs_repair:
        repairs = generate_recommendations(foreground, background)
        st.session_state.selected_recommendation = repairs[0] if repairs else None


def use_recommendation_pair(recommendation: Dict[str, object]) -> None:
    set_current_pair(
        str(recommendation["foreground"]),
        str(recommendation["background"]),
        "recommendation",
        original_pair=st.session_state.original_pair,
        selected_recommendation=recommendation,
    )


def preview_recommendation_pair(recommendation: Dict[str, object]) -> None:
    st.session_state.selected_recommendation = recommendation
    set_page("Component Lab")


def save_recommendation_pair(recommendation: Dict[str, object]) -> None:
    save_pair(
        str(recommendation["foreground"]),
        str(recommendation["background"]),
        str(recommendation["strategy"]),
        note="Saved from recommendation",
    )


def css() -> str:
    return """
    <style>
    :root {
        --page: #F4F7FB;
        --panel: #FFFFFF;
        --panel-strong: #F7FAFF;
        --panel-tint: #EEF5FF;
        --ink: #111827;
        --ink-soft: #253044;
        --muted: #4B5563;
        --muted-2: #667085;
        --soft: #EEF2F8;
        --line: #CAD5E4;
        --line-strong: #AAB7CA;
        --brand: #1E4FD8;
        --brand-strong: #143A9A;
        --brand-soft: #EAF1FF;
        --brand-wash: #DCE8FF;
        --button-secondary: #E7EFFF;
        --button-secondary-hover: #D5E3FF;
        --button-secondary-active: #C3D6FF;
        --violet: #6D3DF5;
        --mint: #08735B;
        --coral: #C83F35;
        --amber: #A76100;
        --success: #0B6B43;
        --success-bg: #E4F7EC;
        --danger: #9F2F28;
        --danger-bg: #FCE8E5;
        --warning-bg: #FFF4D6;
        --shadow: 0 18px 48px rgba(31, 41, 55, 0.10);
        --shadow-soft: 0 8px 22px rgba(31, 41, 55, 0.075);
        --radius: 10px;
        --radius-sm: 8px;
        --space-1: 0.5rem;
        --space-2: 0.75rem;
        --space-3: 1rem;
        --space-4: 1.4rem;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(30,79,216,0.12), transparent 30rem),
            linear-gradient(135deg, #F7FAFF 0%, #F4F7FB 54%, #FFF8F4 100%);
        color: var(--ink);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.8rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        letter-spacing: 0;
        color: var(--ink);
    }

    h1 {
        font-size: clamp(2rem, 4vw, 3rem);
        line-height: 1.02;
    }

    h2 {
        font-size: clamp(1.35rem, 2vw, 1.75rem);
    }

    .stButton > button {
        min-height: 44px;
        border-radius: var(--radius-sm);
        border: 1.5px solid #8EA5D3;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.48), rgba(255,255,255,0) 48%),
            var(--button-secondary);
        color: #102A6B;
        font-weight: 820;
        padding: 0.65rem 0.95rem;
        box-shadow: 0 2px 0 rgba(20, 58, 154, 0.18), 0 8px 18px rgba(31, 41, 55, 0.06);
        transition: background 120ms ease, border-color 120ms ease, box-shadow 120ms ease, transform 120ms ease, color 120ms ease;
    }

    .stButton > button:hover {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.52), rgba(255,255,255,0) 48%),
            var(--button-secondary-hover);
        border-color: var(--brand-strong);
        color: var(--brand-strong);
        box-shadow: 0 3px 0 rgba(20, 58, 154, 0.20), 0 12px 24px rgba(30, 79, 216, 0.15);
        transform: translateY(-1px);
    }

    .stButton > button:active {
        background: var(--button-secondary-active);
        border-color: #102A6B;
        transform: translateY(1px);
        box-shadow: inset 0 2px 6px rgba(16, 42, 107, 0.18);
    }

    .stButton > button:focus-visible,
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible {
        outline: 3px solid #F6C85F !important;
        outline-offset: 2px;
        box-shadow: 0 0 0 5px rgba(30, 79, 216, 0.24) !important;
    }

    .stButton > button[kind="primary"] {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0) 48%),
            var(--brand);
        border-color: var(--brand);
        color: #FFFFFF;
        box-shadow: 0 3px 0 #102A6B, 0 14px 28px rgba(30, 79, 216, 0.24);
    }

    .stButton > button[kind="primary"]:hover {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.16), rgba(255,255,255,0) 48%),
            var(--brand-strong);
        border-color: var(--brand-strong);
        color: #FFFFFF;
    }

    .stButton > button[kind="primary"]:active {
        background: #0F2F7F;
        border-color: #0F2F7F;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.30);
        transform: translateY(1px);
    }

    .stButton > button:disabled,
    .stButton > button[disabled] {
        background: #EEF2F7;
        border-color: #D8DFEA;
        color: #7A8494;
        box-shadow: none;
        transform: none;
    }

    div[data-testid="stSegmentedControl"] button,
    div[data-testid="stRadio"] label {
        min-height: 40px;
    }

    div[data-testid="stSegmentedControl"] {
        border-radius: var(--radius-sm);
    }

    div[data-testid="stSegmentedControl"] button {
        background: #E8F0FF !important;
        border: 1.5px solid #8EA5D3 !important;
        color: #102A6B !important;
        font-weight: 820 !important;
        box-shadow: 0 1px 0 rgba(16,42,107,0.12) !important;
        transition: background 120ms ease, border-color 120ms ease, box-shadow 120ms ease, transform 120ms ease !important;
    }

    div[data-testid="stSegmentedControl"] button:hover {
        background: #D5E3FF !important;
        border-color: var(--brand-strong) !important;
        transform: translateY(-1px);
    }

    button[kind="segmented_control"] {
        background: #E8F0FF !important;
        border: 1.5px solid #8EA5D3 !important;
        color: #102A6B !important;
        font-weight: 820 !important;
        box-shadow: 0 1px 0 rgba(16,42,107,0.14) !important;
    }

    button[kind="segmented_control"] p,
    button[kind="segmented_controlActive"] p {
        color: inherit !important;
        font-weight: inherit !important;
    }

    button[kind="segmented_control"]:hover {
        background: #D5E3FF !important;
        border-color: var(--brand-strong) !important;
        transform: translateY(-1px);
    }

    div[data-testid="stSegmentedControl"] button[aria-pressed="true"],
    div[data-testid="stSegmentedControl"] button[aria-selected="true"],
    div[data-testid="stSegmentedControl"] button[aria-checked="true"],
    div[data-testid="stSegmentedControl"] button[data-selected="true"],
    div[data-testid="stSegmentedControl"] button[kind="primary"],
    button[kind="segmented_controlActive"] {
        background: var(--brand) !important;
        border-color: var(--brand-strong) !important;
        color: #FFFFFF !important;
        box-shadow: inset 5px 0 0 #F6C85F, 0 10px 20px rgba(30,79,216,0.22) !important;
        transform: translateY(1px);
    }

    div[data-testid="stSegmentedControl"] button[aria-pressed="true"]::after,
    div[data-testid="stSegmentedControl"] button[aria-selected="true"]::after,
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]::after,
    div[data-testid="stSegmentedControl"] button[data-selected="true"]::after,
    div[data-testid="stSegmentedControl"] button[kind="primary"]::after,
    button[kind="segmented_controlActive"]::after {
        content: " ✓";
        font-weight: 900;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #172033 100%);
    }

    div[data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    div[data-testid="stSidebar"] .stButton > button {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.72), rgba(255,255,255,0.10)),
            #DCE8FF;
        border: 1.5px solid #8EA5D3;
        color: #102A6B;
        justify-content: flex-start;
        box-shadow: 0 2px 0 rgba(16,42,107,0.16);
        min-height: 46px;
    }

    div[data-testid="stSidebar"] .stButton > button:hover {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.72), rgba(255,255,255,0.10)),
            #C9DAFF;
        border-color: #143A9A;
        color: #102A6B;
        transform: none;
    }

    div[data-testid="stSidebar"] .stButton > button:active {
        background: #BBD0FF;
        box-shadow: inset 0 2px 6px rgba(16,42,107,0.22);
        transform: translateY(1px);
    }

    .shell-brand {
        border-bottom: 1px solid rgba(255,255,255,0.16);
        padding: 0.35rem 0 1.1rem 0;
        margin-bottom: 1rem;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 0.72rem;
    }

    .brand-mark {
        width: 42px;
        height: 42px;
        border-radius: var(--radius-sm);
        display: grid;
        place-items: center;
        color: #FFFFFF;
        font-weight: 900;
        background: linear-gradient(135deg, #0FAE82, #1E4FD8 56%, #D9463E);
        box-shadow: 0 10px 26px rgba(30,79,216,0.32);
    }

    .brand-name {
        font-weight: 900;
        font-size: 1.25rem;
        line-height: 1;
    }

    .brand-sub {
        color: #AAB8CC;
        font-size: 0.82rem;
        margin-top: 0.28rem;
        line-height: 1.35;
    }

    .sidebar-note {
        background: rgba(8, 17, 34, 0.74);
        border: 1px solid rgba(255,255,255,0.20);
        border-radius: var(--radius-sm);
        padding: 0.78rem;
        color: #E7EDF7 !important;
        line-height: 1.45;
        font-size: 0.88rem;
        margin-top: 1rem;
    }

    .sidebar-note * {
        color: #E7EDF7 !important;
    }

    .sidebar-active {
        display: flex;
        align-items: center;
        gap: 0.58rem;
        min-height: 46px;
        margin: 0.25rem 0;
        padding: 0.66rem 0.75rem;
        border-radius: var(--radius-sm);
        background: #EAF1FF;
        color: #102A6B;
        border-left: 5px solid #F6C85F;
        font-weight: 900;
        box-shadow: 0 10px 24px rgba(0,0,0,0.20);
    }

    .sidebar-active-dot {
        width: 0.62rem;
        height: 0.62rem;
        border-radius: 999px;
        background: var(--brand);
        box-shadow: 0 0 0 4px rgba(30,79,216,0.14);
        flex: 0 0 auto;
    }

    .app-hero {
        background:
            linear-gradient(135deg, rgba(17,24,39,0.94), rgba(23,58,146,0.92)),
            linear-gradient(135deg, #17202A, #2457D6);
        color: #FFFFFF;
        border-radius: var(--radius);
        padding: clamp(1.25rem, 3vw, 2.2rem);
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        min-height: 260px;
    }

    .app-hero:after {
        content: "";
        position: absolute;
        inset: auto -12% -26% 42%;
        height: 260px;
        background: linear-gradient(135deg, rgba(15,174,130,0.55), rgba(217,70,62,0.52));
        transform: rotate(-10deg);
        border-radius: 8px;
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 780px;
    }

    .eyebrow {
        text-transform: uppercase;
        font-size: 0.78rem;
        font-weight: 850;
        color: #A7F3D0;
        margin-bottom: 0.75rem;
    }

    .app-hero h1 {
        color: #FFFFFF;
        font-size: clamp(2.35rem, 5vw, 4rem);
        line-height: 0.96;
        margin: 0 0 0.85rem 0;
        max-width: 720px;
    }

    .app-hero p {
        color: #DCE8F8;
        max-width: 680px;
        font-size: 1.08rem;
        line-height: 1.62;
        margin: 0;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        margin-top: 1.25rem;
    }

    .panel, .metric-card, .workflow-card, .recommendation-card, .audit-result, .saved-card, .choice-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(216,223,234,0.9);
        border-radius: var(--radius);
        box-shadow: var(--shadow-soft);
    }

    .choice-card {
        padding: 1rem;
        min-height: 150px;
        background: linear-gradient(135deg, #FFFFFF, #F7FAFF);
    }

    .choice-card strong {
        display: block;
        font-size: 1.02rem;
        margin-bottom: 0.35rem;
    }

    .choice-card span {
        color: var(--muted);
        line-height: 1.45;
        font-size: 0.92rem;
    }

    .next-step {
        background: #101827;
        color: #FFFFFF;
        border-radius: var(--radius);
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: var(--shadow-soft);
    }

    .next-step strong {
        display: block;
        color: #FFFFFF;
        margin-bottom: 0.25rem;
    }

    .next-step span {
        color: #D8E3F4;
        line-height: 1.45;
    }

    .panel {
        padding: var(--space-3);
        margin-bottom: 1rem;
    }

    .panel.feature {
        background: linear-gradient(135deg, #FFFFFF, var(--panel-strong));
    }

    .panel-title {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }

    .panel-title h2, .panel-title h3 {
        margin: 0;
    }

    .muted {
        color: var(--muted);
        line-height: 1.55;
    }

    .quiet {
        color: var(--muted-2);
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .metric-card {
        padding: 1rem;
        min-height: 116px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.84rem;
        font-weight: 760;
        text-transform: uppercase;
    }

    .metric-value {
        color: var(--ink);
        font-size: clamp(1.7rem, 3vw, 2.4rem);
        font-weight: 900;
        line-height: 1.1;
        margin-top: 0.45rem;
    }

    .metric-help {
        color: var(--muted);
        font-size: 0.88rem;
        margin-top: 0.45rem;
        line-height: 1.38;
    }

    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.65rem;
        position: relative;
    }

    .workflow-card {
        padding: 1rem;
        border-top: 0;
        min-height: 132px;
        position: relative;
        overflow: hidden;
    }

    .workflow-card:before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 5px;
        background: var(--brand);
    }

    .workflow-card:nth-child(2):before { background: var(--mint); }
    .workflow-card:nth-child(3):before { background: var(--coral); }
    .workflow-card:nth-child(4):before { background: var(--violet); }
    .workflow-card:nth-child(5):before { background: var(--amber); }

    .workflow-step {
        color: var(--brand-strong);
        font-size: 0.76rem;
        font-weight: 850;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }

    .workflow-card strong {
        display: block;
        margin-bottom: 0.35rem;
        line-height: 1.25;
    }

    .workflow-card span {
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.4;
    }

    .working-pair {
        background: linear-gradient(135deg, #111827, #1D2A44);
        color: #FFFFFF;
        border-radius: var(--radius);
        padding: 1rem;
        box-shadow: var(--shadow);
    }

    .working-pair h3 {
        color: #FFFFFF;
        margin: 0;
    }

    .working-pair .muted {
        color: #C9D5E6;
    }

    .pair-swatches {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.6rem;
        margin: 0.9rem 0;
    }

    .pair-swatch {
        border-radius: var(--radius-sm);
        border: 1px solid rgba(255,255,255,0.18);
        padding: 0.7rem;
        min-height: 78px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .pair-swatch span {
        color: rgba(255,255,255,0.82);
        font-size: 0.76rem;
        font-weight: 780;
        text-transform: uppercase;
    }

    .pair-swatch strong {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.95rem;
    }

    .context-row {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.55rem;
    }

    .context-pill, .status-pill {
        border-radius: var(--radius-sm);
        padding: 0.58rem 0.66rem;
        font-weight: 780;
        font-size: 0.86rem;
        line-height: 1.25;
    }

    .context-pill {
        background: rgba(255,255,255,0.09);
        color: #E7EDF7;
    }

    .status-pill.pass {
        background: var(--success-bg);
        color: var(--success);
        border: 1px solid #A9E5C4;
    }

    .status-pill.fail {
        background: var(--danger-bg);
        color: var(--danger);
        border: 1px solid #F0B4AD;
    }

    .mini-preview, .component-preview, .audit-preview {
        border-radius: var(--radius-sm);
        border: 1px solid rgba(17,24,39,0.14);
    }

    .mini-preview {
        padding: 0.7rem;
        font-weight: 850;
        min-height: 58px;
        display: grid;
        place-items: center;
        margin: 0.7rem 0;
    }

    .recommendation-card {
        padding: 1rem;
        min-height: 330px;
        position: relative;
    }

    .recommendation-card.best {
        border: 2px solid var(--brand);
        background: linear-gradient(135deg, #FFFFFF, #F1F6FF);
    }

    .score-card {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: var(--radius);
        padding: 1.15rem;
        box-shadow: var(--shadow-soft);
    }

    .score-card.pass {
        border-color: #9BDBB8;
        background: linear-gradient(135deg, #FFFFFF, #F1FBF5);
    }

    .score-card.fail {
        border-color: #F0B4AD;
        background: linear-gradient(135deg, #FFFFFF, #FFF5F3);
    }

    .score-number {
        font-size: clamp(2.25rem, 5vw, 3.6rem);
        line-height: 1;
        font-weight: 950;
        margin: 0.25rem 0;
        color: var(--ink);
    }

    .score-label {
        color: var(--muted);
        font-weight: 760;
        line-height: 1.45;
    }

    .status-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.55rem;
        margin: 0.65rem 0;
    }

    .target-summary {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: var(--radius-sm);
        padding: 0.8rem;
        margin: 0.75rem 0 1rem 0;
    }

    .target-summary strong {
        display: block;
        margin-bottom: 0.2rem;
    }

    .rec-actions-note {
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.4;
        margin: 0.35rem 0 0.5rem 0;
    }

    .recommended-callout {
        background: var(--brand-soft);
        border: 1px solid #BBD0FF;
        color: #102A6B;
        border-radius: var(--radius);
        padding: 0.9rem 1rem;
        margin: 0.75rem 0 1rem 0;
        line-height: 1.45;
    }

    .recommended-callout strong {
        color: #102A6B;
    }

    .rec-badge {
        display: inline-flex;
        width: fit-content;
        background: var(--brand-soft);
        color: var(--brand-strong);
        border-radius: 999px;
        padding: 0.24rem 0.55rem;
        font-weight: 850;
        font-size: 0.75rem;
        margin-bottom: 0.55rem;
    }

    .rec-title {
        font-weight: 900;
        font-size: 1.08rem;
        margin-bottom: 0.25rem;
    }

    .rec-copy {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.45;
        min-height: 48px;
    }

    .data-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.8rem;
        border-top: 1px solid #E9EEF5;
        padding: 0.5rem 0;
        color: var(--muted);
        font-size: 0.88rem;
    }

    .data-row strong {
        color: var(--ink);
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    .token-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.75rem;
    }

    .color-token {
        display: inline-flex;
        align-items: center;
        gap: 0.42rem;
        border: 1px solid var(--line);
        background: #FFFFFF;
        border-radius: 999px;
        padding: 0.35rem 0.55rem 0.35rem 0.35rem;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.82rem;
        color: var(--ink);
    }

    .token-dot {
        width: 24px;
        height: 24px;
        border-radius: 999px;
        border: 1px solid rgba(17,24,39,0.18);
    }

    .audit-result {
        padding: 0.9rem;
        margin-bottom: 0.7rem;
    }

    .audit-grid {
        display: grid;
        grid-template-columns: 82px 1.2fr 0.7fr 0.8fr;
        gap: 0.8rem;
        align-items: center;
    }

    .audit-preview {
        width: 70px;
        height: 58px;
        display: grid;
        place-items: center;
        font-size: 1.35rem;
        font-weight: 900;
    }

    .hex-line {
        display: flex;
        flex-wrap: wrap;
        gap: 0.38rem;
        align-items: center;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.9rem;
    }

    .arrow {
        color: var(--muted);
        font-family: inherit;
    }

    .section-heading {
        margin: 0.2rem 0 1.1rem 0;
    }

    .section-heading p {
        color: var(--muted);
        max-width: 820px;
        line-height: 1.55;
        margin-top: 0.35rem;
    }

    .builder-grid {
        display: grid;
        grid-template-columns: minmax(320px, 0.82fr) minmax(440px, 1.18fr);
        gap: 1rem;
        align-items: start;
    }

    .lab-grid {
        display: grid;
        grid-template-columns: 260px 1fr;
        gap: 1rem;
        align-items: start;
    }

    .component-preview {
        min-height: 280px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.18);
    }

    .component-preview h3 {
        color: inherit;
        margin: 0.45rem 0 0.35rem 0;
    }

    .component-preview p {
        line-height: 1.45;
        margin: 0.25rem 0;
    }

    .component-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.65rem;
        margin-bottom: 0.7rem;
    }

    .component-chip {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.28rem 0.58rem;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.28);
        font-weight: 850;
        font-size: 0.76rem;
    }

    .component-note {
        font-size: 0.9rem;
        font-weight: 760;
        opacity: 0.88;
    }

    .mock-surface {
        border-radius: var(--radius-sm);
        border: 1px solid currentColor;
        padding: 0.85rem;
        margin: 0.6rem 0;
        background: rgba(255,255,255,0.08);
    }

    .mock-title {
        font-weight: 900;
        font-size: 1.08rem;
        line-height: 1.2;
        margin-bottom: 0.32rem;
    }

    .mock-line {
        opacity: 0.84;
        font-size: 0.92rem;
        line-height: 1.4;
    }

    .mock-alert {
        border-left: 5px solid currentColor;
    }

    .mock-field {
        border: 1px solid currentColor;
        border-radius: var(--radius-sm);
        padding: 0.65rem;
        margin-top: 0.45rem;
        background: rgba(255,255,255,0.10);
    }

    .comparison-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.85rem;
    }

    .comparison-heading h3 {
        margin: 0;
    }

    .preview-column-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 0.55rem;
    }

    .preview-column-heading strong {
        font-size: 1.04rem;
    }

    .preview-meta {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: var(--radius-sm);
        padding: 0.72rem;
        margin-top: 0.55rem;
        color: var(--ink);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
    }

    .preview-meta span {
        color: var(--muted);
        font-size: 0.88rem;
    }

    .demo-button {
        display: inline-flex;
        width: fit-content;
        border-radius: 8px;
        border: 1px solid currentColor;
        padding: 0.68rem 0.9rem;
        font-weight: 850;
        margin-top: 0.8rem;
    }

    .demo-input {
        border: 1px solid currentColor;
        border-radius: 8px;
        padding: 0.7rem;
        opacity: 0.92;
        margin: 0.5rem 0;
    }

    .saved-card {
        padding: 0.9rem;
        min-height: 274px;
    }

    .save-localstorage {
        display: none;
    }

    @media (max-width: 980px) {
        .workflow-grid, .builder-grid, .lab-grid {
            grid-template-columns: 1fr;
        }

        .audit-grid {
            grid-template-columns: 72px 1fr;
        }
    }

    @media (max-width: 680px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .app-hero {
            min-height: 0;
        }

        .pair-swatches, .context-row {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """


def initialize_state() -> None:
    defaults = {
        "page": "Dashboard / Home",
        "foreground": "#2457D6",
        "background": "#F7F8FA",
        "target_key": "body",
        "source": "custom",
        "selected_recommendation": None,
        "show_stronger": False,
        "import_text": SAMPLE_PALETTE,
        "imported_colors": extract_hex_colors(SAMPLE_PALETTE),
        "audit_filter": "Needs repair",
        "audit_filter_choice": "Needs repair",
        "component_type": "Card",
        "component_type_choice": "Card",
        "target_choice": "body",
        "saved_pairings": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if "original_pair" not in st.session_state:
        st.session_state.original_pair = {
            "foreground": st.session_state.foreground,
            "background": st.session_state.background,
            "source": st.session_state.source,
        }
    ensure_state_integrity()


def render_sidebar() -> None:
    if st.session_state.get("pending_page"):
        st.session_state.page = st.session_state.pending_page
        del st.session_state.pending_page

    st.sidebar.markdown(
        """
        <div class="shell-brand">
            <div class="brand-row">
                <div class="brand-mark">AP</div>
                <div>
                    <div class="brand-name">AccessiPair</div>
                    <div class="brand-sub">Accessible UI color workflow</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    nav_options = [
        "Dashboard / Home",
        "Palette Audit",
        "Pair Builder",
        "Component Lab",
        "Saved Pairings",
    ]
    st.sidebar.caption("Workflow")
    for option in nav_options:
        active = option == st.session_state.page
        if active:
            st.sidebar.markdown(
                f"""
                <div class="sidebar-active">
                    <span class="sidebar-active-dot"></span>
                    <span>{escape(option)}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            continue
        if st.sidebar.button(option, key=f"nav_{option}", use_container_width=True):
            set_page(option)
            st.rerun()
    st.sidebar.markdown(
        """
        <div class="sidebar-note">
            Follow the flow: import, audit, repair, preview, then save.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_action_button(label: str, page: str, key: str, kind: str = "secondary") -> None:
    if st.button(label, key=key, type="primary" if kind == "primary" else "secondary"):
        set_page(page)
        st.rerun()


def render_working_pair(compact: bool = False) -> None:
    foreground = st.session_state.foreground
    background = st.session_state.background
    ratio = contrast_ratio(foreground, background)
    current_target = target()
    passes = ratio >= current_target["threshold"]
    source_label = SOURCE_LABELS.get(st.session_state.source, st.session_state.source)
    next_action = "Preview or save this pair" if passes else "Repair this pair"
    st.markdown(
        f"""
        <div class="working-pair">
            <div class="panel-title">
                <div>
                    <h3>Working Pair</h3>
                    <div class="muted">{escape(source_label)} - {escape(next_action)}</div>
                </div>
                <div class="status-pill {'pass' if passes else 'fail'}">{escape(status_for_pair(foreground, background))}</div>
            </div>
            <div class="pair-swatches">
                <div class="pair-swatch" style="background:{foreground}; color:{background};">
                    <span>Foreground</span>
                    <strong>{foreground}</strong>
                </div>
                <div class="pair-swatch" style="background:{background}; color:{foreground};">
                    <span>Background</span>
                    <strong>{background}</strong>
                </div>
            </div>
            <div class="context-row">
                <div class="context-pill">Contrast: {ratio_text(ratio)}</div>
                <div class="context-pill">Target: {escape(current_target['short_label'])} ({escape(current_target['standard'])})</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not compact:
        col_a, col_b = st.columns(2)
        with col_a:
            render_action_button("Open Pair Builder", "Pair Builder", "wp_builder")
        with col_b:
            render_action_button("Open Component Lab", "Component Lab", "wp_lab")


def render_metric_card(label: str, value: str, help_text: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{escape(label)}</div>
            <div class="metric-value">{escape(value)}</div>
            <div class="metric-help">{escape(help_text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard() -> None:
    colors = st.session_state.imported_colors
    audit_results = audit_palette(colors, st.session_state.target_key) if colors else []
    passing_count = sum(1 for item in audit_results if item["passes"])
    ratio = contrast_ratio(st.session_state.foreground, st.session_state.background)

    hero_col, pair_col = st.columns([1.7, 0.9], gap="large")
    with hero_col:
        st.markdown(
            """
            <div class="app-hero">
                <div class="hero-content">
                    <div class="eyebrow">Accessible color workflow</div>
                    <h1>AccessiPair</h1>
                    <p>
                        Find readable foreground/background pairs, repair weak contrast, and preview
                        the result in UI components before you reuse it in mockups or design systems.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with pair_col:
        render_working_pair(compact=False)

    st.markdown(
        """
        <div class="next-step">
            <strong>Recommended first step</strong>
            <span>Start with Palette Audit if you have several brand or design-token colors. Use Pair Builder when you only need to test one custom pair.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Start Here")
    start_cols = st.columns(3)
    with start_cols[0]:
        st.markdown(
            """
            <div class="choice-card">
                <strong>Audit a pasted palette</strong>
                <span>Best when you have CSS variables, design tokens, or notes with several colors.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_action_button("Start palette audit", "Palette Audit", "dash_choice_audit", "primary")
    with start_cols[1]:
        st.markdown(
            """
            <div class="choice-card">
                <strong>Test one color pair</strong>
                <span>Enter a foreground and background, then get a pass/fail result and repair options.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_action_button("Test custom pair", "Pair Builder", "dash_choice_builder")
    with start_cols[2]:
        st.markdown(
            """
            <div class="choice-card">
                <strong>Preview in UI components</strong>
                <span>See how the current or recommended pair behaves in realistic interface patterns.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_action_button("Preview components", "Component Lab", "dash_choice_lab")

    st.markdown("### Workflow Overview")
    st.markdown(
        """
        <div class="workflow-grid">
            <div class="workflow-card"><div class="workflow-step">Step 1</div><strong>Import colors</strong><span>Paste tokens from Figma notes, CSS, or design documentation.</span></div>
            <div class="workflow-card"><div class="workflow-step">Step 2</div><strong>Audit combinations</strong><span>See which foreground and background pairs pass the selected target.</span></div>
            <div class="workflow-card"><div class="workflow-step">Step 3</div><strong>Repair weak pairs</strong><span>Generate alternatives that preserve design intent where possible.</span></div>
            <div class="workflow-card"><div class="workflow-step">Step 4</div><strong>Preview components</strong><span>Compare original and recommended colors in realistic UI patterns.</span></div>
            <div class="workflow-card"><div class="workflow-step">Step 5</div><strong>Save pairings</strong><span>Keep reusable accessible combinations for future mockups.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Current Workspace")
    metric_cols = st.columns(5)
    with metric_cols[0]:
        render_metric_card("Working ratio", ratio_text(ratio), "Current foreground on background.")
    with metric_cols[1]:
        render_metric_card("Imported colors", str(len(colors)), "Unique HEX colors ready to audit.")
    with metric_cols[2]:
        render_metric_card("Passing pairs", str(passing_count), "Pairs that meet the selected target.")
    with metric_cols[3]:
        render_metric_card("Need repair", str(max(0, len(audit_results) - passing_count)), "Pairs below the target.")
    with metric_cols[4]:
        render_metric_card("Saved pairs", str(len(st.session_state.saved_pairings)), "Reusable accessible choices.")


def render_target_selector(key_prefix: str = "target") -> None:
    target_help = {
        "ui": "Large text, thick icons, and key graphics can pass at a lower contrast because they are easier to see.",
        "body": "This is the everyday minimum for paragraphs, labels, helper text, and most interface copy.",
        "high": "Use this stricter target when the text is critical, dense, or needs extra readability support.",
    }
    st.segmented_control(
        "What are these colors for?",
        options=list(TARGETS.keys()),
        format_func=lambda key: f"{TARGETS[key]['label']} - {TARGETS[key]['standard']}",
        key="target_choice",
        on_change=sync_target_choice,
        help="Choose the UI context you are designing for. AccessiPair checks the pair against that threshold.",
    )
    st.session_state.target_key = valid_target_key(st.session_state.get("target_choice"))
    current_target = target()
    selected_target_key = valid_target_key()
    st.markdown(
        f"""
        <div class="target-summary">
            <strong>{escape(current_target['label'])}: needs {escape(current_target['standard'])}</strong>
            <div class="quiet">{escape(target_help[selected_target_key])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("What do these targets mean?"):
        st.markdown(
            """
            - **Large UI text / graphics - 3:1:** large text, thick icons, and graphical UI elements.
            - **Body text - 4.5:1:** normal paragraph text, labels, descriptions, and helper text.
            - **High readability - 7:1:** stricter contrast for body text and critical information.
            """
        )


def render_palette_tokens(colors: List[str]) -> None:
    if not colors:
        st.info("Paste palette text or load the sample tokens to extract 6-digit HEX colors.")
        return
    token_html = ['<div class="token-wrap">']
    for color in colors:
        token_html.append(
            f'<span class="color-token"><span class="token-dot" style="background:{color};"></span>{color}</span>'
        )
    token_html.append("</div>")
    st.markdown("".join(token_html), unsafe_allow_html=True)

    st.caption("Click a token below to set it as the foreground or background.")
    for color in colors:
        token_col, fg_col, bg_col = st.columns([1.2, 1, 1])
        with token_col:
            st.markdown(
                f'<span class="color-token"><span class="token-dot" style="background:{color};"></span>{color}</span>',
                unsafe_allow_html=True,
            )
        with fg_col:
            if st.button("Set foreground", key=f"token_fg_{color}", use_container_width=True):
                set_current_pair(color, st.session_state.background, "custom")
                st.rerun()
        with bg_col:
            if st.button("Set background", key=f"token_bg_{color}", use_container_width=True):
                set_current_pair(st.session_state.foreground, color, "custom")
                st.rerun()


def render_audit_result(item: Dict[str, object], index: int) -> None:
    foreground = str(item["foreground"])
    background = str(item["background"])
    ratio = float(item["ratio"])
    passes = bool(item["passes"])
    source = "audit_passing" if passes else "audit_failed"
    st.markdown(
        f"""
        <div class="audit-result">
            <div class="audit-grid">
                <div class="audit-preview" style="color:{foreground}; background:{background};">Aa</div>
                <div>
                    <div class="hex-line"><strong>{foreground}</strong><span class="arrow">on</span><strong>{background}</strong></div>
                    <div class="muted">{escape(SOURCE_LABELS[source])} for {escape(target()['label'])}</div>
                </div>
                <div>
                    <div class="metric-label">Contrast</div>
                    <div style="font-weight:900;font-size:1.2rem;">{ratio_text(ratio)}</div>
                </div>
                <div class="status-pill {'pass' if passes else 'fail'}">{'Passes' if passes else 'Needs repair'}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    actions = st.columns(4)
    with actions[0]:
        if passes:
            st.button(
                "Use pair",
                key=f"audit_use_{index}",
                on_click=choose_audit_pair,
                args=(foreground, background, source, "Pair Builder", False),
            )
        else:
            st.button(
                "Repair",
                key=f"audit_repair_{index}",
                type="primary",
                on_click=choose_audit_pair,
                args=(foreground, background, source, "Pair Builder", True),
            )
    with actions[1]:
        st.button(
            "Preview",
            key=f"audit_preview_{index}",
            on_click=choose_audit_pair,
            args=(foreground, background, source, "Component Lab", not passes),
        )
    with actions[2]:
        if passes and st.button("Save", key=f"audit_save_{index}"):
            save_pair(foreground, background, SOURCE_LABELS[source], note="Saved from palette audit")
            st.toast("Saved passing audit pair.")
            st.rerun()
    with actions[3]:
        st.caption("Ready for UI preview" if passes else "Send to repair flow")


def render_palette_audit() -> None:
    st.markdown(
        """
        <div class="section-heading">
            <h1>Palette Audit</h1>
            <p>
                Paste colors from design tokens, CSS, Figma annotations, or rough notes. AccessiPair
                extracts unique 6-digit HEX colors, tests every foreground/background combination,
                and shows which pairs are ready for UI use.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns([0.95, 1.25], gap="large")
    with left:
        st.markdown('<div class="panel feature"><div class="panel-title"><h2>Import Colors</h2></div>', unsafe_allow_html=True)
        text = st.text_area(
            "Palette text",
            key="import_text",
            height=250,
            help="Paste token files, CSS variables, or notes. Six-digit HEX colors are extracted automatically.",
        )
        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Extract colors", type="primary"):
                st.session_state.imported_colors = extract_hex_colors(text)
                st.rerun()
        with btn_cols[1]:
            if st.button("Use sample tokens"):
                st.session_state.import_text = SAMPLE_PALETTE
                st.session_state.imported_colors = extract_hex_colors(SAMPLE_PALETTE)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="panel"><h3>Extracted Tokens</h3>', unsafe_allow_html=True)
        render_palette_tokens(st.session_state.imported_colors)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        render_target_selector("audit")
        colors = st.session_state.imported_colors
        audit_results = audit_palette(colors, st.session_state.target_key) if colors else []
        passing_count = sum(1 for item in audit_results if item["passes"])
        needs_count = len(audit_results) - passing_count
        summary_cols = st.columns(4)
        with summary_cols[0]:
            render_metric_card("Imported", str(len(colors)), "Unique colors")
        with summary_cols[1]:
            render_metric_card("Tested", str(len(audit_results)), "Ordered pairs")
        with summary_cols[2]:
            render_metric_card("Passing", str(passing_count), "Meet target")
        with summary_cols[3]:
            render_metric_card("Need repair", str(needs_count), "Below target")

        st.segmented_control(
            "Filter results",
            ["All", "Passing", "Needs repair"],
            key="audit_filter_choice",
            on_change=sync_audit_filter,
        )
        st.session_state.audit_filter = valid_audit_filter(
            st.session_state.get("audit_filter_choice")
        )
        filtered = audit_results
        if st.session_state.audit_filter == "Passing":
            filtered = [item for item in audit_results if item["passes"]]
        elif st.session_state.audit_filter == "Needs repair":
            filtered = [item for item in audit_results if not item["passes"]]

        st.markdown('<div class="panel"><div class="panel-title"><h2>Audit Results</h2></div>', unsafe_allow_html=True)
        if not filtered:
            st.info("No results match this filter yet.")
        else:
            for index, item in enumerate(filtered[:30]):
                render_audit_result(item, index)
            if len(filtered) > 30:
                st.caption(f"Showing 30 of {len(filtered)} results to keep the audit scannable.")
        st.markdown("</div>", unsafe_allow_html=True)


def sync_manual_pair() -> None:
    fg = normalize_hex(st.session_state.builder_fg)
    bg = normalize_hex(st.session_state.builder_bg)
    if fg and bg:
        set_current_pair(
            fg,
            bg,
            "custom",
            original_pair={"foreground": fg, "background": bg, "source": "custom"},
        )


def render_contrast_result(foreground: str, background: str) -> None:
    ratio = contrast_ratio(foreground, background)
    current_target = target()
    passes = ratio >= current_target["threshold"]
    selected_target_key = valid_target_key()
    target_hint = {
        "ui": "This is the minimum for large text, thick icons, and graphical UI elements.",
        "body": "This is the standard minimum for normal paragraph text and labels.",
        "high": "This is a stricter readability target for critical or dense information.",
    }[selected_target_key]
    plain_result = (
        "This pair passes the selected target."
        if passes
        else "This pair fails the selected target and needs a contrast repair."
    )
    st.markdown(
        f"""
        <div class="score-card {'pass' if passes else 'fail'}">
            <div class="score-label">Contrast ratio</div>
            <div class="score-number">{ratio_text(ratio)}</div>
            <div class="status-row">
                <div class="status-pill {'pass' if passes else 'fail'}">{'Passes selected target' if passes else 'Fails selected target'}</div>
                <div class="quiet">Target: {escape(current_target['label'])} ({escape(current_target['standard'])})</div>
            </div>
            <div class="mini-preview" style="color:{foreground}; background:{background};">
                Aa - interface text preview
            </div>
            <div class="score-label">
                {escape(plain_result)}
            </div>
            <div class="quiet">
                {escape(target_hint)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation_card(recommendation: Dict[str, object], index: int) -> None:
    foreground = str(recommendation["foreground"])
    background = str(recommendation["background"])
    ratio = float(recommendation["ratio"])
    is_best = bool(recommendation.get("is_best"))
    action_label = "Apply recommended fix" if is_best else "Apply this option"
    preview_label = "Preview in components"
    st.markdown(
        f"""
        <div class="recommendation-card {'best' if is_best else ''}">
            <span class="rec-badge">{escape(recommendation['badge'])}</span>
            <div class="rec-title">{escape(recommendation['strategy'])}</div>
            <div class="rec-copy">{escape(recommendation['when'])}</div>
            <div class="mini-preview" style="color:{foreground}; background:{background};">
                Aa - recommended pair
            </div>
            <div class="data-row"><span>Foreground</span><strong>{foreground}</strong></div>
            <div class="data-row"><span>Background</span><strong>{background}</strong></div>
            <div class="data-row"><span>Contrast</span><strong>{ratio_text(ratio)}</strong></div>
            <div class="data-row"><span>Status</span><strong>{'Passes' if recommendation['passes'] else 'Best available'}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="rec-actions-note">
            {'Best choice because it makes the smallest overall change that passes.' if is_best else 'Use this when this constraint matches your design.'}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button(
        action_label,
        key=f"rec_use_{index}",
        type="primary" if is_best else "secondary",
        use_container_width=True,
        on_click=use_recommendation_pair,
        args=(recommendation,),
    )
    st.button(
        preview_label,
        key=f"rec_preview_{index}",
        use_container_width=True,
        on_click=preview_recommendation_pair,
        args=(recommendation,),
    )
    st.button(
        "Save",
        key=f"rec_save_{index}",
        use_container_width=True,
        on_click=save_recommendation_pair,
        args=(recommendation,),
    )


def pair_builder_title() -> Tuple[str, str]:
    source = st.session_state.source
    if source == "audit_failed":
        return (
            "Repair selected audit pair",
            "This pair came from Palette Audit and needs more contrast for the selected target.",
        )
    if source == "audit_passing":
        return (
            "Confirm passing audit pair",
            "This pair already passes. Preview it in context or save it for reuse.",
        )
    if source == "saved":
        return (
            "Review saved pair",
            "This reusable pair is loaded from your saved pairings.",
        )
    return (
        "Test a custom pair",
        "Enter a foreground and background color, choose the UI target, then review the contrast result.",
    )


def render_pair_builder() -> None:
    title, subtitle = pair_builder_title()
    st.markdown(
        f"""
        <div class="section-heading">
            <h1>{escape(title)}</h1>
            <p>{escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.builder_fg = st.session_state.foreground
    st.session_state.builder_bg = st.session_state.background

    left, right = st.columns([0.82, 1.18], gap="large")
    with left:
        st.markdown('<div class="panel"><h2>Colors and Target</h2>', unsafe_allow_html=True)
        st.color_picker("Foreground color", key="builder_fg_picker", value=st.session_state.foreground)
        fg_input = st.text_input("Foreground HEX", value=st.session_state.foreground, key="builder_fg_input")
        st.color_picker("Background color", key="builder_bg_picker", value=st.session_state.background)
        bg_input = st.text_input("Background HEX", value=st.session_state.background, key="builder_bg_input")

        input_cols = st.columns(2)
        with input_cols[0]:
            if st.button("Apply colors", type="primary"):
                fg = normalize_hex(fg_input) or normalize_hex(st.session_state.builder_fg_picker)
                bg = normalize_hex(bg_input) or normalize_hex(st.session_state.builder_bg_picker)
                if fg and bg:
                    set_current_pair(
                        fg,
                        bg,
                        "custom",
                        original_pair={"foreground": fg, "background": bg, "source": "custom"},
                    )
                    st.rerun()
                st.error("Use valid 6-digit HEX colors.")
        with input_cols[1]:
            if st.button("Swap colors"):
                set_current_pair(
                    st.session_state.background,
                    st.session_state.foreground,
                    "custom",
                    original_pair={
                        "foreground": st.session_state.background,
                        "background": st.session_state.foreground,
                        "source": "custom",
                    },
                )
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        render_target_selector("builder")
        render_working_pair(compact=True)

    with right:
        foreground = st.session_state.foreground
        background = st.session_state.background
        ratio = contrast_ratio(foreground, background)
        current_passes = ratio >= target()["threshold"]
        render_contrast_result(foreground, background)

        if current_passes:
            st.success("This pair passes the selected target. No repair is needed.")
            st.markdown(
                """
                <div class="next-step">
                    <strong>Next step</strong>
                    <span>Preview this pair in real UI components, or save it if it is already ready for reuse.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            primary = st.columns(3)
            with primary[0]:
                render_action_button("Preview pair", "Component Lab", "builder_preview_pass", "primary")
            with primary[1]:
                if st.button("Save pair", key="builder_save_pass"):
                    save_pair(foreground, background, SOURCE_LABELS.get(st.session_state.source, "Custom pair"))
                    st.toast("Saved passing pair.")
                    st.rerun()
            with primary[2]:
                if st.button("View stronger alternatives"):
                    st.session_state.show_stronger = not st.session_state.show_stronger
                    st.rerun()
            if st.session_state.show_stronger:
                st.markdown("### Stronger Alternatives")
                st.caption("These are optional because the current pair already passes the selected target.")
                recommendations = generate_recommendations(foreground, background, include_stronger=True)
                rec_cols = st.columns(min(3, len(recommendations)))
                for index, recommendation in enumerate(recommendations):
                    with rec_cols[index % len(rec_cols)]:
                        render_recommendation_card(recommendation, index)
        else:
            st.warning("This pair fails the selected target, so AccessiPair generated repair options.")
            st.markdown(
                """
                <div class="recommended-callout">
                    <strong>Recommended fix</strong>
                    Start with the Best choice card. It changes both colors as little as possible while meeting the selected contrast target.
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("How repairs are chosen"):
                st.markdown(
                    """
                    AccessiPair keeps hue and saturation where possible, then adjusts lightness until the selected target passes.

                    - **Best choice:** adjusts both colors and chooses the smallest total change.
                    - **Preserve background:** keeps the surface color fixed and adjusts the text color.
                    - **Preserve text color:** keeps the text/accent color fixed and adjusts the background.
                    - **Maximum readability:** uses a high-contrast fallback when readability matters most.
                    """
                )
            recommendations = generate_recommendations(foreground, background)
            st.session_state.selected_recommendation = st.session_state.selected_recommendation or (
                recommendations[0] if recommendations else None
            )
            rec_cols = st.columns(min(2, max(1, len(recommendations))))
            for index, recommendation in enumerate(recommendations):
                with rec_cols[index % len(rec_cols)]:
                    render_recommendation_card(recommendation, index)


def component_markup(kind: str, foreground: str, background: str, label: str) -> str:
    common = f'color:{foreground}; background:{background};'
    ratio = contrast_ratio(foreground, background)
    pair_passes = ratio >= target()["threshold"]
    label_lower = label.lower()
    status_text = "Recommended fix" if "recommended" in label_lower else ("Passes target" if pair_passes else "Fails target")
    status_class = "pass" if pair_passes or "recommended" in label_lower else "fail"
    top = clean_html(
        f"""
        <div class="component-top">
            <span class="component-chip">{escape(kind)}</span>
            <span class="status-pill {status_class}">{escape(status_text)}</span>
        </div>
        """
    )
    if kind == "Button":
        return clean_html(
            f"""
        <div class="component-preview" style="{common}">
            <div>{top}
                <div class="mock-title">Checkout actions</div>
                <span class="demo-button">Continue</span>
                <span class="demo-button" style="opacity:0.72;">Back</span>
            </div>
            <div class="component-note">Look at button labels and disabled/secondary states.</div>
        </div>
        """
        )
    if kind == "Alert":
        return clean_html(
            f"""
        <div class="component-preview" style="{common}">
            <div>{top}
                <div class="mock-surface mock-alert">
                    <div class="mock-title">Contrast warning</div>
                    <div class="mock-line">Review this color pair before handoff.</div>
                </div>
            </div>
            <div class="component-note">Alerts need readable headings and short messages.</div>
        </div>
        """
        )
    if kind == "Form field":
        return clean_html(
            f"""
        <div class="component-preview" style="{common}">
            <div>{top}
                <div class="mock-title">Token name</div>
                <div class="mock-field">color.text.primary</div>
                <div class="mock-line">Used for body copy and form labels.</div>
            </div>
            <div class="component-note">Check label, input value, and helper text readability.</div>
        </div>
        """
        )
    if kind == "Badge":
        return clean_html(
            f"""
        <div class="component-preview" style="{common}; min-height:240px;">
            <div>{top}
                <div class="mock-title">Compact status</div>
                <span class="demo-button">Ready for UI</span>
            </div>
            <div class="component-note">Small labels have less letter shape, so contrast matters more.</div>
        </div>
        """
        )
    if kind == "Navigation item":
        return clean_html(
            f"""
        <div class="component-preview" style="{common}">
            <div>{top}
                <div class="mock-title">Navigation</div>
                <div class="mock-surface">
                    <div class="mock-line"><strong>Palette Audit</strong></div>
                    <div class="mock-line" style="opacity:0.72;">Pair Builder</div>
                    <div class="mock-line" style="opacity:0.72;">Saved Pairings</div>
                </div>
            </div>
            <div class="component-note">Active items should be readable at a glance.</div>
        </div>
        """
        )
    return clean_html(
        f"""
    <div class="component-preview" style="{common}">
        <div>{top}
            <div class="mock-surface">
                <div class="mock-title">Project card</div>
                <div class="mock-line">Accessibility review ready</div>
                <div class="mock-line" style="opacity:0.72;">Updated just now</div>
            </div>
        </div>
        <div class="component-note">Check heading, body text, metadata, and action contrast.</div>
    </div>
    """
    )


def render_component_lab() -> None:
    st.markdown(
        """
        <div class="section-heading">
            <h1>Component Lab</h1>
            <p>
                Preview the working pair in realistic interface components. When you arrive from a
                repair flow, compare the original failed pair against the recommended option before
                saving it.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns([0.68, 1.32], gap="large")
    with left:
        render_working_pair(compact=True)
        st.markdown('<div class="panel"><h3>Component Type</h3>', unsafe_allow_html=True)
        st.segmented_control(
            "Choose preview",
            ["Card", "Button", "Alert", "Form field", "Badge", "Navigation item"],
            key="component_type_choice",
            on_change=sync_component_type,
        )
        st.session_state.component_type = valid_component_type(
            st.session_state.get("component_type_choice")
        )
        if st.button("Swap foreground/background", key="lab_swap"):
            set_current_pair(
                st.session_state.background,
                st.session_state.foreground,
                "custom",
                original_pair={
                    "foreground": st.session_state.background,
                    "background": st.session_state.foreground,
                    "source": "custom",
                },
            )
            st.rerun()
        render_action_button("Return to Pair Builder", "Pair Builder", "lab_return")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        selected = st.session_state.selected_recommendation
        original = st.session_state.original_pair
        current_passes = passes_target(st.session_state.foreground, st.session_state.background)
        if selected:
            original_ratio = contrast_ratio(str(original["foreground"]), str(original["background"]))
            recommended_ratio = float(selected["ratio"])
            original_passes = original_ratio >= target()["threshold"]
            st.markdown(
                """
                <div class="comparison-heading">
                    <div>
                        <h3>Original vs Recommended</h3>
                        <div class="quiet">Compare the current pair against the repair before saving it.</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            preview_cols = st.columns(2)
            with preview_cols[0]:
                st.markdown(
                    f"""
                    <div class="preview-column-heading">
                        <strong>Original pair</strong>
                        <span class="status-pill {'pass' if original_passes else 'fail'}">{'Passes target' if original_passes else 'Fails target'}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    component_markup(
                        st.session_state.component_type,
                        str(original["foreground"]),
                        str(original["background"]),
                        "Original pair",
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                    <div class="preview-meta">
                        <span>Original contrast</span>
                        <strong>{ratio_text(original_ratio)}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with preview_cols[1]:
                st.markdown(
                    """
                    <div class="preview-column-heading">
                        <strong>Recommended fix</strong>
                        <span class="status-pill pass">Approved path</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    component_markup(
                        st.session_state.component_type,
                        str(selected["foreground"]),
                        str(selected["background"]),
                        "Recommended pair",
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                    <div class="preview-meta">
                        <span>Recommended contrast</span>
                        <strong>{ratio_text(recommended_ratio)}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown(
                """
                <div class="next-step">
                    <strong>Next step</strong>
                    <span>If the recommended component reads well, apply the fix and save it as an approved pairing.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            action_cols = st.columns(3)
            with action_cols[0]:
                if st.button("Apply recommended fix", type="primary"):
                    set_current_pair(
                        str(selected["foreground"]),
                        str(selected["background"]),
                        "recommendation",
                        selected_recommendation=selected,
                        original_pair=original,
                    )
                    st.rerun()
            with action_cols[1]:
                if st.button("Save recommended pair"):
                    save_pair(
                        str(selected["foreground"]),
                        str(selected["background"]),
                        str(selected["strategy"]),
                        note="Saved from component lab",
                    )
                    st.toast("Saved recommended pair.")
                    st.rerun()
            with action_cols[2]:
                render_action_button("View saved pairs", "Saved Pairings", "lab_saved")
        else:
            st.markdown("### Selected Passing Pair" if current_passes else "### Selected Pair")
            st.markdown(
                component_markup(
                    st.session_state.component_type,
                    st.session_state.foreground,
                    st.session_state.background,
                    "Selected pair",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="preview-meta">
                    <span>Current contrast</span>
                    <strong>{ratio_text(contrast_ratio(st.session_state.foreground, st.session_state.background))} - {status_for_pair(st.session_state.foreground, st.session_state.background)}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
            action_cols = st.columns(2)
            with action_cols[0]:
                if st.button("Save current pair", type="primary"):
                    save_pair(
                        st.session_state.foreground,
                        st.session_state.background,
                        SOURCE_LABELS.get(st.session_state.source, "Custom pair"),
                        note="Saved from component lab",
                    )
                    st.toast("Saved current pair.")
                    st.rerun()
            with action_cols[1]:
                render_action_button("Return to Pair Builder", "Pair Builder", "lab_builder_return")


def render_saved_pairing_card(saved: Dict[str, object], index: int) -> None:
    foreground = str(saved["foreground"])
    background = str(saved["background"])
    st.markdown(
        f"""
        <div class="saved-card">
            <div class="mini-preview" style="color:{foreground}; background:{background};">
                Aa - saved pair
            </div>
            <div class="data-row"><span>Foreground</span><strong>{foreground}</strong></div>
            <div class="data-row"><span>Background</span><strong>{background}</strong></div>
            <div class="data-row"><span>Ratio</span><strong>{ratio_text(float(saved['ratio']))}</strong></div>
            <div class="data-row"><span>Source</span><strong>{escape(saved['source'])}</strong></div>
            <div class="muted">Saved {escape(saved['saved_at'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    actions = st.columns(3)
    with actions[0]:
        if st.button("Use", key=f"saved_use_{index}"):
            load_saved_pairing(saved, "Pair Builder")
            st.rerun()
    with actions[1]:
        if st.button("Preview", key=f"saved_preview_{index}"):
            load_saved_pairing(saved, "Component Lab")
            st.rerun()
    with actions[2]:
        if st.button("Delete", key=f"saved_delete_{index}"):
            st.session_state.saved_pairings = [
                item for item in st.session_state.saved_pairings if item["id"] != saved["id"]
            ]
            st.rerun()


def render_saved_pairings() -> None:
    st.markdown(
        """
        <div class="section-heading">
            <h1>Saved Pairings</h1>
            <p>
                Keep approved foreground/background combinations for design systems, mockups, and
                prototype specs. Saved pairings can be reopened in Pair Builder or Component Lab.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    top_cols = st.columns([0.8, 0.8, 1.2])
    with top_cols[0]:
        if st.button("Save current pair", type="primary"):
            save_pair(
                st.session_state.foreground,
                st.session_state.background,
                SOURCE_LABELS.get(st.session_state.source, "Custom pair"),
                note="Saved from saved pairings view",
            )
            st.toast("Saved current pair.")
            st.rerun()
    with top_cols[1]:
        selected = st.session_state.selected_recommendation
        if selected and st.button("Save selected recommendation"):
            save_pair(
                str(selected["foreground"]),
                str(selected["background"]),
                str(selected["strategy"]),
                note="Saved selected recommendation",
            )
            st.toast("Saved selected recommendation.")
            st.rerun()
    with top_cols[2]:
        st.caption("Saved pairings stay available while you work in this browser session.")

    saved_json = json.dumps(st.session_state.saved_pairings)
    st.markdown(
        f"""
        <div class="save-localstorage" data-pairs='{escape(saved_json)}'></div>
        <script>
        try {{
            const holder = window.parent.document.querySelector('.save-localstorage');
            if (holder) {{
                window.localStorage.setItem('accessipair.savedPairings', holder.dataset.pairs || '[]');
            }}
        }} catch (error) {{}}
        </script>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.saved_pairings:
        st.info("No saved pairings yet. Save a passing audit pair, a recommended repair, or the current working pair.")
        return

    cols = st.columns(3)
    for index, saved in enumerate(st.session_state.saved_pairings):
        with cols[index % 3]:
            render_saved_pairing_card(saved, index)


def main() -> None:
    st.set_page_config(page_title="AccessiPair", page_icon="AP", layout="wide")
    initialize_state()
    st.markdown(css(), unsafe_allow_html=True)
    render_sidebar()

    page = st.session_state.page
    if page == "Palette Audit":
        render_palette_audit()
    elif page == "Pair Builder":
        render_pair_builder()
    elif page == "Component Lab":
        render_component_lab()
    elif page == "Saved Pairings":
        render_saved_pairings()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
