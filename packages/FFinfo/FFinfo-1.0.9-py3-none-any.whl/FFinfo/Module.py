import requests
import subprocess
import json
import os

api_url = os.environ.get('API_URL')

def get_data(player_id):
    regions_to_check = ["BR", "LATAM", "IND", "ID", "PK", "SG", "TW", "ME", "TH", "RU"]
    for region in regions_to_check:
        base_url = f"{api_url}/search_id"
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
    url = f"{api_url}/stats?id={player_id}&match_mode={match_modes[match_mode]}&region={region_text}"
    response = requests.get(url)
    if response.status_code == 200:
        player_info = response.json()
        json_data = json.dumps(player_info)
        return json_data
        
        
        
def checkUID(uid):
    cookies = {
        'datadome': 'mE1gQN8LTYOt1Kk8oMfKzJhKFQfazhw0kK7k117u1QgpHtfgIWV~ziz6JzJ8IUuzFWzg1MGHyyEz7n_jAiPfDMgKwCK36hG7LGKkMj9VhoXA1A65TsvRrvotuvWQBIBH',
        '_ga_KE3SY7MRSD': 'GS1.1.1705587363.7.1.1705587363.0.0.0',
        '_ga_RF9R6YT614': 'GS1.1.1705587363.7.0.1705587363.0.0.0',
        '_ga': 'GA1.2.2111498544.1703553296',
        '_gid': 'GA1.2.70074869.1705587364',
        '_gat_gtag_UA_207309476_25': '1',
    }
    headers = {
        'authority': 'ff.garena.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': 'datadome=mE1gQN8LTYOt1Kk8oMfKzJhKFQfazhw0kK7k117u1QgpHtfgIWV~ziz6JzJ8IUuzFWzg1MGHyyEz7n_jAiPfDMgKwCK36hG7LGKkMj9VhoXA1A65TsvRrvotuvWQBIBH; _ga_KE3SY7MRSD=GS1.1.1705587363.7.1.1705587363.0.0.0; _ga_RF9R6YT614=GS1.1.1705587363.7.0.1705587363.0.0.0; _ga=GA1.2.2111498544.1703553296; _gid=GA1.2.70074869.1705587364; _gat_gtag_UA_207309476_25=1',
        'referer': 'https://ff.garena.com/en/support/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'B6FksShzIgjfrYImLpTsadjS86sddhFH',
    }
    params = {
        'lang': 'en',
        'uid': uid,
    }
    response = requests.get('https://ff.garena.com/api/antihack/check_banned', params=params, cookies=cookies, headers=headers)
    return response.text
