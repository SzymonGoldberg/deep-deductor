from pyker.agents.base import Agent
from .cards import *
from operator import attrgetter

class CardValidator:
    @classmethod
    def showdown(self, players, commCards):
    #check for maximum values in all cards
        pointsList  = [[x, self.combination(x.agent.hand + commCards)]for x in players]
        maxPoints   = max(pointsList, key=lambda x : x[1])[1]
    #check for best kicker
        maxPlayers  = [[x, self.combination(x.agent.hand)]for x, y in pointsList if y == maxPoints]
        maxPoints   = max(maxPlayers, key=lambda x : x[1])[1]
        return [x for x, y in maxPlayers if y == maxPoints]

    @classmethod
    def combination(self, cards):
        funcList = [
            self.checkForStraightFlush,
            self.checkForFourOfKind,
            self.CheckForFullHouse,
            self.checkForFlush,
            self.checkForStraight,
            self.checkForThreeOfKind,
            self.checkForPairs,
            self.checkHighCard]
        return max([x(cards) for x in funcList])
    @classmethod
    def groupCardsIf(self, cards, ifStatement, appendStatement):
        groups = []
        for cardIter in cards:
            counter = 0
            group = []
            for card in cards:
                if ifStatement(cardIter, card, counter):
                    counter += 1
                    group.append(card)
            if appendStatement(counter):
                groups.append(group[-1])

        return groups
    @classmethod
    def checkForStraightFlush(self, cards):
        sortedCards = sorted(cards, key=attrgetter('suit', 'rank'))
        straightFlushes = self.groupCardsIf(
            sortedCards, 
            lambda x, y, z: (x.suit == y.suit and y.rank == (x.rank + z)),
            lambda x: x == 5)
        
        if len(straightFlushes) > 0:
            maxstr = max(straightFlushes)
            return 10_000 + maxstr.rank * 10 + maxstr.suit
        return False
    @classmethod
    def checkForFourOfKind(self, cards):
        sortedCards = sorted(cards, key=attrgetter('suit', 'rank'))
        fours = self.groupCardsIf(
            sortedCards,
            lambda x, y, z: (x.rank == y.rank),
            lambda x: x == 4)

        if len(fours) > 0:
            maxFour = max(fours)
            return 9_000 + maxFour.rank * 10 + maxFour.suit

        return False
    @classmethod
    def findAllThree(self, cards):
        threes = self.groupCardsIf(
            cards,
            lambda x, y, z: (x.rank == y.rank),
            lambda x: x >= 3)
        return list(set(threes))
    @classmethod
    def findAllPairs(self, cards):
        pairs = self.groupCardsIf(
            cards, 
            lambda x, y, z: (x.rank == y.rank),
            lambda x: x >= 2)
        return list(set(pairs))        
    @classmethod
    def CheckForFullHouse(self, cards):
        threes = self.findAllThree(cards)
        if len(threes) == 0: return False
        maxThree = max(threes)
        
        pairs = self.findAllPairs(cards)
        pairs = list(set([x for x in pairs if x.rank != maxThree.rank]))

        if len(pairs) == 0: return False

        maxPair = max(pairs)
        return 8_000 + maxThree.rank * 10 + maxPair.rank

    @classmethod
    def checkForFlush(self, cards):
        sortedCards = sorted(cards, key=attrgetter('suit', 'rank'))
        straightFlushes = self.groupCardsIf(
            sortedCards,
            lambda x, y, z: (x.suit == y.suit),
            lambda x: x == 5)
        
        if len(straightFlushes) > 0:
            maxstr = max(straightFlushes)
            return 7_000 + maxstr.rank * 10 + maxstr.suit
        return False
    @classmethod
    def checkForStraight(self, cards):
        sortedCards = sorted(cards, key=attrgetter('rank', 'suit'))
        straightHands = self.groupCardsIf(
            sortedCards,
            lambda x, y, z: (y.rank == x.rank + z),
            lambda x: x == 5)

        if len(straightHands) > 0:
            maxstr = max(straightHands)
            return 6_000 + maxstr.rank * 10 + maxstr.suit
        return False
    @classmethod
    def checkForThreeOfKind(self,cards):
        threes = self.findAllThree(cards)
        if len(threes) > 0:
            return 5_000 + max(threes).rank * 10
        return False
    @classmethod
    def checkForPairs(self,cards):
        pairs = self.findAllPairs(cards)
        if len(pairs) == 0: return False

        maxPair1 = max(pairs)
        pairs.remove(maxPair1)
        if len(pairs) == 0: 
            return 3_000 + maxPair1.rank * 10 + maxPair1.suit
        
        maxPair2 = max(pairs)
        return 4_000 + maxPair1.rank * 10 + maxPair2.rank
    @classmethod
    def checkHighCard(self, cards):
        highestCard = max(cards, key= attrgetter('rank', 'suit'))
        return 2_000 + highestCard.rank * 10 + highestCard.suit