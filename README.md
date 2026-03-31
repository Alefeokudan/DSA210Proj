# DSA210Proj
Ali Efe Okudan 34314 Sabancı University proj GitHub reporsitory.

Project Proposal: Digital Escapism and Socio-Economic Stress
Motivation The primary goal of this project is to explore the "escapism" hypothesis: the idea that individuals increase their engagement with virtual environments during periods of real-world socio-economic stress. By analyzing the relationship between macroeconomic volatility in Turkey and active player counts on the Steam platform, I aim to determine if digital gaming serves as a primary coping mechanism during financial instability. This project will apply the full data science pipeline to a real-world behavioral problem.
Where will I get the data? I will acquire the data from three distinct digital sources to ensure a comprehensive analysis and satisfy the enrichment requirement:
Gaming Data: Daily concurrent global player counts for high-engagement titles (such as Counter-Strike 2) will be sourced from SteamCharts or the SteamDB.
Economic Indicators: Historical daily USD/TRY exchange rate data will be retrieved from the Yahoo Finance database using the yfinance library.
Societal Stress Indicators: Search volume intensity within Turkey for stress-related keywords (e.g., "ekonomik kriz", "enflasyon") will be obtained via Google Trends to enrich the dataset.
How will you collect it? The data collection process will be automated using Python-based tools:
I will utilize the yfinance library to download daily financial time-series data.
The pytrends API wrapper will be used to fetch normalized search interest scores for the selected keywords.
Since Steam does not provide real-time player counts filtered specifically by country, I will use Google Trends search volume within Turkey as a localized proxy to weight and enrich the global Steam trend data.
All datasets will be integrated into a unified dataframe using the Pandas library, synchronized by date.
The characteristics of the data you will be using: 
Sample Size: The dataset will cover a 24-month period, providing approximately 730 daily data points for each variable to ensure statistical relevance.
Data Types: The features include temporal data (dates), continuous numerical values (exchange rates and player counts), and normalized indices (Google Trend scores).
Preprocessing: The data will undergo cleaning to handle missing values from market holidays and will be scaled using normalization techniques to allow for accurate comparison between diverse units
