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
            return json_data, region
            break


def get_stats(player_id, match_mode):
    json_data, region_text = get_data(player_id)
    match_modes = {
    "BR_CAREER": 0,
    "BR_CLASSIC": 1,
    "BR_RANKED": 2
    }
    url = f"https://freefireapi.com.br/api/stats?id={player_id}&match_mode={match_modes[match_mode]}&region={region_text}"
    response = requests.get(url)
    if response.status_code == 200:
        player_info = response.json()
        json_data = json.dumps(player_info)
        return json_data
