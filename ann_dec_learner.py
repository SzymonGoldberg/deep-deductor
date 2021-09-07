import json
import joblib
from pyker.cards import Card
from pyker.cardValidator import CardValidator
import tensorflow as tf
import numpy as np

#   networks data
#       flop
#           hand1   hand2   card1   card2   card3   bestHand
#       river
#           hand1   hand2   card1   card2   card3   card4   bestHand
#       turn
#           hand1   hand2   card1   card2   card3   card4   card5   bestHand

def stringsToCards(strList):
    return [Card.fromString(x) for x in strList]

def countActions(l, actions):
    return sum(1 for x in l if x in actions) / 1.0

with open('/home/szymon/inne/ips/PokerHandsDataset/hands_valid.json','r') as f:
    features = ([],[],[])
    labels = ([],[],[])

    line = f.readline()
    while line:
        info = json.loads(line)
        comm = stringsToCards(info['board'])
        numOfPlayers = [x['num_players'] for x in info['pots'][1:]]
        commPts = list(map(lambda x: CardValidator.checkHighCard([x]) / 1.0, comm))
        points = [[],[],[]]
        winners = []
        for player in info['players']:
            if player['winnings'] > 0:
                winners.append(player['user'])
            for idx in range(3):
                points[idx].append(
                    [player['user'],
                    CardValidator.combination(stringsToCards(player['pocket_cards'])+comm[:3 + idx])/ 1.0])

        for player in info['players']:
            hand = [CardValidator.checkHighCard([x]) for x in stringsToCards(player['pocket_cards'])]
            for idx, stage in enumerate(player['bets'][1:]):
                maxHand = max(x[1] for x in points[idx] if x[0] != player['user'])
                features[idx].append(np.array(hand + commPts[:3 + idx] + [maxHand]))
                labels[idx].append([1.0 if player['user'] in winners else 0.0])
        print(f'feature = {features[idx][-1]}\n   label = {labels[idx][-1]}')
        line = f.readline()

for n in range(3):
    features_tf = tf.convert_to_tensor(features[n])
    labels_tf = tf.convert_to_tensor(labels[n])
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(24, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(features_tf, labels_tf, epochs=5, batch_size=16)
    model.save('ann_dec_models/ann'+str(n))
