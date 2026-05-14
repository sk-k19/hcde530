# Figma UI3 community feedback — synthesis

**Source:** `week7_figma_feedback.csv` — real posts from the Figma community forum about the UI3 interface change and related editor UX (March–November 2025).

---

## What the majority agrees on

Most rows in the dataset (especially ids 1–20, the UI3 migration thread) converge on a few themes.

### 1. Removal of choice

There is strong agreement that **forcing** users off UI2 is the core problem. Many say they could tolerate UI3 existing if **UI2 stayed optional**, or if the interface could be customized back toward UI2-like layouts.

### 2. UI3 feels worse for day-to-day work

Repeated claims that UI3 is **slower, less efficient, and harder to use** than UI2: lost muscle memory, reorganized controls, “visual noise” (especially the right panel), and a sense that **priorities are wrong** (for example burying useful tools while other elements stay prominent).

### 3. Broken trust in process

Skepticism that **real user research** or forum feedback justified the change. Language appears often that Figma is **not listening**, **ignoring** complaints, or acting **ego-driven**.

### 4. Identity of the audience

Several posts stress irony: **designers who care about UX** are stuck with a product they experience as bad UX.

**Summary narrative:** Mandatory UI3 is experienced as a **downgrade in speed and control**, and **Figma should keep UI2 (or meaningful choice)** instead of deprecating it.

---

## Posts that don’t fit the main narrative

These add a different perspective, a specific technical or interaction concern, or a nuance the consensus thread tends not to develop.

| Id | Author | Why it stands out |
|----|--------|-------------------|
| 10 | Edward Saleeby | **Mixed judgment:** dislikes layout and inputs that look selected without interaction, but **praises resizable panels** — not a flat “everything new is bad” take. |
| 11 | Darius Vitkunas | **Actionable, engineering-level detail** (plans for a Chrome extension): top toolbar, panel order, **visible checkboxes** (e.g. Clip content), dropdown padding. The majority says “slow”; this says **where** it hurts. |
| 12 | Vern B | **Physical workflow:** bottom panel conflicts with a **second laptop** used for requirements — asks for **movable UI**, not only reverting UI2. |
| 15 | Radu Muntean | **Concrete priority inversion:** navbar removed, boolean operations buried vs prominent FigPal — a sharp example others imply but rarely spell out. |
| 17 | Vosidiy M | **Performance hypothesis:** ties **desktop slowness and drag lag** to UI3; names **alternatives** (Motiff, Penpot). Most posts blame layout, not **runtime**. |
| 20 | Bingyan Li | **Micro-detail:** **mouse pointer angle** changed — an outlier that does not argue policy, only disorientation. |
| 21 | Martin Wermers-Pauly | **Different thread and scope** (“Editor UX critique”): **recent Sketch→Figma** user; critique is **general Figma editor UX** (hide vs disable, library publish flows, misleading success toasts, duplicate library tabs, component rules, **CMD-D inconsistency**). Not centered on “give us UI2 back.” |
| 22 | Carlo23 | **Product and strategy angle:** **accessibility**, **new-user friction**, **growth risk**, **Canva, Affinity, AI tools** filling gaps — forecasts consequences beyond power-user anger. |

**Smaller tonal outliers:** Post **7** (Artist and Machine) adds explicit **accessibility** (very small thin type) and briefly acknowledges team effort. Post **8** (suzshu) questions **research and usability testing** in a more analytic register than pure venting.

---

## What the minority view adds

- **Specificity for product work:** Where the majority says “bad UI,” posts **10, 11, 12, 15,** and **20** add **interaction bugs, layout constraints, hardware setup, and micro-affordances** that could be turned into tickets or design criteria.

- **Performance and competition:** Post **17** widens the story from “I don’t like the layout” to **“the app feels slower; I might leave the ecosystem.”**

- **Systemic UX beyond UI3 chrome:** Post **21** reframes the discussion as **cross-cutting patterns** (discoverability, disabled vs hidden states, inconsistent commands). A UI2 toggle alone might not address those.

- **Business and inclusion:** Post **22** adds **accessibility, onboarding, and market** implications that the migration thread mostly skips.

**Overall:** The **consensus** captures legitimate anger about **loss of control and perceived speed**. The **minority threads** add **diagnosable issues, edge cases (multi-device layouts), performance hypotheses, and a broader critique of Figma’s UX discipline** — useful for synthesis aimed at design or strategy, not only at “bring back UI2.”
