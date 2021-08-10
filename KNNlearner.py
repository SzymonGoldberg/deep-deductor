import json

with open('/home/szymon/inne/ips/PokerHandsDataset/hands_valid.json','r') as f:
    line = f.readline()
    hand = json.loads(line)
    for players in hand['players']:
        print(players)