import json

def get_cached_data():
  with open ('generated/formatted_data.json', 'r') as f:
    formatted_data = json.load(f)["a"]
  
  return formatted_data

