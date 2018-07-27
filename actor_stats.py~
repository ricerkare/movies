### Are Actor X's movies getting better over time?
# This was inspired by seeing Tom Cruise do particularly well in 
# Edge of Tomorrow and (supposedly) Mission: Impossible - Fallout.
import matplotlib.pyplot as plt
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os

# Setup
chromedriver_path = '/usr/lib/chromium-browser/chromedriver' # Path to chromedriver (in this case, chromium-chromedriver)
# chromedriver_path = os.path.expanduser('~') + '/chromedriver/chromedriver' # Anohter possible path; if so, uncomment and comment line above
browser = webdriver.Chrome(chromedriver_path)
find_xpath = browser.find_element_by_xpath
find_css = browser.find_element_by_css_selector

### Hyperparameters (you set these)
baseline = 'https://www.imdb.com/name/nm0001016/' 	# Tom Cruise's webpage (example)
rolling_num = 5

# Get the URLS for every movie they were in
# This is a fairly messy way of doing it (dependency-wise) but it works
browser.get(baseline)
num_movies = int(find_xpath('//*[@id="filmo-head-actor"]').text.split(' ')[2][1:])
actor_name = find_xpath('//*[@id="overview-top"]/h1/span').text
data_and_links = find_xpath('//*[@id="filmography"]/div[2]')
movie_divs = [data_and_links.find_element_by_xpath('div[' + str(n) + ']') for n in range(1, num_movies + 1)]
movie_urls = [BeautifulSoup(x.get_attribute('outerHTML'), 'html.parser').a.attrs['href'] for x in movie_divs if not ('(announced)' in x.text or '(filming)' in x.text or '(Coming Soon)' in x.text)]

# Now if top billed on linked movie, then get IMDB rating
# (You can remove this condition by changing leading to False)
primary_dataset = []
only_leading = False

for movie in movie_urls:
    browser.get('https://www.imdb.com' + movie)
    check = True	# If check_leading is False, check always returns True (i.e. no check is done)
    if only_leading:
        top_actor = find_xpath('//*[@id="titleCast"]/table/tbody/tr[2]')
        check = (' '.join(top_actor.text.split(' ')[:2]) == actor_name)
    if check:
        top_card_info = find_xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div').text.split('\n')
        is_movie = ('TV' not in top_card_info[-1])
        if is_movie and ('Coming Soon' not in top_card_info):
            # top_card_info has one of two formats (excluding 'Coming Soon' cases):
            # either [rating, number of individual ratings, 'Rate this', movie title, a bunch of info separated by |]
            # ... or [rating, number of ratings, 'Rate this', movie title, original movie title, info separated by |]
            # TODO: Ignore movies without ratings
            top_card_info = [t for t in top_card_info if 'original title' not in t]
            print(top_card_info)
            movie_title = top_card_info[3].split('(')[0]
            movie_year	= top_card_info[3].split('(')[1].split(')')[0]
            movie_rating = float(top_card_info[0].split('/')[0])
            primary_dataset.append([movie_title, movie_year, movie_rating])

# Rolling mean is meaningless until you have at least len(dataset)=length, so this computes it that way, then graphs it.
def rolling_mean(dataset,length):
    mean = lambda x: sum(x)/len(x)
    return [mean(dataset[i:i+length]) for i,x in enumerate(dataset[length-1:])]

plt.scatter([x[1] for x in primary_dataset][::-1],[x[2] for x in primary_dataset][::-1])
rolling_avg_num = 5
plt.plot([x[1] for x in primary_dataset][::-1][rolling_avg_num-1:],rolling_mean([x[2] for x in primary_dataset][::-1],rolling_avg_num))
plt.rcParams['figure.figsize'] = (20,10)
plt.ylim(0,10)
plt.title(actor_name + '\'s IMDB ratings over the years')
role_type = 'leading role' if only_leading else 'role'
plt.ylabel('IMDB score in movie where ' + actor_name + ' had a ' + role_type)
plt.xlabel('Year movie released')
plt.savefig('_'.join([name.lower() for name in actor_name.split(' ')]) + ('_leading_role_stats.png' if only_leading else '_stats.png'), bbox_inches='tight')
plt.show()
