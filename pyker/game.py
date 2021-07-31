from .roundData import BetQueue, BetEnded, LastPlayerLeft
from pyker.cardValidator import CardValidator
from .seat import PlayerWrapper

class Game:
    def __init__(self, agents :list, deck, limit :int) -> None:
        assert(12 > len(agents) > 1 and limit > 1)
        self.deck = deck
        self.limit = limit
        self.betQueue = BetQueue(self.limit, [PlayerWrapper(*n) for n in enumerate(agents)])

    def drawCommunityCards(self, numOfCards :int) -> None:
        self.betQueue.extendCommCards(self.deck.draw(numOfCards))

    def roundReset(self) -> None:
        self.deck.reset()
        self.betQueue.reset(self.limit)

    def dealCards(self) -> None:
        for player in self.betQueue.getPlayers():
            player.agent.hand.extend(self.deck.draw(2))

    def showdown(self) -> None:
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

    def raiseLimit(self) -> None:
        self.betQueue.communityData.limit *= 2

    def bets(self) -> None:
        try:
        #blinds
            self.betQueue.blindLoop()
            self.dealCards()
        #pre-flop
            self.betQueue.betLoop()
            self.drawCommunityCards(3)
        #flop
            self.betQueue.betLoop()
            self.drawCommunityCards(1)
            self.raiseLimit()
        #river
            self.betQueue.betLoop()
            self.drawCommunityCards(1)
        #turn
            self.betQueue.betLoop()
        except BetEnded: pass

    def start(self):
        try:
            while True:
                self.bets()
                self.showdown()
                self.roundReset()
        except LastPlayerLeft:
            return self.betQueue.getPlayers()[0]