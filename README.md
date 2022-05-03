# Reddit and Flashscore SOCCER SCRAPER
Flask Application retrieving all videos from reddit and mapping to the matches from flashscore.
App uses the Flask framework to create a website retrieving all the relevant highlights from football/soccer matches.

# Website as of May 3, 2022
## https://irekniedzialkowski.github.io/index


# Old version:

Soccer/Football scraping scripts enabling the user to view all the goals and other media highlights directly under results scraped from flashscore.

Use the bellow command to get the print of the scores and highlights from most important games played during the day
```python
from reddit_flashscore import print_soccer_hightlights
print_soccer_highlights()
```

To view highlights for past days you can use `day` argument in `print_soccer_highlights` function
```python
# for previous day
print_soccer_highlights(day=-1)
# for day before yesterday
print_soccer_highlights(day=-2)
```
