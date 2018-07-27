### Are Actor X's movies getting better over time?
# This was inspired by seeing Tom Cruise do particularly well in 
# Edge of Tomorrow and (supposedly) Mission: Impossible - Fallout.
import matplotlib.pyplot as plt
from selenium import webdriver
import time
from bs4 import BeautifulSoup

# Setup
browser = webdriver.Chrome('/home/order/Videos/chromedriver/chromedriver')
find_xpath = browser.find_element_by_xpath
find_css = browser.find_element_by_css_selector

### Hyperparameters (you set these)
baseline = 'https://www.imdb.com/name/nm0000129/?ref_=tt_cl_t1' # Tom Cruise's webpage
rolling_num = 5

# Get the URLS for every movie they were in
# This is a fairly messy way of doing it (dependency-wise) but it works
browser.get(baseline)
num_movies = int(find_xpath('//*[@id="filmo-head-actor"]').text.split(' ')[2][1:])
actor_name = find_xpath('//*[@id="overview-top"]/h1/span').text
data_and_links = find_xpath('//*[@id="filmography"]/div[2]')
movie_divs = [data_and_links.find_element_by_xpath('div[' + str(n) + ']') for n in range(1,num_movies+1)]
movie_urls = [BeautifulSoup(x.get_attribute('outerHTML'), 'html.parser').a.attrs['href'] for x in movie_divs if '(announced)' not in x.text and '(filming)' not in x.text]
# Now if top billed on linked movie, then get IMDB rating
# (You can remove this condition simply by commenting out the if statement and de-indenting)
primary_dataset = []
for movie in movie_urls:
    browser.get('https://www.imdb.com' + movie)
    top_actor = find_xpath('//*[@id="titleCast"]/table/tbody/tr[2]')
    if ' '.join(top_actor.text.split(' ')[:2]) == actor_name:
        top_card_info = find_xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div').text.split('\n')
        primary_dataset.append([top_card_info[3].split('(')[0],top_card_info[3].split('(')[1][:-1],float(top_card_info[0].split('/')[0])])
print(primary_dataset)

# Rolling mean is meaningless until you have at least len(dataset)=length, so this computes it that way, then graphs it.
def rolling_mean(dataset,length):
    mean = lambda x: sum(x)/len(x)
    return [mean(dataset[i:i+length]) for i,x in enumerate(dataset[length-1:])]

plt.scatter([x[1] for x in primary_dataset][::-1],[x[2] for x in primary_dataset][::-1])
rolling_avg_num = 5
plt.plot([x[1] for x in primary_dataset][::-1][rolling_avg_num-1:],rolling_mean([x[2] for x in primary_dataset][::-1],rolling_avg_num))
plt.rcParams['figure.figsize'] = (20,10)
plt.ylim(0,10)
plt.title('Tom Cruise is a surprisingly consistent actor')
plt.ylabel('IMDB score in movie where Tom Cruise had a leading role')
plt.xlabel('Year movie released')
# plt.savefig('tom_cruise_consistency.png',bbox_inches='tight')
plt.show()
