# Week 2 — Competency 2: Code literacy and documentation

This file captures **your** observations for HCDE 530. We’ll fill it in through a short interview so the language stays in your voice.

---

## What “code literacy and documentation” means to me (this week)

### Code literacy

For me, code literacy means being able to read and understand what a script is doing at a basic level, even if I didn’t write it myself. As an HCD person, it also means I can communicate with engineers, ask better questions, and judge whether a tool or output makes sense instead of just trusting it blindly.

### Documentation

Good documentation means clearly explaining what the code does, how to run it, and what the output actually means so someone else can understand and use it without confusion. For a small class project, it should be simple but complete enough that another student could pick it up and not feel lost.

---

## What I can do now that I couldn’t (or wasn’t confident doing) before

This week, I got more comfortable working with data in Python, especially reading and exploring CSV files, which I wasn’t confident doing before. I also learned how to use Git to track changes and push my work. It was confusing at first, but now I feel a lot more comfortable using it.

---

## How I documented or explained my work

Examples: `context.md`, comments in Python, README-style notes, how someone else would run the scripts.

This week I used AI to generate `context.md` as a baseline explanation of our code, added comments in my Python files to clarify key logic, and used `.cursorrules` to keep development consistent while working in Cursor.

---

## Evidence from this project

Point to concrete artifacts (files, behaviors). For example: reading a CSV, counting words, dashboard, Git/GitHub.

_(Draft after Q4.)_

---

## What was hard or confusing—and what helped

_(Draft after Q5.)_

---

## What I want to practice next

_(Draft after Q6.)_

---

## Notes / quotes I want to keep verbatim

_(Optional: paste phrases you want to remember.)_

---

## Competency claim

### C2 — Code Literacy and Documentation

In `demo_word_count.py`, I added inline comments that explain how the script loads the CSV file, loops through each response, and stores word counts so the program can print summary statistics at the end. I used Cursor to help me understand what each part of the code was doing and how they tie together, then rewrote those explanations in plain English so I wasn’t running code without understanding it first.

For example, I initially didn't understand what `csv.DictReader` did. So, I used Cursor's autofill function to write the initial inline comment to see what the function does, and then I was able to rewrite the comment in plain English so that I better understood what `DictReader` is used for (which is that it basically turns your rows into a dictionary so you can access values using column names to make things a bit easier).

This was my overall approach with the rest of the inline comments as well, as I focused on adding “why” explanations in my comments so that if I revisit this file later, I can understand the logic behind each step without having to relearn how the code works or so that anyone else reading my work is able to follow what I did.
