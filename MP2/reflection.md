# Reflection

## What did you build?

I built AccessiPair, an interactive Streamlit app that helps HCD students, UI designers, and product designers make more accessible color pairing decisions. The app supports entering custom HEX colors, importing pasted palette text, auditing foreground/background combinations, calculating WCAG contrast ratios, generating accessible repair recommendations, previewing pairings in UI components, and saving useful pairs.

The goal was to move beyond a basic contrast checker. A simple checker can tell a designer that a pair is `3.2:1`, but that does not always explain what the number means, whether it is acceptable for a specific UI use, or what to do next. AccessiPair tries to connect the full workflow: import colors, find weak pairings, repair failed pairs, preview the result in interface components, and save combinations that are useful later.

This came from a real design frustration for me. In UX and HCD work, color choices are rarely abstract math problems. A designer might be working with brand colors, Figma tokens, course project mockups, or a design system that already has a visual direction. When a color pair fails contrast, the useful answer is not only "use black" or "use white." The useful answer is closer to: "Here is the smallest change that preserves the palette, here is the safer readability fallback, and here is what that choice looks like in a button, badge, form field, or card." That is the kind of decision support I wanted AccessiPair to provide.

## What decisions did you make?

My original MP2a declaration said I would build the project in Bolt. I chose Bolt because it was recommended for the assignment and seemed appropriate for an interactive tool with visual UI and some computation. I started there, but Bolt became a problem as the project got more complex. I ran into credit limits, and the generated app stayed too basic. It could produce a visual interface, but it struggled to connect features into a coherent workflow.

I also used ChatGPT to think through the contrast logic, recommendation strategies, and app structure. ChatGPT helped me reason about features and generate pieces of code, but manually inserting code into Bolt still did not solve the full usability problem. The app still felt disconnected: the palette audit, pair repair, component preview, and saved pairings did not feel like one workflow. This was a good reminder that generating code and designing a usable product are related but not the same thing. A page can technically function and still leave a first-time user wondering, "Where did this color pair come from?" or "What am I supposed to click next?"

I eventually switched to Codex because the project needed connected feature logic across multiple pages and more control over a larger codebase. I chose Streamlit/Python for the final version because it made the contrast math, palette parsing, state management, and deployment path more manageable. Streamlit also let me keep everything client-side without authentication, a backend, or a database.

I chose paste/import for Figma/CSS colors instead of real Figma API integration. That felt more realistic for the scope of this project and still matched a real designer workflow: copying design tokens, CSS variables, or notes into a tool. It also kept the project focused on the accessibility decision rather than account setup, authentication, or API permissions. I also scoped the recommendation logic around preserving palette intent when possible. Instead of always jumping to black or white, AccessiPair tries strategies like balanced repair, preserving the surface, preserving the text color, and maximum readability.

Another important decision was to treat the app itself as part of the accessibility argument. Because AccessiPair is about readable UI color pairings, the interface needed clear hierarchy, strong button states, visible pass/fail labels, and plain-language explanations of the 3:1, 4.5:1, and 7:1 targets. I had to keep returning to the user experience, not just the contrast formula.

## What would you do differently?

The app’s strength is that it became more than a basic contrast checker. It tries to preserve palette intent and connect the decision-making process from audit to repair to preview to saving. But the feature set also became complex. As I added palette audit, custom pair testing, recommendation cards, component previews, and saved pairings, the flow became harder to make simple.

Bolt, ChatGPT, and Codex all helped at different points, but they also struggled in different ways. Bolt was useful for quick visual starting points but hit credit limits and did not handle the larger workflow well. ChatGPT was helpful for reasoning, but generated pieces did not automatically become a coherent app. Codex was better for working across the codebase, but adding more prompt context did not always improve usability. Sometimes it created more features or more explanatory text instead of a clearer flow.

If I did this again, I would focus on fewer features in more depth. I might build only palette audit, failed-pair repair, and component preview, then make those three parts extremely clear before adding saved pairings or more recommendation options. For example, I would spend more time on the moment when a user selects a failed palette pair and moves into repair mode. That transition is the heart of the tool, so it should feel almost impossible to miss what happened, what failed, and what AccessiPair recommends next.

I would also user-test the flow with designers earlier, especially the target explanations and recommendation strategies. I want to know whether terms like "preserve surface" and "balanced repair" make sense without explanation. I would probably give a designer a small palette and ask them to complete one realistic task: choose a text color and surface color for a component, repair it if needed, preview it, and save it. Watching where they hesitate would give better guidance than adding more features from my own assumptions.

## What does this work demonstrate?

This project demonstrates **C1 — Vibecoding and Rapid Prototyping** because I used AI tools to move from a plain-language concept to a working app, then iterated when the first platform was not enough. I started with Bolt, used ChatGPT to reason through features, and switched to Codex when the project needed more control and connected logic.

It demonstrates **C2 — Code Literacy and Documentation** because I revised a Python/Streamlit app, added plain-English comments in `app.py`, and updated the README, reflection, and competency claims so someone outside the course can understand the project. The comments explain the parts of the code that matter most for the tool: HEX validation, RGB conversion, luminance, contrast ratio calculation, target checking, palette import, repair generation, session state, and saved pairings.

It demonstrates **C7 — Critical Evaluation and Professional Judgment** because I did not accept the AI-generated output as automatically good. Early versions technically worked but felt like disconnected contrast-checking screens. I had to decide that the problem was not just code correctness but usability and workflow clarity. I also had to recognize when more prompting was making the app busier instead of clearer. That judgment feels connected to HCD practice: the user experience is the evidence, not just the existence of features.

It demonstrates **C8 — Building and Deploying a Complete Tool** because AccessiPair is a complete interactive tool for a real HCD use case. It helps designers make accessible color decisions by importing colors, auditing combinations, repairing failed pairs, previewing results, and saving pairings. The biggest challenge was connecting those features into a tool that someone could actually use during a design workflow, not just proving that the contrast math works.
