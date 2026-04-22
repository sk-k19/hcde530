# Week 3 — Competency 3: Data cleaning and file handling

## Competency claim

### C3 — Data Cleaning and File Handling

I worked with a messy CSV file and a buggy Python script, and used error messages to figure out what exactly was breaking and how to fix it so the script could run the data properly. At first the script crashed with an IndentationError because the loop reading the CSV had no body, so nothing was being loaded. I attempted to fix this by adding the missing loop body to actually append each row to a list. After that I hit a ValueError: invalid literal for int() with base 10: 'fifteen', which showed me that one row had text instead of a number in the experience column ('fifteen' vs. '15'). I handled this by wrapping the int() conversion in a try/except block and skipping any rows that couldn’t be converted. I also noticed the “top 5 highest” scores were wrong because the list was sorted in ascending order, so I changed the sort to descending before selecting the top five results. The final script reads directly from a CSV file, handles messy values and produces consistent output. My commit messages and inline comments explain each step showing that I can diagnose errors, use tracebacks to debug issues and make messy data usable.
