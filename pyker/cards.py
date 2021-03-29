from enum import IntEnum
from collections import namedtuple
import random

class Suit(IntEnum):
    """Simple enum with suits set in order of their priority (lowest is 0, highest is 3)"""
    CLUB    = 0
    DIAMOND = 1
    HEART   = 2
    SPADE   = 3

suit_to_str = {
    Suit.CLUB   : 'c',
    Suit.DIAMOND: 'd',
    Suit.HEART  : 'h',
    Suit.SPADE  : 's'
}

class Rank(IntEnum):
    TWO     = 2
    THREE   = 3
    FOUR    = 4
    FIVE    = 5
    SIX     = 6
    SEVEN   = 7
    EIGHT   = 8
    NINE    = 9
    TEN     = 10
    JACK    = 11
    QUEEN   = 12
    KING    = 13
    ACE     = 14

rank_to_str = {
    Rank.TWO    : '2',
    Rank.THREE  : '3',
    Rank.FOUR   : '4',
    Rank.FIVE   : '5',
    Rank.SIX    : '6',
    Rank.SEVEN  : '7',
    Rank.EIGHT  : '8',
    Rank.NINE   : '9',
    Rank.TEN    : 'T',
    Rank.JACK   : 'J',
    Rank.QUEEN  : 'Q',
    Rank.KING   : 'K',
    Rank.ACE    : 'A'
}

class Card(namedtuple('Card', 'rank suit')):
    """ card type builded with rank (int between 2 and 14) and suit (see Suit class)"""
    def asString(self):
        """ This method return card as string like this one from IRC  database.
            If some errors occured it returns 'invalid card' string"""
        return str(rank_to_str[self.rank] + suit_to_str[self.suit]
            ) if self.rank in rank_to_str and self.suit in suit_to_str else str(
            'invalid card')
            
class Deck():
    """ Class represents all cards used in single game"""
    def __init__(self):
        """ class is initialized as classic deck with all 52"""
        self.cards = [Card(x, y) for x in Rank for y in Suit]
        random.shuffle(self.cards)

    def draw(self, n):
        """ Returns n cards from the deck. If deck is smaller than n it returns empty list"""
        output = []
        if n <= len(self.cards):
            output = self.cards[:n]
            del self.cards[:n]
        return output


if __name__ == '__main__':
    deck = Deck()
    for elem in deck.cards:
        print(elem.asString())