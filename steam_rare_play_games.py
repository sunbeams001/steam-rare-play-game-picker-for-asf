import requests
import json
import time

steam_key = '$steam_key$' # a steam web api key, can get one from here -> https://steamcommunity.com/dev/apikey
steam_user_id = '$steam_user_id$' # your steam user id
config_file_path = "$config_file_path$" # your ASF config file.
max_hours = 7  # max farming time in hours
blacklist_appids = [] # not idle this games.
idle_appids = [] # idle this games when all other games are beyond max_hours [570,440] dota2, tf2 and etc.

res = requests.get(
    'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&include_played_free_games=1&format=json'.format(steam_key,
                                                                                                             steam_user_id))
if res.status_code != 200:
    print 'request error'
    exit(0)

data = res.json()['response']['games']
data = [d for d in data if d[u'playtime_forever'] < max_hours * 60 and d[u'appid'] not in blacklist_appids]

rare_games = sorted(data, key=lambda i: i[u'playtime_forever'])[:32]
rare_game_ids = [r[u'appid'] for r in rare_games]
rare_game_ids = (rare_game_ids + idle_appids)[:32]

print len(rare_game_ids)
print rare_game_ids

with open(config_file_path, 'r+') as f:
    # file_data = f.read()
    file_json = json.load(f)
    f.seek(0)
    file_json['GamesPlayedWhileIdle'] = rare_game_ids
    # print file_json
    json.dump(file_json, f, indent=2, sort_keys=lambda x: x)
    f.truncate()

print 'the end.'
time.sleep(1)
