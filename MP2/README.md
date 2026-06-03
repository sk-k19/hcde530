# AccessiPair

AccessiPair is a simple Python and Streamlit app for checking whether a foreground/text color and background color have enough contrast for accessible interface design.

Users choose or type two HEX colors. The app calculates the WCAG contrast ratio, explains whether the pairing passes common accessibility thresholds, and recommends accessible foreground alternatives when the pairing does not pass WCAG AA for normal text.

## Who It Is For

AccessiPair is designed for HCD students, UI designers, product designers, and other early-stage interface makers who want fast feedback while choosing colors for text, buttons, labels, and design system components.

## Why Accessible Color Pairing Matters

Color contrast affects readability, usability, and inclusion. Low contrast text can be difficult to read for people with low vision, color vision differences, screen glare, tired eyes, or small mobile screens. Checking contrast early helps designers make choices that work for more people instead of treating accessibility as a final checklist item.

## How To Run Locally

1. Install Python 3.10 or newer.
2. Install the project dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Streamlit app:

```bash
streamlit run app.py
```

## Public App

[Public app URL goes here after deployment]

The app is intended to be deployed on Streamlit Community Cloud from a public GitHub repository.

## Files Included

- `app.py`: The Streamlit application and color contrast logic.
- `requirements.txt`: Python dependency list for local use and Streamlit deployment.
- `README.md`: Project overview and setup instructions.
- `mp2.md`: Competency claims with evidence from the project.
- `reflection.md`: Project reflection.
- `.gitignore`: Files and folders that should not be committed.

## Limitations

- AccessiPair focuses on foreground text against a single background color. It does not evaluate full layouts, images, gradients, hover states, or transparency.
- Recommendations preserve hue and saturation as much as possible by adjusting lightness, but some backgrounds require black or white for the strongest contrast.
- The tool explains WCAG contrast thresholds, but it is not a complete accessibility audit.
