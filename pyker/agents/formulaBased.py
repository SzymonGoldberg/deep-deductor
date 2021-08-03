from pyker.moveValidator import MoveValidator
from pyker.betQueue import Move, CommunityData
from pyker.agents.base import Agent
from pyker.cardValidator import CardValidator

class FormulaBasedAgent(Agent):
    def bet(self, communityData: CommunityData, playerPot: int):
        moves = MoveValidator.legalMoves(communityData, playerPot)
        if len(communityData.actions) == 1:
            if Move.CALL in moves: return Move.CALL
            elif Move.CHECK in moves: return Move.CHECK
            elif Move.BLIND in moves: return Move.BLIND
            return Move.QUIT

        handValue = CardValidator.combination(self.hand + communityData.communityCards)
        ihr = ((handValue * 100)/10_143)/100
        print('---formula based---\nhands: ')
        [print(x.asString()) for x in self.hand]
        print('ihr > ', ihr)
        if ihr > 0.35:
            if Move.BET in moves: return Move.BET
            elif Move.RAISE in moves: return Move.RAISE

        if ihr > 0.25:
            if Move.CALL in moves: return Move.CALL
            elif Move.CHECK in moves: return Move.CHECK
        
        return Move.FOLD if Move.FOLD in moves else Move.QUIT

    def showdown(self, winners: list, all: list):
        pass