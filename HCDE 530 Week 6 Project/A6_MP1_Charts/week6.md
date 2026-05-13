# Week 6 — MP1 Chart Justifications and Competency Claim

## Chart 1: Average Absolute Difference Between Actual and Feels-Like Temperature by City

This chart compares the average absolute gap between actual mean temperature and apparent, or “feels-like,” mean temperature for each city. I chose a horizontal bar chart because the goal is to compare one numeric value across a set of city categories. The x-axis shows the average temperature gap in degrees Fahrenheit, and the y-axis lists the cities.

This chart helps answer my first analytical question: which city had the biggest average difference between actual temperature and “feels like” temperature? Using the absolute gap makes the comparison easier because it focuses on the size of the difference rather than whether the city felt warmer or colder.

## Chart 2: Average Daily Relative Humidity by City

This chart compares average daily relative humidity across the eight cities. I chose a horizontal bar chart because humidity is one continuous numeric measure, and the city names are easier to read horizontally than in a crowded vertical chart. The x-axis shows average relative humidity as a percentage.

This chart helps answer my second analytical question: which city had the highest average humidity, and how does Seattle compare to the others? The chart makes it easier to see whether Seattle is actually near the top of the humidity ranking or whether other cities were more humid during the selected winter period.

## Chart 3: Percent of Winter Days Classified as Clear, Cloudy, or Rainy by City

This chart compares the percentage of days classified as clear, cloudy, or rainy for each city. I chose a grouped horizontal bar chart because the question compares multiple weather patterns across the same set of cities. Percentages are more useful than raw counts here because they make the cities easier to compare across the full winter season.

This chart helps answer my third analytical question: which cities had the most cloudy, rainy, or clear days, and whether there are any rough regional patterns. The regional interpretation should still be treated carefully because each region is represented by only one city, so the chart shows a snapshot of these selected cities rather than a broad claim about entire regions.

## Competency claim

## Competency claim: C6 - Data Visualization

For this assignment, I practiced C6 — Data Visualization by turning my MP1 weather analysis into charts that helped answer my research questions. My dataset has daily winter weather records for eight U.S. cities, so I used pandas to summarize the data by city first, then built charts that made those comparisons easier to understand/visualize.

I chose horizontal bar charts for the feels-like temperature gap and humidity comparisons because both questions compare one number across multiple cities. Since the city names are categories, a horizontal layout is easier to read than a vertical bar chart, especially with longer labels like New York City and New Orleans. For the weather pattern chart, I used a grouped horizontal bar chart because I wanted to compare three related percentages (clear days, cloudy days, and rainy days) across the same cities.

The charts are saved as static image files and included in my GitHub repo, along with the Jupyter notebook that shows the code, output, and markdown explanations. This shows that I can choose proper chart types based on the structure of the data and the questions being asked. The charts also helped me start building the Analysis section of MP1b by showing which cities had the biggest feels-like temperature gaps, which cities had the highest humidity, and how winter weather patterns differed across the cities I selected.
