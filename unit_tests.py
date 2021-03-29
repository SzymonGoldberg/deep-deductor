import unittest
from pyker.cards import Suit, Rank, Card, Deck
from pyker.pokerGame import CashService, Seat, Move
from pyker.agents.base import Agent

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
    def testDeckInit(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def testDraw(self):
        deck = Deck()
        self.assertEqual(len(deck.draw(3)), 3)
        self.assertEqual(len(deck.cards), 52-3)
        del deck.cards[:48]
        self.assertEqual(deck.draw(3), [])
        self.assertEqual(deck.draw(10), [])

class TestCashService(unittest.TestCase):
    def testMoveValidation(self):
        service = CashService(10)
        move = service.legalMoves(0, 0, 0)
        self.assertEqual(move, [Move.BLIND])

        move = service.legalMoves(0, 0, 1)
        self.assertEqual(move, [Move.BLIND])

        move = service.legalMoves(0, 0, 2)
        self.assertEqual(move, [Move.FOLD, Move.CHECK, Move.BET])

        move = service.legalMoves(0, 1, 2)
        self.assertEqual(move, [Move.FOLD, Move.CALL, Move.RAISE])


    def testCashValidation(self):
        seat = Seat(Agent(100, 'testname'))
        service = CashService(10)

        move = service.checkAffordability(0, seat, 2)
        self.assertEqual(move, [Move.FOLD, Move.CHECK, Move.BET])


if __name__ == '__main__':
    unittest.main()