import bs4 as bs
import requests
from pprint import pprint
import json

def get_html(url):
  response = requests.get(url)
  return response.text


def season_data(tables):
  headings = (tables.find("ul", {"class": "simpleTabsNavigation"})).find_all("li")
  headings_list = []

  for i in range(len(headings)-1):
    headings_list.append(headings[i].a.text)
  
  if 'BR' in headings_list:
    headings_list.remove('BR')
  if 'SU' in headings_list:
    headings_list.remove('SU')


  data = tables.find_all("div", {"class": "simpleTabsContent"})

  # gets the header row containg all rounds. data[0] just using first table as it is all the same
  # there are two table rows (tr) in the thead. The second one contains the round numbers so we go 
  # find_all("tr") and then the second element [1]
  rounds = data[0].table.thead.find_all("tr")[1].find_all("th")       


  num_rounds = rounds[-2].text.replace('R', '')
  decrement = -2
  while True:
    if num_rounds.isdigit():
      break
    else:
      decrement -= 1
      num_rounds = rounds[-2 + decrement].text.replace('R', '')
  
  bye_rounds = []
  round_counter = 1
  for round in rounds[1:-1]:
    # print(round.text)
    try:
      current_round = int(round.text.replace('R', ''))
    except ValueError:
      if round.text == 'QF' or round.text == 'SF' or round.text == 'EF' or round.text == 'PF' or round.text == 'GF':
        continue
      else:
        raise ValueError(f'Round not valid: {round.text}')
    if current_round == round_counter:
      round_counter += 1
    else:
      bye_rounds.append(round_counter)
      round_counter += 2

  rounds_list = []
  for i in range(1, int(num_rounds) + 1 ):
    if i in bye_rounds:
      rounds_list.append('BYE')
    else:
      rounds_list.append(i)

  return rounds_list, bye_rounds, num_rounds


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


def get_player_data(tables, bye_rounds, year, num_rounds, final_data):    
  #returns data as lists of each data point which needs to be decoded into lists of each player

  temp_player_data = []
  
  data = tables.find_all("div", {"class": "simpleTabsContent"})
  data = data[0:-1]

  #removing brownlow votes table as it is not available for the current year
  for i in data:
    if i.table.thead.tr.th.text == 'Brownlow Votes':
      data.remove(i)

  # you can use data[n] to get the nth table of data 
  for i in data:        # -1 to remove the last table which is the subs
    table_data = i.table.tbody
    table_key = i.table.thead.tr.th.text

    for row in table_data.find_all("tr"):
      round_counter = 0
      for cell in row.find_all("td")[0:-1]:     # -1 to remove the last cell which is the total
        round_counter += 1
        
        if round_counter in bye_rounds:
          if round_counter == 1:                    
          # if it is the first round then the player name needs to be added to the list first and then the bye round
            temp_player_data.append(cell.text)
            temp_player_data.append(None)
            continue                            #there it continues as there is no need to add the player_name later
          else:
            temp_player_data.append(None)
            round_counter += 1

        if cell.text == '\xa0':
          temp_player_data.append(None)
          continue
        elif cell.text == '-':
          temp_player_data.append(0)
          continue

        temp_player_data.append(cell.text)
        # print(temp_player_data)
      
      # print(f'{table_key}: {temp_player_data} \n\n')
      final_data[year][key_to_shorthand(table_key)][temp_player_data[0]] = temp_player_data[1:]
      temp_player_data.clear()
  
  final_data[year]["number_rounds"] = num_rounds
  # pprint(final_data)   

  return final_data


def format_data(unformatted_data):
  max_rounds = 24
  data = []

  player_list = []
  for i in unformatted_data["2024"]["DI"]:
    player_list.append(i)

  for player in player_list:
    player_element = []

    name_element = []
    name_element.append(player)
    for i in range(22):
      name_element.append(None)
    
    player_element.append(name_element)

    for year in unformatted_data.keys():
      round_counter = 1

      while round_counter <= max_rounds:
        match_element = []
        match_element.append(f'{year}_{round_counter}')

        for table_key in unformatted_data[year].keys():
          if table_key == "number_rounds":
            continue
          if player in unformatted_data[year][table_key]:
            try:
              match_element.append(unformatted_data[year][table_key][player][round_counter-1])
            except IndexError:
              match_element.append(None)
          else:
            match_element.append(None)

        player_element.append(match_element)
        round_counter += 1
        
    data.append(player_element)
  
  with open('generated/formatted_data.txt', 'w') as f:
    f.write(str(data))


    
      




        

unformatted_data = {
  "2024": {
    "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
  },
  "2023": {
    "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
  },
  "2022": {
    "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
  },
  "2021": {
    "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
  },
  "2020": {
    "DI": {}, "KI": {}, "MK": {}, "HB": {}, "GL": {}, "BH": {}, "HO": {}, "TK": {}, "RB": {}, "I5": {}, "CL": {}, "CG": {}, "FF": {}, "FA": {}, "CP": {}, "UP": {}, "CM": {}, "MI": {}, "OP": {}, "BO": {}, "GA": {}, "%P": {}
  }
}

years = ['2024', '2023', '2022', '2021', '2020']


teams = ['adelaide', 'brisbanel', 'carlton', 'collingwood', 'essendon','fremantle', 'geelong', 
          'goldcoast', 'gws', 'hawthorn', 'melbourne', 'kangaroos', 'padelaide', 'richmond', 
          'stkilda', 'swans', 'westcoast', 'bullldogs']    
         #bullldogs with 3 ls is not a typo by me. The person who made afltables.com made a typo in the url

for team in teams:
  print(team)
  for year in years:
    print(year)
    soup = bs.BeautifulSoup(get_html(f'https://afltables.com/afl/stats/teams/{team}/{year}_gbg.html'), 'html.parser')

    if not soup:
      print('could not get html')
      exit()

    tables = soup.find("div", {"class": "simpleTabs"})

    rounds, bye_rounds, num_rounds = season_data(tables)

    unformatted_data = get_player_data(tables, bye_rounds, year, num_rounds, unformatted_data)
    # pprint(unformatted_data)

with open('generated/unformatted_data.json', 'w') as f:
  json.dump(unformatted_data, f, indent=2)

format_data(unformatted_data)

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