# movies
(Code related to movie ratings/recommendations, mostly through IMDB scraping)

Currently implemented:
1. tom_cruise.py

   Given his recent successes with Edge of Tomorrow and (apparently) Mission Impossible, I was curious to see if his movies were getting better over time. The answer is slightly yes, with a good consistency all the way back to the 1980s:

![Tom Cruise IMDB scores when he's top billed actor](https://i.imgur.com/0aCN8nw.png)

The code as written is fairly general - all that is required to change actors is a new baseline IMDB page and some edits to the graph wording. Note that the code also currently only counts movies in which Tom Cruise was the top billed actor - this is a simple if condition and may be turned off at any time.
