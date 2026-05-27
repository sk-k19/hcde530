# MP1 Competency Claim

## C6 — Data Visualization

For this project, I practiced C6 — Data Visualization by turning my MP1 weather analysis into charts that help answer specific research questions. My dataset has daily winter weather records for eight U.S. cities, so I used pandas to summarize the data by city first, then built charts that made those comparisons easier to understand.

I chose horizontal bar charts for the feels-like temperature gap and humidity comparisons because both questions compare one number across multiple cities. Since the city names are categories, a horizontal layout is easier to read than a vertical bar chart, especially with longer labels like New York City and New Orleans. For the weather pattern chart, I used a grouped horizontal bar chart because I wanted to compare three related percentages — clear days, cloudy days, and rainy days — across the same cities.

The charts are saved as static image files and included in my GitHub repo, along with the Jupyter notebook that shows the code, output, and markdown explanations. This shows that I can choose chart types based on the structure of the data and the question being asked, rather than making charts just to have visuals. The charts also helped me build the Analysis section of MP1 by showing which cities had the biggest feels-like temperature gaps, which cities had the highest humidity, and how winter weather patterns differed across the selected cities.

## C7 — Critical Evaluation and Professional Judgment

This project also demonstrates C7 because I had to evaluate Cursor’s output instead of accepting everything it generated. When I asked Cursor to create a standalone MP1 project folder, it copied over or created a `.venv` folder inside the project directory. That was not something I wanted to publish because virtual environment folders are machine-specific, usually large, and unnecessary for someone reviewing the notebook on GitHub. I caught the issue by checking the file tree before pushing and noticed that the standalone project contained environment files along with the actual notebook, data, charts, and markdown files.

Instead of pushing the folder as is, I decided to remove `.venv` from the MP1 project folder and make sure it was ignored by Git. This is a good example of professional judgment because the AI-generated output technically created a working project folder, but it also included files that should not be part of a clean public repo. I treated Cursor’s work as a draft that still needed review, checked what changed, and corrected the project structure before submitting it.