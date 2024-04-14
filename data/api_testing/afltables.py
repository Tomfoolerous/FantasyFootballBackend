import bs4 as bs
import requests
from pprint import pprint

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

def key_to_shorthand(key):
  if key == 'Disposals':
    return 'DI'
  elif key == 'Kicks':
    return 'KI'
  elif key == 'Marks':
    return 'MK'
  elif key == 'Handballs':
    return 'HB'
  elif key == 'Goals':
    return 'GL'
  elif key == 'Behinds':
    return 'BH'
  elif key == 'Hit Outs':
    return 'HO'
  elif key == 'Tackles':
    return 'TK'
  elif key == 'Rebounds':
    return 'RB'
  elif key == 'Inside 50s':
    return 'I5'
  elif key == 'Clearances':
    return 'CL'
  elif key == 'Clangers':
    return 'CG'
  elif key == 'Frees':
    return 'FF'
  elif key == 'Frees Against':
    return 'FA'
  elif key == 'Brownlow Votes':
    return 'BR'
  elif key == 'Contested Possessions':
    return 'CP'
  elif key == 'Uncontested Possessions':
    return 'UP'
  elif key == 'Contested Marks':
    return 'CM'
  elif key == 'Marks Inside 50':
    return 'MI'
  elif key == 'One Percenters':
    return 'OP'
  elif key == 'Bounces':
    return 'BO'
  elif key == 'Goal Assists':
    return 'GA'
  elif key == '% Played':
    return '%P'
  else: 
    print('Key not found')
    exit()


def get_player_data(tables, bye_rounds, year, num_rounds):    
  #returns data as lists of each data point which needs to be decoded into lists of each player
  final_data = {
    "2024": {
      "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "BR": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
    },
    "2023": {
      "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "BR": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
    },
    "2022": {
      "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "BR": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
    },
    "2021": {
      "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "BR": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
    },
    "2020": {
      "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "BR": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
    }
}

  temp_player_data = []
  
  data = tables.find_all("div", {"class": "simpleTabsContent"})

  # you can use data[x] to get the xth table of 
  for i in data[0:-1]:        # -1 to remove the last table which is the subs
    table_data = i.table.tbody
    table_key = i.table.thead.tr.th.text

    for row in table_data.find_all("tr"):
      round_counter = 0
      for cell in row.find_all("td")[0:-1]:     # -1 to remove the last cell which is the total
        round_counter += 1
        
        if round_counter in bye_rounds:
          temp_player_data.append(None)
          round_counter += 1

        if cell.text == '\xa0':
          temp_player_data.append(None)
          continue
        elif cell.text == '-':
          temp_player_data.append(0)
          continue

        temp_player_data.append(cell.text)
      
      # print(f'{table_key}: {temp_player_data} \n\n')
      final_data[year][key_to_shorthand(table_key)][temp_player_data[0]] = temp_player_data[1:]
      temp_player_data = []
  
  final_data[year]["number_rounds"] = num_rounds
  # print(final_data['2023'])
  



tables = soup.find("div", {"class": "simpleTabs"})

rounds, bye_rounds = season_data(tables)

unformatted_data = get_player_data(tables, bye_rounds, year, num_rounds)

'''
unformatted data:

unformatted_data = {          #eg. key = DI, name = David Mackay, year = 2023, round = 1
  "key": {
    "year": {
      "name": {
        "round": [data]
      }
    }
  }
}

format for data:

data = [
  [[name, position, cost, None, None...], [match_id, stats...], [match_id, stats...], [match_id, stats...]... ], 
  [[name, position, cost, None, None...], [match_id, stats...], [match_id, stats...], [match_id, stats...]... ], 
  ... 
]
'''