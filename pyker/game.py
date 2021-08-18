from .betQueue import BetQueue, BetEnded, LastPlayerLeft
from pyker.cardValidator import CardValidator
from .playerWrapper import PlayerWrapper

class Poker:
    def __init__(self, agents :list, deck, limit :int, startBalance :int) -> None:
        assert(12 > len(agents) > 1 and limit > 1)
        self.deck = deck
        self.limit = limit
        self.betQueue = BetQueue(limit,[
            PlayerWrapper(*n, startBalance) for n in enumerate(agents)])

    def __drawCommunityCards(self, numOfCards :int) -> None:
        self.betQueue.extendCommCards(self.deck.draw(numOfCards))

    def __prepareNextRound(self) -> None:
        self.deck.reset()
        self.betQueue.reset(self.limit)

    def __dealCards(self) -> None:
        for player in self.betQueue.getNonFoldingPlayers():
            player.agent.hand.extend(self.deck.draw(2))

    def __showdown(self) -> None:
        players = self.betQueue.getNonFoldingPlayers()
        winners = CardValidator.showdown(players, self.betQueue.getCommCards())
        prize   = self.betQueue.getBankroll() // len(winners)
        prizeToSmallBets = prize // (self.betQueue.communityData.limit//2)
        for player in players:
            player.agent.handsPlayed += 1
            if player in winners:
                player.incrBalance(prize)
                player.agent.smallBets += prizeToSmallBets
            else:
                player.agent.smallBets -= prizeToSmallBets
        for player in self.betQueue.allPlayers():
            player.agent.showdown(winners, players)

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
            return self.betQueue.allPlayers()[0]