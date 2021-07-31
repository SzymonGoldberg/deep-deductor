from pyker.roundData import CommunityData
from .cardValidator import CardValidator
from .moveValidator import MoveValidator

class NotEnoughCashException(Exception): pass
class IllegalMoveException(Exception): pass

class PlayerWrapper:
    def __init__(self, dealerIndex :int, agent) -> None:
        self.agent = agent
        self.inPot = 0
        self.dealerIdx = dealerIndex

    def bet(self, communityData :CommunityData):
        move = self.agent.bet(communityData, self.inPot)
        amount = MoveValidator.moveToCash(communityData, self.inPot, move)
        if amount > self.agent.balance: 
            raise NotEnoughCashException
        if not move in MoveValidator.legalMoves(communityData, self.inPot):
            raise IllegalMoveException()

        self.agent.balance -= amount
        self.inPot += amount

        communityData.actions[-1].append((self.agent.name, move, amount))
        return move

    def clearHandAndPot(self):
        self.agent.clearHand()
        self.inPot = 0

    def incrBalance(self, num :int):
        self.agent.balance += num

    def getHand(self):
        return self.agent.hand

    def __repr__(self):
        return self.agent.name