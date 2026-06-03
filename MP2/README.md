# AccessiPair

AccessiPair is a Streamlit app for creating readable, accessible color pairings for interface design.

Enter a foreground color and a background color to check their WCAG contrast ratio. If the pairing needs more contrast, AccessiPair recommends related foreground colors that preserve the original hue and saturation where possible.

## Audience

AccessiPair is designed for HCD students, UI designers, product designers, and other interface makers who want quick feedback while choosing colors for text, buttons, labels, and design system components.

## Why It Matters

Color contrast affects readability, usability, and inclusion. Checking contrast early helps designers make choices that work for more people across devices, lighting conditions, and visual abilities.

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
