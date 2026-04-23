# Week 3 — Competency 3: Data cleaning and file handling

Competency claims
C3 — Data Cleaning and File Handling

This week I worked with a messy CSV file and a buggy Python script, and I felt like I was actually learning how to deal with things breaking or things that are messy (which seems to be a very realistic case for the type of data we collect in the real world). When I first ran the script, it crashed with an IndentationError and I didn’t fully understand what that meant. I used Cursor to explain the error to me in plain English, which helped me realize that the loop reading the CSV didn’t have a body, so nothing was being loaded at all. Once I saw that, I asked curosor to help me add the missing lines to append each row into a list, and the script was able to run properly.

Then I ran into a ValueError: invalid literal for int() with base 10: 'fifteen'. I was unsure what this error was as well, so I had Cursor help me break that down too in plain English again, and that’s how I understood that a ValueError is basically Python saying the value isn’t in the format it expected. In this case the script expected a number ('15') but got the word “fifteen.” I fixed that by having Cursor explain how these issues are normally fixed, and it helped me implement the fix which was wrapping the conversion in a try/except block so the script skips bad rows instead of crashing. 

I also realized the “top 5 highest” scores didn’t make sense. After looking at the code more closely with Cursor's help, I saw it was sorting from lowest to highest and then taking the first five values. I asked Cursor for help and then changed the sort to descending so it actually returns the highest scores.

By the end the script reads directly from a CSV file, kept running even when the data we were given was messy and produced consistent output. My commit messages and inline comments show what I changed and why. This week made me more comfortable using error messages as clues and showed me how to take a broken script and make it work on real data (which I now can see is often messy). Also, I added commit messages and inline comments to thoroughly explain each change I made so I could show that I can diagnose errors, use tracebacks to debug issues and make messy data usable.

C2 — Code Literacy and Documentation

This week also pushed me to think about how someone else would understand my code. As I briefly talked about before, I added inline comments throughout the cleaning script while I was working through it, especially in places where I had been confused myself. For example, when I was cleaning the experience values, I added a comment explaining why I was converting words like “fifteen” into numbers, because that was directly tied to the ValueError I had just dealt with and writing that out made it clearer to me too.

I also started organizing the code into small functions like clean_role and clean_experience, which helped me see what each part of the script was responsible for. My commit messages reflect the actual problems I ran into, like the ValueError and the incorrect sorting, and explain what I changed to fix them. I also included a markdown file that explains what the script does and how to run it. I feel that going through this made me realize that understanding code is about being able to explain it, change it and also leave it in a state where someone else could pick it up and follow what’s happening easily.
