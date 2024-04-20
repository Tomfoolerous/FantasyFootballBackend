import requests
import bs4 as bs
from pprint import pprint


def get_html(url):
  response = requests.get(url)
  return response.text


def get_cost(player_name):
  soup = bs.BeautifulSoup(get_html('https://www.footywire.com/afl/footy/dream_team_prices'), 'html.parser')
  outer_table = soup.body.find('div').table.find_all('tr')
  print(str(outer_table[6])[:2000])


get_cost('David Mackay')

#path to table:
# soup.body