import json
import requests
import os

session = requests.Session()
session.headers.update({"User-Agent": f"FantasyFootballBackend - Contact at {os.getenv('EMAIL')}"})

def teams():
  response = session.get('https://api.squiggle.com.au/?q=teams')
  print(f'status: {response.status_code}')
  return response.json()

def get_games(year):
  response = session.get(f'https://api.squiggle.com.au/?q=games;year={year}')
  print(f'status: {response.status_code}')
  return response.json()

def sort_games(year):
  return_data = []
  games = get_games(year)['games']

  for game in games:
    return_data.append({
      'round': game['round'],
      'unix_time': game['unixtime'],
      'home_team': game['hteamid'],
      'away_team': game['ateamid'],
      'abehinds': game['abehinds'],
      'agoals': game['agoals'],
      'ascore': game['ascore'],
      'hbehinds': game['hbehinds'],
      'hgoals': game['hgoals'],
      'hscore': game['hscore'],
      'venue': game['venue'],
      'is_final': game['is_final'],
      'winner': game['winnerteamid'],
    })
  
  return return_data


def game_data_to_json(year):
  path = f'data/{year}_games.json'  # relative to the root of the project
  with open(path, 'w') as f:        # automatically makes a new file if it doesnt exist
    json.dump(sort_games(year), f, indent=2)

game_data_to_json(2021)