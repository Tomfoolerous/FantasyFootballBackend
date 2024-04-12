import bs4 as bs
import requests

def get_html(url):
  response = requests.get(url)
  return response.text

soup = bs.BeautifulSoup(get_html('https://afltables.com/afl/stats/teams/adelaide/2024_gbg.html'), 'html.parser')


# soup.body.center.table.thead.tr      this gets the stat header (eg. Kicks, Handballs, Marks, Tackles, etc.)
# soup.body.center.table.tbody          this gets the stats for each player
tables = soup.find("div", {"class": "simpleTabs"})
# print(f'tables: {tables.get_text()}')
headings = (tables.find("ul", {"class": "simpleTabsNavigation"})).find_all("li")
headings_list = []

for i in range(len(headings)-1):
  headings_list.append(headings[i].a.text)

print(f'headings_list: {headings_list}')