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

For this assignment, I extended my MP1 dataset analysis by creating three charts that directly connect to the analytical questions I declared earlier. I used pandas to group the daily weather data by city, calculate average temperature gaps and humidity, and convert true/false weather pattern columns into percentages. I then used matplotlib to create static charts and saved them as image files so they could be committed to my repo.

This work demonstrates that I can move from collecting and cleaning data into visual analysis. Instead of only printing tables, I used charts to compare cities and make patterns easier to see. I also made decisions about chart type based on the structure of the data: bar charts for comparing city-level averages, and a grouped bar chart for comparing multiple weather pattern percentages across cities. The charts are an early version of the Analysis section for MP1b because they begin answering the main questions about feels-like temperature, humidity, and winter weather patterns across the selected cities.
