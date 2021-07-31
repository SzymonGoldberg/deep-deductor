from enum import IntEnum
import itertools as it

class BetEnded(Exception): pass
class LastPlayerLeft(Exception): pass

class Move(IntEnum):
    BLIND = 0
    FOLD = 2
    CHECK = 3
    BET = 4
    CALL = 5
    RAISE = 6
    QUIT = 7

class CommunityData:
    def __init__(self, limit :int) -> None:
        self.communityCards = []
        self.limit = limit
        self.actions = [[]]
        self.maxPot = 0
    
    def getNumOfBlinds(self) -> int:   #tuple 'cause its faster than list()
        return len(tuple(filter(lambda x: x[1] == Move.BLIND, self.actions[0])))

class BetQueue:
    def __init__(self, limit :int, players :list) -> None:
        self.initAfterFoldAndCommData(limit)
        self.waiting = players  #players who do not bet yet

    def initAfterFoldAndCommData(self, limit):
        self.communityData = CommunityData(limit)
        self.after = []     #players who are after their bets
        self.fold = []      #playesr who folded

    def reset(self, limit :int):
        self.waiting.extend(self.after + self.fold)
        self.initAfterFoldAndCommData(limit)
        for player in self.waiting:
            player.dealerIdx -= 1
            if player.dealerIdx < 0:
                player.dealerIdx = len(self.waiting) - 1
            player.clearHandAndPot()

        self.waiting.sort(key=lambda x: x.dealerIdx)

    def blindLoop(self) -> None:
        self.loop(lambda x, y : y.getNumOfBlinds() < 2)

    def betLoop(self) -> None:
        self.loop(lambda x, y: len(x) > 0)

        self.waiting.extend(self.after)
        self.after.clear()
        self.waiting.sort(key=lambda x: x.dealerIdx)
        self.communityData.actions.append([])

    def extendCommCards(self, cards):
        self.communityData.communityCards.extend(cards)

    def getCommCards(self):
        return self.communityData.communityCards

    def getBankroll(self):
        return sum(map(lambda x: x[2], list(it.chain(*self.communityData.actions))))

    def getPlayers(self) -> list:
        return self.waiting + self.after + self.fold

    def getNonFoldingPlayers(self) -> list:
        return self.waiting + self.after

    def getNumOfInGamePlayers(self) -> int:
        return len(self.after) + len(self.waiting)

    def getNumOfPlayers(self) -> int:
        return len(self.after) + len(self.waiting) + len(self.fold)

    def loop(self, statement) -> None:
        while statement(self.waiting, self.communityData):
            player = self.waiting.pop(0)
            move = player.bet(self.communityData)
            
            if move in [Move.RAISE, Move.BET, Move.BLIND]: #raising moves
                self.waiting.extend(self.after)
                self.after = [player]
                self.communityData.maxPot = player.inPot
            elif move == Move.FOLD:
                self.fold.append(player)
            elif move != Move.QUIT:
                self.after.append(player)
   
            if self.getNumOfPlayers() < 2:      raise LastPlayerLeft()
            if self.getNumOfInGamePlayers() < 2:raise BetEnded()