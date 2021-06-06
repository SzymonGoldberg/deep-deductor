from pyker.roundData import Move
from pyker.agents.base import Agent
from pyker.cardValidator import CardValidator

class FormulaBasedPotOddAgent(Agent):
    cardValidator = CardValidator()
    def bet(self, moves, roundData):
        if roundData.stage == 0:
            if Move.CALL in moves: return Move.CALL
            elif Move.CHECK in moves: return Move.CHECK
            elif Move.BLIND in moves: return Move.BLIND
            return Move.QUIT

        handValue = self.cardValidator.combination(self.hand + roundData.communityCards)
        ihr = (handValue)/10_143
        potOdd = roundData.localLimit / roundData.bankroll + roundData.localLimit

        print('-------------formula based------------\nhands: ')
        [print(x.asString()) for x in self.hand]
        print('ihr > ', ihr)
        print('potodd > ', potOdd)

        if ihr > 0.35:
            if Move.BET in moves: return Move.BET
            elif Move.RAISE in moves: return Move.RAISE

        if ihr > 0.25:
            if Move.CALL in moves: return Move.CALL
            elif Move.CHECK in moves: return Move.CHECK
        
        return Move.FOLD if Move.FOLD in moves else Move.QUIT