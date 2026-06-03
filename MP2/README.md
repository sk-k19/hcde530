# AccessiPair

AccessiPair is a simple Python and Streamlit app for checking whether a foreground/text color and background color have enough contrast for accessible interface design.

Users choose or type two HEX colors. The app calculates the WCAG contrast ratio, explains whether the pairing passes common accessibility thresholds, and recommends accessible foreground alternatives when the pairing does not pass WCAG AA for normal text.

## Who It Is For

AccessiPair is designed for HCD students, UI designers, product designers, and other early-stage interface makers who want fast feedback while choosing colors for text, buttons, labels, and design system components.

## Why Accessible Color Pairing Matters

Color contrast affects readability, usability, and inclusion. Low contrast text can be difficult to read for people with low vision, color vision differences, screen glare, tired eyes, or small mobile screens. Checking contrast early helps designers make choices that work for more people instead of treating accessibility as a final checklist item.

## How To Start The App Locally

These steps are for someone running the project on their own computer.

1. Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/) if it is not already installed.
2. Open Terminal on Mac, or Command Prompt/PowerShell on Windows.
3. Move into the project folder. For example, if the repository is on your Desktop:

```bash
cd path/to/hcde530/MP2
```

4. Install the app dependency:

```bash
python3 -m pip install -r requirements.txt
```

5. Start the Streamlit server:

```bash
python3 -m streamlit run app.py
```

Starting Streamlit with `python3 -m streamlit` is more reliable on Mac because it uses the same Python installation that installed the dependency.

6. After the command runs, Streamlit should print a local URL that looks like this:

```text
Local URL: http://localhost:8501
```

7. Open that URL in a web browser. The AccessiPair app should appear.

To stop the server, go back to Terminal and press `Control + C`.

## How To Test It Locally

You do not need a web development background to test the app. After the app opens in your browser:

1. Try the default colors and confirm the app shows a contrast ratio and pass/fail results.
2. Change the foreground HEX value to `#CCCCCC` and the background HEX value to `#FFFFFF`.
3. Confirm the app says the pairing needs more contrast.
4. Check that the recommendation cards show darker accessible foreground colors.
5. Try an invalid HEX value, such as `#12Z`, and confirm the app shows a helpful error instead of crashing.
6. Try a high contrast pair, such as foreground `#000000` and background `#FFFFFF`, and confirm the app says it passes for normal text.

If the browser does not open automatically, copy the local URL from Terminal and paste it into your browser address bar.

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
