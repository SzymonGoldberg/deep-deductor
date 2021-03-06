import random
from pyker.cardValidator import CardValidator as CardVal
from pyker.agents.base import Agent
from pyker.betQueue import Move
from pyker.moveValidator import MoveValidator
import tensorflow as tf

def deprecated_model_build():
    for n in range(3):
        features = joblib.load('ann_raw_features.joblib')
        labels = joblib.load('ann_raw_labels.joblib')
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        features_tf = tf.convert_to_tensor(features[n])
        labels_tf = tf.convert_to_tensor(labels[n])
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(features_tf, labels_tf, epochs=5, batch_size=16)
        model.save('ann_models/ann'+str(n))


print('creating neural networks models')
ann = []
for n in range(3):
    ann.append(tf.keras.models.load_model('ann_models/ann'+str(n)))

def countCalls(player, actions):
    return sum(1 for x in actions if x[0] == player and x[1] in [Move.CALL, Move.CHECK]) / 1.0

def countBets(player, actions):
    return sum(1 for x in actions if x[0] == player and x[1] in [Move.RAISE, Move.BET]) / 1.0

class AnnBot(Agent):
    def showdown(self, winners: list, all: list):
        pass

    def bet(self, communityData, playerPot: int):
        #predefined pre-flop behavior - try to go into flop with low cost
        moves = MoveValidator.availableAndLegalMoves(communityData, playerPot, self.balance)
        if len(communityData.actions) == 1:
            if Move.CALL in moves: return Move.CALL
            elif Move.CHECK in moves: return Move.CHECK
            elif Move.BLIND in moves: return Move.BLIND
            return Move.QUIT

        playerList = set(x[0] for x in communityData.actions[-1] if x[0] != self.name)
        commVal = list(map(lambda x: CardVal.checkHighCard([x]) / 1.0, communityData.communityCards))
        predStr = []
        for idx, player in enumerate(playerList):
            ans = tf.convert_to_tensor(tuple(
                [[*commVal[:3+len(communityData.actions)-2],
                countCalls(player, communityData.actions[-1]),
                countBets(player, communityData.actions[-1]),
                idx/1.0,
                len(playerList)/1.0]]))
            predStr.append(ann[len(communityData.actions)-2].predict(ans))
        if len(predStr) > 0 and\
           max(predStr) > CardVal.combination(communityData.communityCards + self.hand):
            return Move.FOLD
        if random.choice([True, False]):
            if Move.BET in moves: return Move.BET
            elif Move.RAISE in moves: return Move.RAISE
        else:
            if Move.CALL in moves: return Move.CALL
            elif Move.CHECK in moves: return Move.CHECK
        
        if Move.CHECK in moves: return Move.CHECK
        return Move.FOLD if Move.FOLD in moves else Move.QUIT
