from .cards import *
from operator import attrgetter

class CardValidator:
    def combination(self):
        pass

    def checkForStraightFlush(self, cards):
        
        sortedCards = sorted(cards, key=attrgetter('suit', 'rank'))
        
        for cardIter in sortedCards:
            inRow = [0]
            for card in sortedCards:
                if card.suit == cardIter.suit and card.rank == (inRow + cardIter.rank):
                    inRow += 1
            if inRow == 5: 
                return True

        return False

    def checkForRoyalFlush(self):
        pass