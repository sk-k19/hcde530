# Reflection

## What did you build?

I built AccessiPair, a small Python and Streamlit tool that helps HCD students and interface designers create accessible color pairings. The user enters a foreground or text color and a background color using either color pickers or editable HEX fields. The app calculates the WCAG contrast ratio, shows whether the pairing passes AA normal text, AA large text, and AAA normal text, and recommends accessible foreground alternatives when the current pairing does not meet the AA normal text threshold. It also includes a live preview so users can compare the original pairing against a recommended accessible version in a simple text card and button context.

## What decisions did you make?

I chose Python and Streamlit because they fit the scope of the assignment and made the project easy to run with `streamlit run app.py`. Streamlit also kept the interface simple, public, and deployable without needing React, routing, authentication, a database, or a complex backend. I kept the project focused on one main tool: checking and improving text/background contrast. That focus made it possible to spend more attention on correctness, plain-language feedback, and a polished student-project interface instead of adding features that would distract from the core accessibility goal.

The most important design decision was to make the recommendations preserve designer intent where possible. Instead of replacing a failing color with a random accessible color, the app converts the foreground color to HSL and adjusts lightness while keeping hue and saturation. This means the suggested color usually feels related to the original choice. I also included a stronger contrast option and a black or white fallback because some backgrounds make subtle related colors less effective. The fallback gives users a dependable option when accessibility needs to matter more than visual similarity.

## What would you do differently?

In a future version, I would add more context-aware preview examples, such as form labels, navigation items, warning text, and disabled states. I would also test the interface with HCD students to see whether the labels and explanations are clear to first-time users. Another improvement would be support for design tokens or small color palettes, so a user could evaluate multiple foreground/background combinations at once. I would still avoid turning the project into a full design system platform unless the course scope required it.

## What does this work demonstrate?

This work demonstrates several competency domains. It shows interactive tool building through a working Streamlit app with live inputs and results. It demonstrates human-centered design and accessibility by translating WCAG contrast guidance into feedback that students and designers can act on. It demonstrates computational reasoning through color conversion, relative luminance, contrast ratio calculation, and recommendation generation. It also demonstrates interface design and usability because the app is organized into clear sections with readable labels, visual swatches, recommendation cards, and live previews. Finally, the README, competency claims, and reflection show documentation and specification engineering by explaining not only what the project does, but why those implementation choices support the goals of the assignment.
