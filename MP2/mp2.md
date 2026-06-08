# MP2 Competency Claims: AccessiPair

## C1 — Vibecoding and Rapid Prototyping

I demonstrated vibecoding and rapid prototyping by using AI tools to build and revise AccessiPair across multiple iterations. My MP2a declaration said I would build the project in Bolt, so I started there. Bolt was useful for quickly generating early interface ideas, but I ran into credit limits and the output stayed too basic for the tool I wanted to build.

I then used ChatGPT to reason through feature ideas and code structure, especially around contrast logic, recommendation strategies, and the app workflow. However, manually inserting code into Bolt still did not solve the bigger problem: the app needed multiple connected features, not just separate screens.

I switched to Codex because I needed to revise and connect a larger Streamlit/Python app. The final version includes a dashboard, palette audit, pair builder, component lab, and saved pairings. The AI tools did well at generating code quickly for UI structure and contrast logic. What I had to correct was the information architecture: early versions had disconnected pages, unclear recommendation cards, and not enough explanation of why one repair option was best.

Evidence: the final deployed app, the Streamlit app in `app.py`, the platform switch from Bolt to Codex, and the commit history showing multiple workflow and usability revisions.

## C2 — Code Literacy and Documentation

I demonstrated code literacy and documentation by revising and documenting a Python/Streamlit app rather than only prompting for output. In `app.py`, I added plain-English comments explaining important parts of the code for a future designer/developer. These comments cover HEX validation, HEX-to-RGB conversion, relative luminance, contrast ratio calculation, target checking, palette import, recommendation generation, audit results, session state, and saved pairings.

The README now explains what AccessiPair does, who it is for, why accessible color pairing matters, how to run the app locally, and where to add the live deployment and repository links. The `reflection.md` file explains what I built, the platform decisions I made, what went wrong, and what I would do differently. This `mp2.md` file documents the competency claims with specific evidence instead of general statements.

Evidence: comments in `app.py`, the updated `README.md`, this `mp2.md`, and `reflection.md`.

## C7 — Critical Evaluation and Professional Judgment

I demonstrated critical evaluation by not treating AI-generated output as automatically correct or usable. Early versions of AccessiPair technically calculated contrast, but they felt more like a static contrast checker than a design workflow tool. That was not enough for the project goal.

I noticed several problems that required judgment:

- Recommendation cards showed ratios but did not clearly explain which option was best.
- Users could not always tell whether they were testing a custom pair or repairing an imported failed pair.
- Palette audit, repair, component preview, and saving felt disconnected.
- Bolt ran into credit limits and struggled to support the depth of the app.
- Adding more AI prompt context sometimes produced more features, but not a clearer experience.

I responded by changing platforms, reframing the app around a connected workflow, and asking Codex to help improve the flow from audit to repair to preview to save. I also made judgment calls about scope. For example, I chose paste/import for Figma or CSS colors instead of a real Figma API because it was more feasible and still reflected a real designer workflow.

Evidence: the platform-switch explanation in `reflection.md`, the connected state and source labels in `app.py`, and the workflow improvements across Palette Audit, Pair Builder, Component Lab, and Saved Pairings.

## C8 — Building and Deploying a Complete Tool

I demonstrated building and deploying a complete tool by creating AccessiPair for a real HCD use case: helping designers make accessible color decisions. The app includes palette import, contrast audit, accessible repair recommendations, component previews, and saved pairings. It is designed for HCD students, UI designers, and product designers who need to make readable color choices while working on prototypes or design systems.

The biggest challenge was not making the contrast math work. The harder problem was connecting complex features into a usable flow. A user needed to understand whether a pair came from a custom input, a failed palette audit result, a passing audit result, a saved pair, or a recommendation. I handled this by adding source labels, clearer next-step actions, and a workflow that moves from audit to repair to preview to save.

The project also includes documentation that explains what the tool does, who it is for, how to run it, what went wrong, and what I would do differently. The live app and public repository links still need to be pasted into `README.md` once the final deployment URL is available.

Evidence: `app.py`, `README.md`, `reflection.md`, this `mp2.md`, the public app URL placeholder, and the public GitHub repository placeholder.
