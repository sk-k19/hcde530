# Week 5 — Competency reflection

## Competency claim

**C5 — Data Analysis with Pandas**

## My response:

For this assignment, I used pandas to analyze historical winter weather data from the Open-Meteo API for eight different U.S. cities. Specifically, I used data for the previous winter season in Seattle, Phoenix, Miami, Chicago, New York City, Los Angeles, Denver, and New Orleans. My original idea was to compare current weather patterns across all of those cities, but that would have only given me one row per city, so I changed the project to use daily historical data across a full winter season. That gave me enough data to look for patterns instead of only reading values (that could’ve been looked up directly very easily) from a small table.

The questions I wanted to answer were: which cities had the biggest gap between actual temperature and “feels like” temperature, which cities had the highest humidity, and what kinds of weather conditions were most common across the cities. I was mostly interested in patterns that showed how weather, or feels-like temperature, can feel different from what the actual temperature alone suggests. For example I wanted to see whether colder/cloudier cities (like Seattle) had more days where the feels-like temperature felt lower than the actual temperature, whether humid cities stood out consistently across the season, and also whether certain weather conditions were more common in some cities compared to others.

In my notebook I used pandas to check the structure of the dataset with `head()` and `info()`, check for missing values with `isnull().sum()`, count common weather conditions with `value_counts()`, filter for specific types of days, and group by city to compare average humidity and “feels like” temperature differences. These operations helped me answer the questions in a more organized way because I could summarize the data, narrow it down to specific types of weather days and then compare the cities side by side instead of manually scanning rows. The main thing I was trying to understand was how weather feels across different climates, especially because moving from California to Seattle has made me much more aware of how much certain weather conditions can change the experience of temperature. 