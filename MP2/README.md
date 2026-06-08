# AccessiPair

AccessiPair is a Streamlit app that helps designers create accessible foreground/background color pairings for interface design.

The tool lets users enter custom HEX colors, paste palette colors from design tokens or CSS notes, audit possible color combinations, understand contrast ratios, repair weak pairs, preview colors in UI components, and save useful accessible pairings.

## Who It Is For

AccessiPair is intended for HCD students, UI designers, product designers, and anyone working on mockups, prototypes, or design systems who needs quick support choosing readable UI colors.

## Why Accessible Color Pairing Matters

Color contrast affects whether people can read text, understand UI states, and use an interface comfortably. Designers often have to balance accessibility with brand or palette constraints. AccessiPair is meant to help with that decision, not just report a number.

## Main Features

- Enter custom text and surface colors
- Import or paste palette colors from CSS, design tokens, or notes
- Extract unique 6-digit HEX colors automatically
- Audit foreground/background palette combinations
- Calculate WCAG contrast ratios
- Explain the 3:1, 4.5:1, and 7:1 targets in plain language
- Generate accessible repair recommendations
- Preview pairings in realistic UI components
- Save useful color pairings for reuse

## Contrast Targets

AccessiPair uses three target levels:

- **3:1 — Large UI text / graphics:** good for large headings, icons, thick borders, graphics, and UI states.
- **4.5:1 — Body text:** good for paragraphs, labels, descriptions, and helper text.
- **7:1 — High readability:** a stricter target for body text or critical information.

## Live Links

Live app: (https://accessipair.streamlit.app/)

## How To Run Locally

From the `MP2` folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Press `Control + C` in the terminal to stop the app.

## Built With

- Python
- Streamlit
- WCAG contrast logic
- AI-assisted development using Bolt, ChatGPT, and Codex

## Development Note

My original MP2a plan was to build AccessiPair in Bolt. I started there because Bolt was recommended for the assignment and seemed like a good match for an interactive visual tool. As the app grew, I ran into Bolt credit limits and the generated app stayed too basic. It also struggled to connect palette audit, pair repair, component preview, and saved pairings into one clear workflow.

I used ChatGPT to reason through features and generate pieces of code, but manually inserting those pieces into Bolt still did not solve the larger structure problem. I eventually switched to Codex and Streamlit/Python because I needed more control over the app logic, state, documentation, and connected workflow.

## Repository Contents

- `app.py` — Streamlit app, WCAG contrast logic, palette audit, recommendation generation, component previews, and saved pairings
- `requirements.txt` — Python dependencies
- `README.md` — project overview and local setup
- `reflection.md` — project reflection
- `mp2.md` — competency claims

## Limitations

- AccessiPair checks solid HEX foreground/background pairings only.
- It does not analyze images, gradients, opacity, or full interface screenshots.
- Saved pairings are stored in the current browser/session workflow, not in a backend database.
- The tool gives contrast guidance, not a complete accessibility audit.
