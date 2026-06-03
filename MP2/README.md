# AccessiPair

AccessiPair is a Streamlit workflow app for creating readable, accessible color pairings for interface design.

Designers can paste palette notes or design tokens, audit foreground/background combinations, understand WCAG contrast targets, repair failing pairs, preview recommendations in UI components, and save reusable accessible pairings.

## Audience

AccessiPair is designed for HCD students, UI designers, product designers, and other interface makers who want quick feedback while choosing colors for text, buttons, labels, and design system components.

## Why It Matters

Color contrast affects readability, usability, and inclusion. Checking contrast early helps designers make choices that work for more people across devices, lighting conditions, and visual abilities.

## Core Workflow

AccessiPair is organized around a connected design workflow:

1. Dashboard / Home: start a palette audit, test a custom pair, or open the component lab.
2. Palette Audit: paste design tokens, extract unique HEX colors, audit all pair combinations, and send weak pairs into repair.
3. Pair Builder: test custom colors, review selected audit pairs, choose a WCAG target, and generate repair strategies.
4. Component Lab: compare original and recommended pairings in realistic UI components.
5. Saved Pairings: keep useful accessible combinations for reuse during the session.

## Features

- WCAG contrast math for 3:1, 4.5:1, and 7:1 targets
- Automatic 6-digit HEX extraction from pasted palette text
- Filterable palette audit results for passing and failing pairs
- Repair recommendations for balanced changes, fixed backgrounds, fixed text, and maximum readability
- Component previews for cards, buttons, alerts, form fields, badges, and navigation items
- Session-based saved pairings with use, preview, and delete actions

## Run Locally

From the `MP2` folder:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually:

```text
Local URL: http://localhost:8501
```

Press `Control + C` in Terminal to stop the app.

## Deployment

[Public app URL goes here after deployment]

This project is ready to deploy on Streamlit Community Cloud from GitHub.

## Repository Contents

- `app.py`: Streamlit app and color contrast logic
- `requirements.txt`: Python dependencies
- `README.md`: Project overview and setup
- `mp2.md`: Competency claims
- `reflection.md`: Project reflection
- `.gitignore`: Ignored local and system files

## Limitations

- Evaluates solid foreground/background color pairs only
- Does not analyze images, gradients, transparency, or full interface states
- Provides contrast guidance, not a complete accessibility audit
