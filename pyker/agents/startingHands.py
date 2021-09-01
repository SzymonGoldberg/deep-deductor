'''https://help.replaypoker.com/hc/en-us/articles/360002230913-A-beginner-s-guide-to-hand-selection-'''
from enum import IntEnum
from operator import attrgetter
from pyker.betQueue import Move
from pyker.cards import Rank, Suit

class StartCat(IntEnum):
    PLAYABLE        = 0
    PLAYABLE_EXTENT = 1
    UNTIL_RAISE     = 2
    TO_FOLD         = 3

PAIRED = {
    Rank.ACE    : StartCat.PLAYABLE, 
    Rank.KING   : StartCat.PLAYABLE,
    Rank.QUEEN  : StartCat.PLAYABLE,
    Rank.JACK   : StartCat.PLAYABLE,
    Rank.TEN    : StartCat.PLAYABLE,
    Rank.NINE   : StartCat.PLAYABLE,
    Rank.EIGHT  : StartCat.PLAYABLE,
    Rank.SEVEN  : StartCat.PLAYABLE,
    Rank.SIX    : StartCat.PLAYABLE_EXTENT,
    Rank.FIVE   : StartCat.PLAYABLE_EXTENT,
    Rank.FOUR   : StartCat.UNTIL_RAISE,
    Rank.THREE  : StartCat.UNTIL_RAISE,
    Rank.TWO    : StartCat.UNTIL_RAISE
}

SUITED = {
    Rank.ACE : {
        Rank.KING   : StartCat.PLAYABLE, 
        Rank.QUEEN  : StartCat.PLAYABLE, 
        Rank.JACK   : StartCat.PLAYABLE, 
        Rank.TEN    : StartCat.PLAYABLE,
        Rank.NINE   : StartCat.PLAYABLE_EXTENT,
        Rank.EIGHT  : StartCat.PLAYABLE_EXTENT,
        Rank.SEVEN  : StartCat.PLAYABLE_EXTENT,
        Rank.SIX    : StartCat.PLAYABLE_EXTENT,
        Rank.FIVE   : StartCat.UNTIL_RAISE,
        Rank.FOUR   : StartCat.UNTIL_RAISE,
        Rank.THREE  : StartCat.UNTIL_RAISE,
        Rank.TWO    : StartCat.UNTIL_RAISE
    },
    Rank.KING : {
        Rank.QUEEN  : StartCat.PLAYABLE,
        Rank.JACK   : StartCat.PLAYABLE,
        Rank.TEN    : StartCat.PLAYABLE,
        Rank.NINE   : StartCat.PLAYABLE_EXTENT,
        Rank.EIGHT  : StartCat.UNTIL_RAISE,
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.UNTIL_RAISE,
        Rank.FIVE   : StartCat.UNTIL_RAISE,
        Rank.FOUR   : StartCat.UNTIL_RAISE,
        Rank.THREE  : StartCat.UNTIL_RAISE,
        Rank.TWO    : StartCat.UNTIL_RAISE
    },
    Rank.QUEEN : {
        Rank.JACK   : StartCat.PLAYABLE,
        Rank.TEN    : StartCat.PLAYABLE,
        Rank.NINE   : StartCat.PLAYABLE_EXTENT,
        Rank.EIGHT  : StartCat.PLAYABLE_EXTENT,
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.JACK : {
        Rank.TEN    : StartCat.PLAYABLE,
        Rank.NINE   : StartCat.PLAYABLE,
        Rank.EIGHT  : StartCat.PLAYABLE_EXTENT,
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.TEN : {
        Rank.NINE   : StartCat.PLAYABLE,
        Rank.EIGHT  : StartCat.PLAYABLE_EXTENT,
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.NINE : {
        Rank.EIGHT  : StartCat.PLAYABLE_EXTENT,
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.UNTIL_RAISE,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.EIGHT : {
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.UNTIL_RAISE,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.SEVEN : {
        Rank.SIX    : StartCat.UNTIL_RAISE,
        Rank.FIVE   : StartCat.UNTIL_RAISE,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.SIX : {
        Rank.FIVE   : StartCat.UNTIL_RAISE,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.FIVE : {
        Rank.FOUR   : StartCat.UNTIL_RAISE,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.FOUR : {
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.THREE : { Rank.TWO : StartCat.TO_FOLD}
}

UNSUITED = {
    Rank.ACE : {
        Rank.KING   : StartCat.PLAYABLE, 
        Rank.QUEEN  : StartCat.PLAYABLE, 
        Rank.JACK   : StartCat.PLAYABLE, 
        Rank.TEN    : StartCat.PLAYABLE,
        Rank.NINE   : StartCat.UNTIL_RAISE,
        Rank.EIGHT  : StartCat.UNTIL_RAISE,
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.KING : {
        Rank.QUEEN  : StartCat.PLAYABLE,
        Rank.JACK   : StartCat.PLAYABLE,
        Rank.TEN    : StartCat.PLAYABLE_EXTENT,
        Rank.NINE   : StartCat.UNTIL_RAISE,
        Rank.EIGHT  : StartCat.TO_FOLD,
        Rank.SEVEN  : StartCat.TO_FOLD,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.QUEEN : {
        Rank.JACK   : StartCat.PLAYABLE_EXTENT,
        Rank.TEN    : StartCat.PLAYABLE_EXTENT,
        Rank.NINE   : StartCat.UNTIL_RAISE,
        Rank.EIGHT  : StartCat.TO_FOLD,
        Rank.SEVEN  : StartCat.TO_FOLD,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.JACK : {
        Rank.TEN    : StartCat.PLAYABLE_EXTENT,
        Rank.NINE   : StartCat.UNTIL_RAISE,
        Rank.EIGHT  : StartCat.UNTIL_RAISE,
        Rank.SEVEN  : StartCat.TO_FOLD,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.TEN : {
        Rank.NINE   : StartCat.UNTIL_RAISE,
        Rank.EIGHT  : StartCat.UNTIL_RAISE,
        Rank.SEVEN  : StartCat.TO_FOLD,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.NINE : {
        Rank.EIGHT  : StartCat.UNTIL_RAISE,
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.EIGHT : {
        Rank.SEVEN  : StartCat.UNTIL_RAISE,
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.SEVEN : {
        Rank.SIX    : StartCat.TO_FOLD,
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.SIX : {
        Rank.FIVE   : StartCat.TO_FOLD,
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.FIVE : {
        Rank.FOUR   : StartCat.TO_FOLD,
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.FOUR : {
        Rank.THREE  : StartCat.TO_FOLD,
        Rank.TWO    : StartCat.TO_FOLD
    },
    Rank.THREE : { Rank.TWO : StartCat.TO_FOLD}
}

def handToStartCategory(hand):
    hand = sorted(hand, key=attrgetter('rank', 'suit'))
    assert(len(hand) == 2)
    if hand[0].rank == hand[1].rank:
        return PAIRED[hand[0].rank]
    if hand[0].suit == hand[1].suit:
        return UNSUITED[hand[1].rank][hand[0].rank]
    return SUITED[hand[1].rank][hand[0].rank]