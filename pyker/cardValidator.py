from .cards import *
from operator import attrgetter
from collections import Counter

class CardValidator:
    def combination(self):
        pass

    def checkForStraightFlush(self, cards):
        sortedCards = sorted(cards, key=attrgetter('suit', 'rank'))
        straightFlushes = []
        for cardIter in sortedCards:
            inRow = 0
            flush = []
            for card in sortedCards:
                if card.suit == cardIter.suit and card.rank == (inRow + cardIter.rank):
                    inRow += 1
                    flush.append(card)
            if inRow == 5:
                straightFlushes.append(flush[0])

        if len(straightFlushes) > 0:
            maxstr = max(straightFlushes)
            return 10_000 + maxstr.rank * 10 + maxstr.suit

        return False

    def checkForFourOfKind(self, cards):
        sortedCards = sorted(cards, key=attrgetter('suit', 'rank'))
        fours = []
        for cardIter in sortedCards:
            sameRankCounter = 0
            four = []
            for card in sortedCards:
                if card.rank == cardIter.rank:
                    sameRankCounter += 1
                    four.append(card)
            if sameRankCounter == 4:
                fours.append(four[0])

        if len(fours) > 0:
            maxFour = max(fours)
            return 9_000 + maxFour.rank * 10 + maxFour.suit

        return False
    
    def findAllThree(self, cards):
        threes = []
        for cardIter in cards:
            three = []
            sameRankCounter = 0 
            for card in cards:
                if card.rank == cardIter.rank:
                    sameRankCounter += 1
                    three.append(card)
            if sameRankCounter >= 3:
                threes.append(three[0])

        return list(set(threes))

    def findAllPairs(self, cards):
        pairs = []
        for cardIter in cards:
            pair = []
            sameRankCounter = 0
            for card in cards:
                if card.rank == cardIter.rank:
                    sameRankCounter += 1
                    pair.append(card)
            if sameRankCounter >= 2:
                pairs.append(pair[0])

        return list(set(pairs))        

    def CheckForFullHouse(self, cards):
        threes = self.findAllThree(cards)
        if len(threes) == 0: return False
        maxThree = max(threes)
        
        pairs = self.findAllPairs(cards)
        pairs = list(set([x for x in pairs if x.rank != maxThree.rank]))

        if len(pairs) == 0: return False

        maxPair = max(pairs)
        return 8_000 + maxThree.rank * 10 + maxPair.rank

    
    def checkForFlush(self, cards):
        sortedCards = sorted(cards, key=attrgetter('suit', 'rank'))
        straightFlushes = []
        for cardIter in sortedCards:
            inRow = 0
            flush = []
            for card in sortedCards:
                if card.suit == cardIter.suit:
                    inRow += 1
                    flush.append(card)
            if inRow == 5:
                straightFlushes.append(flush[-1])

        if len(straightFlushes) > 0:
            maxstr = max(straightFlushes)
            return 7_000 + maxstr.rank * 10 + maxstr.suit

        return False

    def checkForStraight(self, cards):
        sortedCards = sorted(cards, key=attrgetter('rank', 'suit'))
        straightHands = []
        for cardIter in sortedCards:
            inRow = 0
            straight = []
            for card in sortedCards:
                if card.rank == (inRow + cardIter.rank):
                    inRow += 1
                    straight.append(card)
            if inRow == 5:
                straightHands.append(straight[-1])

        if len(straightHands) > 0:
            maxstr = max(straightHands)
            return 6_000 + maxstr.rank * 10 + maxstr.suit

        return False

    def checkForThreeOfKind(self,cards):
        threes = self.findAllThree(cards)
        if len(threes) > 0:
            return 5_000 + max(threes).rank * 10

    def checkForPairs(self,cards):
        pairs = self.findAllPairs(cards)
        if len(pairs) == 0: return False

        maxPair1 = max(pairs)
        pairs.remove(maxPair1)
        if len(pairs) == 0: 
            return 3_000 + maxPair1.rank * 10 + maxPair1.suit
        
        maxPair2 = max(pairs)
        return 4_000 + maxPair1.rank * 10 + maxPair2.rank

    def checkHighCard(self, cards):
        highestCard = max(cards, key= attrgetter('rank', 'suit'))
        return 2_000 + highestCard.rank * 10 + highestCard.suit