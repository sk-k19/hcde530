# Reflection

## What did you build?

I built AccessiPair, an interactive Streamlit app that helps HCD students, UI designers, and product designers make more accessible color pairing decisions. The app supports entering custom HEX colors, importing pasted palette text, auditing foreground/background combinations, calculating WCAG contrast ratios, generating accessible repair recommendations, previewing pairings in UI components, and saving useful pairs.

The goal was to move beyond a basic contrast checker. A simple checker can tell a designer that a pair is `3.2:1`, but that does not always explain what the number means or what to do next. AccessiPair tries to connect the full workflow: import colors, find weak pairings, repair failed pairs, preview the result in interface components, and save combinations that are useful later.

## What decisions did you make?

My original MP2a declaration said I would build the project in Bolt. I chose Bolt because it was recommended for the assignment and seemed appropriate for an interactive tool with visual UI and some computation. I started there, but Bolt became a problem as the project got more complex. I ran into credit limits, and the generated app stayed too basic. It could produce a visual interface, but it struggled to connect features into a coherent workflow.

I also used ChatGPT to think through the contrast logic, recommendation strategies, and app structure. ChatGPT helped me reason about features and generate pieces of code, but manually inserting code into Bolt still did not solve the full usability problem. The app still felt disconnected: the palette audit, pair repair, component preview, and saved pairings did not feel like one workflow.

I eventually switched to Codex because the project needed connected feature logic across multiple pages and more control over a larger codebase. I chose Streamlit/Python for the final version because it made the contrast math, palette parsing, state management, and deployment path more manageable. Streamlit also let me keep everything client-side without authentication, a backend, or a database.

I chose paste/import for Figma/CSS colors instead of real Figma API integration. That felt more realistic for the scope of this project and still matched a real designer workflow: copying design tokens, CSS variables, or notes into a tool. I also scoped the recommendation logic around preserving palette intent when possible. Instead of always jumping to black or white, AccessiPair tries strategies like balanced repair, preserving the surface, preserving the text color, and maximum readability.

## What would you do differently?

The app’s strength is that it became more than a basic contrast checker. It tries to preserve palette intent and connect the decision-making process from audit to repair to preview to saving. But the feature set also became complex. As I added palette audit, custom pair testing, recommendation cards, component previews, and saved pairings, the flow became harder to make simple.

Bolt, ChatGPT, and Codex all helped at different points, but they also struggled in different ways. Bolt was useful for quick visual starting points but hit credit limits and did not handle the larger workflow well. ChatGPT was helpful for reasoning, but generated pieces did not automatically become a coherent app. Codex was better for working across the codebase, but adding more prompt context did not always improve usability. Sometimes it created more features or more explanatory text instead of a clearer flow.

If I did this again, I would focus on fewer features in more depth. I might build only palette audit, failed-pair repair, and component preview, then make those three parts extremely clear. I would also user-test the flow with designers earlier, especially the target explanations and recommendation strategies. I want to know whether terms like "preserve surface" and "balanced repair" make sense without explanation.

## What does this work demonstrate?

This project demonstrates **C1 — Vibecoding and Rapid Prototyping** because I used AI tools to move from a plain-language concept to a working app, then iterated when the first platform was not enough. I started with Bolt, used ChatGPT to reason through features, and switched to Codex when the project needed more control and connected logic.

It demonstrates **C2 — Code Literacy and Documentation** because I revised a Python/Streamlit app, added plain-English comments in `app.py`, and updated the README, reflection, and competency claims so someone outside the course can understand the project.

It demonstrates **C7 — Critical Evaluation and Professional Judgment** because I did not accept the AI-generated output as automatically good. Early versions technically worked but felt like disconnected contrast-checking screens. I had to decide that the problem was not just code correctness but usability and workflow clarity.

It demonstrates **C8 — Building and Deploying a Complete Tool** because AccessiPair is a complete interactive tool for a real HCD use case. It helps designers make accessible color decisions by importing colors, auditing combinations, repairing failed pairs, previewing results, and saving pairings.
