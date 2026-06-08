# MP2 Competency Claims: AccessiPair

## C1 — Vibecoding and Rapid Prototyping

I demonstrated vibecoding and rapid prototyping by using AI tools (specifically Bolt, ChatGPT, and Codex) to build and revise AccessiPair across multiple iterations. In my MP2a declaration I said I would build the project in Bolt, so I initially started there. But while Bolt was useful for quickly generating early interface ideas, I quickly ran into credit limits and the output stayed too basic for the tool I wanted to build. I went through only two iterations of my app interface on Bolt before I ran out of credits. So, I then went to ChatGPT to help me write more code for further app iterations, which I then would plug into Bolt manually. However, even with ChatGPT's guidance, the app features were still too shallow for what I was aiming for, and the different app features did not connect. Bolt and ChatGPT's combination kept giving me a static app page instead of a more complex working app. So, I took my initial Bolt prompt to Codex and refined my app through multiple iterations there. I told it what features I wanted to add, and at first it added them as separate disconnected cards. However through further iterations, I was able to ask it to help me ensure the app features were all connected across pages, and that the information architecture was improved.

I used ChatGPT to reason through feature ideas and code structure, especially around contrast logic, recommendation strategies, and the app workflow. However, manually inserting code into Bolt still did not solve the bigger problem which was that the app needed multiple connected features, and not separate screens. This was one of the biggest learning moments in the project for me. The AI could generate a page that looked like a contrast checker, but it didn't automatically understand the lived design workflow of moving from palette tokens or a custom HEX input to a component decision.

I switched to Codex because I needed to revise and connect a larger Streamlit/Python app. The final version includes a dashboard, palette audit, pair builder, component lab, and saved pairings. The AI tools did well at generating code quickly for UI structure and contrast logic. What I had to correct was the information architecture as early versions had disconnected pages, unclear recommendation cards, and not enough explanation of why one repair option was best. For example selecting a failed audit pair needed to clearly become "repair this failed pair" in Pair Builder, and not just silently update hidden state somewhere else in the app.

So, ultimately I showed C1 in this project by using multiple tools, iterating multiple times with each tool until I got the outcome I wanted, and ending with a deployable tool I was happy with after said iterations. 

## C2 — Code Literacy and Documentation

I demonstrated code literacy and documentation by revising and documenting a Python/Streamlit app rather than only prompting for output. In `app.py`, I added inline comments in plain english that explain important parts of the code for a future designer/developer. These comments cover main functions like HEX validation, HEX-to-RGB conversion, relative luminance, contrast ratio calculation, target checking, palette import, recommendation generation, audit results, session state, and saved pairings. I added these comments for myself so that I understood the main functions the app was using to establish the rules for determining accessible color pairings, but also for any future designers or developers or even myself in the future so that they would be able to understand what the app does and how it functions. It was important to add inline comments that explained what the functions do and why in plain english, so that designers like myself would be able to follow along with what the code is doing. 

This competency matters for me because I am approaching the code as an HCDE student, not as someone whose main background is software engineering. The comments in `app.py` are written like notes to a future designer who needs to understand why the code exists. For example, the contrast math sections explain why HEX colors have to be validated before conversion, why luminance is calculated before the ratio, and why the app checks different targets for large UI elements, body text, and high readability.

## C7 — Critical Evaluation and Professional Judgment

I demonstrated critical evaluation by not treating AI-generated output as automatically correct or usable. Early versions of AccessiPair technically calculated contrast, but they felt more like a static contrast checker than a design workflow tool and that was not enough for my project goal.

I noticed several problems that required judgment:

- Recommendation cards showed WCAG ratios but did not clearly explain which option was best.
- Users could not always tell whether they were testing a custom pair or repairing an imported failed pair.
- Palette audit, repair, component preview, and saving felt disconnected.
- Bolt ran into credit limits and struggled to support the depth of the app.
- Adding more AI prompt context sometimes produced more features, but not a clearer experience.

I responded by changing platforms, reframing the app around a connected workflow, and asking Codex to help improve the flow from audit to repair to preview to save. I also made judgment calls about scope. For example, I chose paste/import for Figma or CSS colors instead of a real Figma API because it was more feasible and still reflected a real designer workflow. A real Figma API integration might sound more impressive, but for this project it would have shifted attention toward authentication and setup instead of the accessibility decision itself.

The biggest professional judgment call was realizing that "working" was not the same as "usable." As someone studying human centered design, I knew that a first time user should not have to infer that a foreground/background selection on one page silently affects another page. I pushed the app toward clearer labels like "Failed pair from audit," "Passing pair from audit," and "Custom pair" because source context changes how a user understands the next action. I also pushed for recommendation language that says why an option is recommended, not only that it passes.

## C8 — Building and Deploying a Complete Tool

I demonstrated building and deploying a complete tool by creating AccessiPair for a real HCD use case which was helping designers make accessible color pairing decisions. The app includes palette import, contrast audit, accessible repair recommendations, component previews, and saved pairings. It is designed for HCD students, UI designers, and product designers who need to make readable color choices while working on prototypes or design systems.

The biggest challenge was connecting multiple complex features into a usable flow. A user needed to understand whether a color pair came from a custom input, a failed palette audit result, a passing audit result, a saved pair, or a recommendation. I handled this by adding source labels, clearer next-step actions, and a workflow that moves from audit to repair to preview to save.

This is a real HCD use case because accessibility color decisions often happen inside messy design work, not in a perfect isolated calculator. A designer may paste in colors from CSS variables, Figma notes, custom HEX codes or a brand palette and then need to know which combinations can be used for body text, labels, buttons, alerts, or badges. AccessiPair supports that practical situation by auditing many combinations, explaining the selected contrast target, generating repair options, and previewing the result in realistic UI components.

