import unittest
from pyker.cards import *
from pyker.pokerGame import *
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

class TestRoundData(unittest.TestCase):
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
    def testThrowingPlayers(self):
        players = [Agent(1, "foo"), Agent(1, "bar"), Agent(1, "fun")]

        for player in players:
            player.move = Move.QUIT

        game = Game(players, 0)
        game.throwPlayers()
        for player in game.players:
            print(player.name)
        self.assertTrue(len(game.players) == 0)



if __name__ == '__main__':
    unittest.main()