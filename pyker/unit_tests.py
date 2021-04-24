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
    def setUp(self):
        self.roundData = RoundData(15)

    def testExpectedMoves(self):

        #check for blind functionality
        expectedMoves = self.roundData.expectedMoves(0)
        self.assertEqual(expectedMoves, [Move.BLIND])

        self.roundData.position = 1
        expectedMoves = self.roundData.expectedMoves(0)
        self.assertEqual(expectedMoves, [Move.BLIND])

        #check for normal round functionality
        self.roundData.position = 4
        expectedMoves = self.roundData.expectedMoves(10)
        self.assertTrue(Move.FOLD in expectedMoves)
        self.assertTrue(Move.CALL in expectedMoves)
        self.assertTrue(Move.RAISE in expectedMoves)
        self.assertTrue(Move.QUIT in expectedMoves)
        self.assertTrue(len(expectedMoves) == 4)

        expectedMoves = self.roundData.expectedMoves(0)
        self.assertTrue(Move.FOLD in expectedMoves)
        self.assertTrue(Move.CHECK in expectedMoves)
        self.assertTrue(Move.BET in expectedMoves)
        self.assertTrue(Move.QUIT in expectedMoves)
        self.assertTrue(len(expectedMoves) == 4)

    def testAffordableMoves(self):

        #blinds
        player = Agent(15, "f00")
        seat = Seat(player)
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.BLIND in moves)
        self.assertTrue(len(moves) == 1)

        self.roundData.position = 1
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.BLIND in moves)
        self.assertTrue(len(moves) == 1)

        #normal
        self.roundData.position = 4
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.QUIT in moves)
        self.assertTrue(Move.BET in moves)
        self.assertTrue(Move.CHECK in moves)
        self.assertTrue(Move.FOLD in moves)
        self.assertTrue(len(moves) == 4)

        #under pot
        seat.underPot = 10
        seat.player.cash = 100
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.QUIT in moves)
        self.assertTrue(Move.RAISE in moves)
        self.assertTrue(Move.CALL in moves)
        self.assertTrue(Move.FOLD in moves)
        self.assertTrue(len(moves) == 4)

        #not enough money for bet
        seat.underPot = 0
        seat.player.cash = 10
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.QUIT in moves)
        self.assertTrue(Move.CHECK in moves)
        self.assertTrue(Move.FOLD in moves)
        self.assertTrue(len(moves) == 3)


class TestGameClass(unittest.TestCase):
    def testThrowingBrokenPlayers(self):
        players = [Agent(1, "foo"), Agent(1, "bar"), Agent(1, "fun")]

        game = Game(players, 0)
        game.throwBrokenPlayers(25)
        self.assertTrue(len(game.players) == 0)



if __name__ == '__main__':
    unittest.main()
