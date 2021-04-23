import unittest
from cards import *
from seat import *
from game import *
from agents.base import *

class TestSuitEnum(unittest.TestCase):
    def testRankComparison(self):
        self.assertTrue(Suit.SPADE > Suit.CLUB)
        self.assertTrue(Suit.HEART > Suit.DIAMOND)
        self.assertFalse(Suit.CLUB > Suit.HEART)

class TestCardClass(unittest.TestCase):
    def testasStringMethod(self):
        card = Card(Rank.ACE, Suit.SPADE)
        self.assertEqual('As', card.asString())
        card = Card(Rank.KING, Suit.DIAMOND)
        self.assertEqual('Kd', card.asString())
        card = Card(6, 2359)
        self.assertEqual('invalid card', card.asString())

class TestDeckClass(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def testDeckInit(self):
        self.assertEqual(len(self.deck.cards), 52)

    def testDraw(self):
        self.assertEqual(len(self.deck.draw(3)), 3)
        self.assertEqual(len(self.deck.cards), 52-3)
        del self.deck.cards[:48]
        self.assertEqual(self.deck.draw(3), [])
        self.assertEqual(self.deck.draw(10), [])

class TestRoundData(unittest.TestCase):
    #TODO repair that test
    def testMoveValidation(self):
        roundData = RoundData(15)
        move = roundData.legalMoves(0)
        self.assertEqual(move, [Move.BLIND])

        roundData.position = 1
        move = roundData.legalMoves(0)
        self.assertEqual(move, [Move.BLIND])

        roundData.stage = 1
        move = roundData.legalMoves(0)
        self.assertEqual(move, [Move.FOLD, Move.CHECK, Move.BET])

        move = roundData.legalMoves(10)
        self.assertEqual(move, [Move.FOLD, Move.CALL, Move.RAISE])

class TestGameClass(unittest.TestCase):
    def testThrowingBrokenPlayers(self):
        players = [Agent(1, "foo"), Agent(1, "bar"), Agent(1, "fun")]

        game = Game(players, 0)
        game.throwBrokenPlayers(25)
        self.assertTrue(len(game.players) == 0)



if __name__ == '__main__':
    unittest.main()