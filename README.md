# movies
(Code related to movie ratings/recommendations, mostly through IMDB scraping)

Currently implemented:
1. actor_stats.py

   Example (David Carradine):
   
![Tom Cruise IMDB scores when he's top billed actor](https://i.imgur.com/zuxC4I6.png)

The code as written is fairly general - all that is required to change actors is a new baseline IMDB page. By default, only leading roles are considered; to change this, set only_leading to False.
