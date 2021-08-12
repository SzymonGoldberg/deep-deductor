import json
import joblib
from pyker.cards import Card
from pyker.cardValidator import CardValidator
from sklearn.neighbors import KNeighborsClassifier

def stringsToCards(strList):
    return [Card.fromString(x) for x in strList]

def countActions(l, actions):
    return sum(1 for x in l if x in actions)
    
with open('/home/szymon/inne/ips/PokerHandsDataset/hands_valid.json','r') as f:
    features = ([],[],[])
    labels = ([],[],[])

    line = f.readline()
    while line:
        info = json.loads(line)
        comm = stringsToCards(info['board'])
        communityCardsValues = tuple(map(CardValidator.combination, [comm[:3], comm[:4], comm]))
        for players in info['players']:
            if len(players['pocket_cards']) == 2:
                playerHand = stringsToCards(players['pocket_cards'])
                for idx, stage in enumerate(players['bets'][1:]):
                    raising = countActions(stage['actions'], ['b', 'r'])
                    calling = countActions(stage['actions'], ['c', 'k'])
                    features[idx].append([communityCardsValues[idx], raising, calling])
                    labels[idx].append(CardValidator.combination(playerHand+comm[:3+idx]))
                    print('features -> ', features[idx][-1], '\tlabels -> ', labels[idx][-1])
        line = f.readline()

print("creating knn models")
knn = []
for n in range(3):
    knn.append(KNeighborsClassifier())
    knn[n].fit(features[n], labels[n])
print("saving models")
joblib.dump(knn, 'testKNNmodels.joblib', compress=4)
print('done')