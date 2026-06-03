# MP2 Competency Claims: AccessiPair

## Claim 1: I built an interactive GenAI-supported design tool that responds to user input in real time.

Evidence: AccessiPair uses Streamlit controls for foreground and background color pickers, editable HEX fields, live validation, and immediate contrast results. The app turns a design question into an interactive workflow where users can test a color pairing, see the ratio, and compare alternatives without leaving the page.

## Claim 2: I connected human-centered design decisions to accessibility standards.

Evidence: The interface explains why color contrast affects readability, accessibility, and usability. The results panel translates WCAG AA and AAA thresholds into plain-language labels such as "Passes for normal text" and "Needs more contrast." The educational note frames contrast as an inclusive design decision rather than only a technical requirement.

## Claim 3: I implemented computational color contrast logic instead of relying on static examples.

Evidence: The app includes helper functions for HEX validation, RGB conversion, relative luminance, WCAG contrast ratio, RGB/HSL conversion, and HSL-to-HEX conversion. The contrast ratio is calculated from the selected colors and rounded to a readable format such as `4.72:1`.

## Claim 4: I designed recommendation logic that balances accessibility with designer intent.

Evidence: When a color pairing fails WCAG AA normal text, AccessiPair converts the original foreground color to HSL, keeps hue and saturation, and adjusts lightness step by step until it finds a foreground color that reaches at least `4.5:1` contrast. The recommendation panel includes a closest accessible option, a stronger contrast option that targets `7:1` when possible, and a black or white high contrast fallback.

## Claim 5: I created a usable interface for learning and comparison.

Evidence: The app separates the experience into clear sections: header, color input, contrast results, accessible alternatives, live preview, and educational note. The live preview shows the original pairing and the recommended accessible version using a text card and a button preview, which makes the accessibility impact easier to see in an interface-like context.

## Claim 6: I practiced documentation and specification engineering.

Evidence: The final repository includes `README.md`, `mp2.md`, and `reflection.md` files that describe the project purpose, audience, setup process, limitations, competency claims, and design decisions. These documents connect the app implementation to the original project goals and make the project understandable to someone outside the course.
