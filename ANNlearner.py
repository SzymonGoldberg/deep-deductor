import imp
import json
import joblib
from pyker.cards import Card
from pyker.cardValidator import CardValidator
import tensorflow as tf
import numpy as np
#   networks data
#       flop
#           card1   card2   card3   calls   raises  pos     numOfPlayers
#       river
#           card1   card2   card3   card4   calls   raises  pos     numOfPlayers
#       turn
#           card1   card2   card3   card4   card5   calls   raises  pos     numOfPlayers
'''
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
        communityCardsValues = list(map(lambda x: CardValidator.checkHighCard([x]) / 1.0, comm))
        for players in info['players']:
            if len(players['pocket_cards']) == 2:
                playerHand = stringsToCards(players['pocket_cards'])
                for idx, stage in enumerate(players['bets'][1:]):
                    raising = countActions(stage['actions'], ['b', 'r'])
                    calling = countActions(stage['actions'], ['c', 'k'])
                    features[idx].append(np.array(communityCardsValues[:3 + idx] + [calling, raising, players['pos'] / 1.0, info['num_players']/1.0]))
                    labels[idx].append([CardValidator.combination(playerHand+comm[:3 + idx]) / 1.0])
                    print('features -> ', features[idx][-1], '\tlabels -> ', labels[idx][-1])
        line = f.readline()
'''


features = joblib.load('ann_raw_features.joblib')
labels = joblib.load('ann_raw_labels.joblib')

print('creating neural networks models')
ann = []
for n in range(3):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    dataset_tf = tf.data.Dataset.from_tensor_slices(tuple([features[n], labels[n]])).batch(32)
    model.fit(dataset_tf, epochs=5, batch_size=32)
    ann.append(model)