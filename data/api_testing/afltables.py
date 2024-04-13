import bs4 as bs
import requests

def get_html(url):
  response = requests.get(url)
  return response.text

soup = bs.BeautifulSoup(get_html('https://afltables.com/afl/stats/teams/adelaide/2023_gbg.html'), 'html.parser')


# soup.body.center.table.thead.tr      this gets the stat header (eg. Kicks, Handballs, Marks, Tackles, etc.)
# soup.body.center.table.tbody          this gets the stats for each player
tables = soup.find("div", {"class": "simpleTabs"})
# print(f'tables: {tables.get_text()}')
headings = (tables.find("ul", {"class": "simpleTabsNavigation"})).find_all("li")
headings_list = []

for i in range(len(headings)-1):
  headings_list.append(headings[i].a.text)

print(f'headings_list: {headings_list}')

data = tables.find_all("div", {"class": "simpleTabsContent"})

# gets the header row containg all rounds. data[0] just using first table as it is all the same
# there are two table rows (tr) in the thead. The second one contains the round numbers so we go 
# find_all("tr") and then the second element [1]
rounds = data[0].table.thead.find_all("tr")[1].find_all("th")       

num_rounds = rounds[-2].text.replace('R', '')
print(f'num_rounds: {num_rounds}')

bye_rounds = []
round_counter = 1
for round in rounds[1:-1]:
  current_round = int(round.text.replace('R', ''))
  if current_round == round_counter:
    round_counter += 1
  else:
    bye_rounds.append(round_counter)
    round_counter += 2

print(f'bye_round(s): {bye_rounds}')