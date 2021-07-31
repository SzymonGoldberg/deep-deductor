from .betQueue import BetQueue, BetEnded, LastPlayerLeft
from pyker.cardValidator import CardValidator
from .playerWrapper import PlayerWrapper

class Game:
    def __init__(self, agents :list, deck, limit :int) -> None:
        assert(12 > len(agents) > 1 and limit > 1)
        self.deck = deck
        self.limit = limit
        self.betQueue = BetQueue(limit, [PlayerWrapper(*n) for n in enumerate(agents)])

    def __drawCommunityCards(self, numOfCards :int) -> None:
        self.betQueue.extendCommCards(self.deck.draw(numOfCards))

    def __prepareNextRound(self) -> None:
        self.deck.reset()
        self.betQueue.reset(self.limit)

    def __dealCards(self) -> None:
        for player in self.betQueue.getNonFoldingPlayers():
            player.agent.hand.extend(self.deck.draw(2))

    def __showdown(self) -> None:
        maxList, max, players = [], 0, self.betQueue.getNonFoldingPlayers()
        for player in players:
            temp = CardValidator.combination(player.getHand() + self.betQueue.getCommCards())
            if temp > max:
                maxList = [player]
                max = temp
            elif temp == max:
                maxList.append(player)
        prize = self.betQueue.getBankroll() // len(maxList)
        print('--- winners ---')
        for player in players:
            if player in maxList:
                player.incrBalance(prize)
                print(player, ' prize = ', prize)

    def __raiseLimit(self) -> None:
        self.betQueue.communityData.limit *= 2

    def bets(self) -> None:
        try:
            self.betQueue.blindLoop()       #blinds
            self.__dealCards()
            self.betQueue.betLoop()         #pre-flop
            self.__drawCommunityCards(3)
            self.betQueue.betLoop()         #flop
            self.__drawCommunityCards(1)
            self.__raiseLimit()
            self.betQueue.betLoop()         #river
            self.__drawCommunityCards(1)
            self.betQueue.betLoop()         #turn
        except BetEnded: pass

    def start(self):
        try:
            while True:
                self.bets()
                self.__showdown()
                self.__prepareNextRound()
        except LastPlayerLeft:
            return (self.betQueue.waiting + self.betQueue.after + self.betQueue.fold)[0]