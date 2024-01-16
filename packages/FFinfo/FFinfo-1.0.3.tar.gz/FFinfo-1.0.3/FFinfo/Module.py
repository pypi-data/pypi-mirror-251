import requests
import subprocess
import json

def get_data(player_id):
    regions_to_check = ["BR", "LATAM", "IND", "ID", "PK", "SG", "TW", "ME", "TH", "RU"]
    for region in regions_to_check:
        base_url = "http://freefireapi.com.br/api/search_id"
        params = {"id": player_id, "region": region}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            player_info = response.json()
            json_data = json.dumps(player_info)
            return json_data
            break
