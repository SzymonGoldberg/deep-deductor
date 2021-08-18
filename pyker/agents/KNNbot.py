import random
from pyker.cardValidator import CardValidator as CardVal
from pyker.agents.base import Agent
from pyker.betQueue import Move
from pyker.moveValidator import MoveValidator
import joblib

knn = joblib.load('testKNNmodels.joblib')
print('loaded knn models')

def countCalls(player, actions):
    return sum(1 for x in actions if x[0] == player and x[1] in [Move.CALL, Move.CHECK])

def countBets(player, actions):
    return sum(1 for x in actions if x[0] == player and x[1] in [Move.RAISE, Move.BET])

class KnnBot(Agent):
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

        commVal = CardVal.combination(communityData.communityCards)
        predictedHands = [knn[len(communityData.actions)-2].predict([[
            commVal,
            countBets(player, communityData.actions[-1]),
            countBets(player, communityData.actions[-1])
        ]]) for player in [x[0] for x in communityData.actions[-1]]]
        if len(predictedHands) > 0 and\
           max(predictedHands) > CardVal.combination(communityData.communityCards + self.hand):
            return Move.FOLD

        if random.choice([True, False]):
            if Move.BET in moves: return Move.BET
            elif Move.RAISE in moves: return Move.RAISE
        else:
            if Move.CALL in moves: return Move.CALL
            elif Move.CHECK in moves: return Move.CHECK
        
        return Move.FOLD if Move.FOLD in moves else Move.QUIT
