from .cards import *
from operator import attrgetter

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

        isStraightFlush = len(straightFlushes) > 0
        return [isStraightFlush, max(straightFlushes) if isStraightFlush else None]

    def checkForRoyalFlush(self,cards):
        isStraightFlush = self.checkForStraightFlush(cards)
        return [True if isStraightFlush[1].rank == Rank.TEN else False, isStraightFlush]