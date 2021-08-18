from pyker.betQueue import CommunityData
from .moveValidator import MoveValidator as mv

class NotEnoughCashException(Exception): pass
class IllegalMoveException(Exception): pass

class PlayerWrapper:
    """This class is wrapper around player class, used to make bets and saving 
    data easier, its contains amount of cash inserted into pot by player and 
    distance from dealer in dealeridx"""

    def __init__(self, dealerIndex :int, agent, balance :int) -> None:
        self.agent = agent
        self.inPot = 0
        self.dealerIdx = dealerIndex
        self.agent.balance = balance

    def bet(self, communityData :CommunityData):
        move = self.agent.bet(communityData, self.inPot)
        amount = mv.moveToCash(communityData, self.inPot, move)
        if amount > self.agent.balance: 
            raise NotEnoughCashException()
        if not move in mv.legalMoves(communityData, self.inPot):
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