import random
from pyker.cardValidator import CardValidator
from pyker.agents.base import Agent
from pyker.betQueue import Move
from pyker.moveValidator import MoveValidator
import joblib


knn = joblib.load('testKNNmodels.joblib')
print('loaded knn models')

class KnnBot(Agent):
    def showdown(self, winners: list, all: list):
        pass

    def bet(self, communityData, playerPot: int):
        #predefined pre-flop behavior - try to go into flop with low cost
        moves = MoveValidator.legalMoves(communityData, playerPot)
        if len(communityData.actions) == 1:
            if Move.CALL in moves: return Move.CALL
            elif Move.CHECK in moves: return Move.CHECK
            elif Move.BLIND in moves: return Move.BLIND
            return Move.QUIT
        cardVal = CardValidator.combination(communityData.communityCards + self.hand)
        commVal = CardValidator.combination(communityData.communityCards)
        predictedHands = []
        for player in [x[0] for x in communityData.actions[-1]]:
            calling = sum(1 for x in communityData.actions[-1] if x[0] == player and x[1] in [Move.CALL, Move.CHECK])
            raising = sum(1 for x in communityData.actions[-1] if x[0] == player and x[1] in [Move.RAISE, Move.BET])
            predictedHands.append(knn[len(communityData.actions)-2].predict([[commVal, raising, calling]]))
        if len(predictedHands)>0 and max(predictedHands) > cardVal:
            return Move.FOLD
        return random.choice([Move.CALL, Move.RAISE] if Move.CALL in moves else [Move.CHECK, Move.BET])