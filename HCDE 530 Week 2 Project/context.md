# HCDE 530 Week 2 Project — Context

## Project context
This is a small HCDE 530 “Week 2” demo project for showing **how to work with a dataset in a clear, repeatable way**. It’s written from the perspective of an HCD practitioner: the emphasis is on *understandable steps* and *interpretable outputs*, not advanced software engineering.

## Who this is for
This repo is maintained by an HCD practitioner (not a software engineer). The code should stay approachable, readable, and easy to run.

## What this project is trying to show
The main point is to **demonstrate effective processing of a data file (CSV)** and to **highlight the parts of the code that matter most**:
- Reading a CSV correctly (headers, encoding, using `DictReader`)
- Keeping data in a clear structure (a list of rows / dictionaries)
- Doing a simple, explainable transformation (word counts from text)
- Producing clear outputs (row-by-row summary + overall summary stats)

## What readers should be able to do
After looking at this project, a reader should be able to:
- Run a Python script that loads a CSV and prints a clean summary
- Explain what a “row” is in a CSV and how `DictReader` maps headers → values
- Compute a simple metric (word count) from free-text responses
- Compare responses using the metric (shorter vs longer) *without over-interpreting it*
- Optionally, open a simple dashboard that visualizes the same dataset

## Dataset (how to talk about it)
- **File**: `demo_responses.csv`
- **Expected columns**: `participant_id`, `role`, `response`
- **How to describe it**: a small, “toy” dataset of short qualitative text responses. Each row represents one participant with a role label and a single written response.
- **What it is NOT**: not a representative sample, not enough to generalize from, and not designed for statistical claims—its job is to support learning the workflow.

## Word count (how to interpret it here)
In this project, **word count is a proxy for response length**, not response quality.

- **What it can tell you**:
  - Which responses are brief vs detailed (length)
  - Whether certain roles tend to write longer responses in *this* dataset
  - A quick way to sanity-check or triage text (e.g., find unusually short rows)
- **What it cannot tell you**:
  - Whether a response is “better” or “more insightful”
  - The theme, sentiment, or correctness of what someone said
  - Anything causal (“role causes longer responses”)—the dataset is too small
- **How it’s computed**:
  - We split the text on whitespace and count tokens (simple and explainable)
  - This means punctuation and phrasing can slightly affect counts
  - Empty/blank responses should count as 0

## What’s in this folder
- `demo_responses.csv`: the dataset used in the demo
- `demo_word_count.py`: Python script that loads the CSV and computes word-count summaries
- `dashboard.html`: browser dashboard that loads the CSV and visualizes basic summaries
- `.gitignore`: ignores common local junk files for this folder
- `context.md`: this file

## What “good” code looks like here
Prefer code that is:
- **Readable over clever**: simple control flow, clear variable names
- **Beginner-friendly**: minimal Python features required to understand it
- **Robust enough**: handles blanks reasonably; uses UTF-8 encoding
- **Easy to run**: no complex setup; avoid heavy dependencies

Avoid:
- Big frameworks or complicated project structure
- Assumptions that only make sense to an experienced engineer

## Key “effort signal” areas to focus on
If you’re improving the code, focus effort on making these sections especially clear:
- **Loading the CSV**: the `open(..., encoding="utf-8")` + `csv.DictReader(...)` block
- **Core logic**: `count_words()` and the loop that computes `word_counts`
- **Output clarity**: readable printed table and summary stats (min/max/average)

## How to run

### Python script
Run from inside this folder (so relative paths work):

```bash
cd "HCDE 530 Week 2 Project"
python3 demo_word_count.py
```

### HTML dashboard
Browsers often block loading local files when you open HTML using `file://`.
Instead, start a simple local server in this folder:

```bash
cd "HCDE 530 Week 2 Project"
python3 -m http.server 8000
```

Then open:
- `http://localhost:8000/dashboard.html`

## Constraints and assumptions
- This is a class demo; prioritize clarity and explanation over production-grade engineering.
- The repo includes a folder name with spaces: `HCDE 530 Week 2 Project/`.
  - When running commands in a terminal, **quote the path**.
- CSV is treated as **UTF-8**.

## If you’re an AI assistant helping with this repo
Please:
- Keep changes small and easy to follow.
- When adding functionality, explain *why* it helps the learning goal (effective data processing).
- Prefer edits to existing files over adding many new files.
- Don’t introduce extra dependencies unless there is a strong reason.
