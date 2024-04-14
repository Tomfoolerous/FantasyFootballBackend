import bs4 as bs
import requests

def get_html(url):
  response = requests.get(url)
  return response.text

team = 'adelaide'
year = '2023'

soup = bs.BeautifulSoup(get_html(f'https://afltables.com/afl/stats/teams/{team}/{year}_gbg.html'), 'html.parser')


def season_data(tables):
  headings = (tables.find("ul", {"class": "simpleTabsNavigation"})).find_all("li")
  headings_list = []

  for i in range(len(headings)-1):
    headings_list.append(headings[i].a.text)

  data = tables.find_all("div", {"class": "simpleTabsContent"})

  # gets the header row containg all rounds. data[0] just using first table as it is all the same
  # there are two table rows (tr) in the thead. The second one contains the round numbers so we go 
  # find_all("tr") and then the second element [1]
  rounds = data[0].table.thead.find_all("tr")[1].find_all("th")       

  num_rounds = rounds[-2].text.replace('R', '')
  
  bye_rounds = []
  round_counter = 1
  for round in rounds[1:-1]:
    current_round = int(round.text.replace('R', ''))
    if current_round == round_counter:
      round_counter += 1
    else:
      bye_rounds.append(round_counter)
      round_counter += 2

  rounds_list = []
  for i in range(1, int(num_rounds) +1 ):
    if i in bye_rounds:
      rounds_list.append('BYE')
    else:
      rounds_list.append(i)

  return rounds_list, bye_rounds



tables = soup.find("div", {"class": "simpleTabs"})

rounds, bye_rounds = season_data(tables)


def get_player_data(tables, bye_rounds):    
  #returns data as lists of each data point which needs to be decoded into lists of each player
  final_data = []
  player_data = []
  temp_player_data = []
  
  data = tables.find_all("div", {"class": "simpleTabsContent"})

  # you can use data[x] to get the xth table of 
  for i in data:
    table_data = i.table.tbody
    table_key = i.table.thead.tr.th.text

    for row in table_data.find_all("tr"):
      round_counter = 0
      for cell in row.find_all("td")[0:-1]:     # -1 to remove the last cell which is the total
        
        if cell.text == '\xa0':
          temp_player_data.append(None)
          continue
        elif cell.text == '-':
          temp_player_data.append(0)
          continue

        temp_player_data.append(cell.text)
      
      print(temp_player_data, '\n')
      temp_player_data.clear()
  


unformatted_data = get_player_data(tables, bye_rounds)

'''
unformatted data:

unformatted_data = {          #eg. key = DI, name = David Mackay, name = Rory Laird, etc.
  "key": {
    "name": [match_id, stat],
    "name": [match_id, stat],
    "name": [match_id, stat],
    ...
  }
  key: {
    "name": [match_id, stat],
    "name": [match_id, stat],
    "name": [match_id, stat],
    ...
}

format for data:

data = [
  [[name, position, cost, None, None...], [match_id, stats...], [match_id, stats...], [match_id, stats...]... ], 
  [[name, position, cost, None, None...], [match_id, stats...], [match_id, stats...], [match_id, stats...]... ], 
  ... 
]
'''