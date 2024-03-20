import json
import requests
import pprint

def teams():
  response = requests.get('https://api.squiggle.com.au/?q=teams')
  print(f'status: {response.status_code}')
  return response.json()

def games():
  response = requests.get('https://api.squiggle.com.au/?q=games')
  printf(f'status: {response.status_code}')
  return response.json

pprint.pprint(teams())