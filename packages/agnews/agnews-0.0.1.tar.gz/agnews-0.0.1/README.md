# Aggregate News Scraping

A simple package to convenience aggregate news scraping through newspaper3k and Google News.

# Usage

```
from agnews.scraper import scrape_ag, parse_ag
query = "YOUR QUERY HERE"
path = "PATH TO DATAFRAME HERE"

scrape_ag(query, path)
parse_ag(path)

```

Credits: Darshan Khandelwal, newspaper3k
