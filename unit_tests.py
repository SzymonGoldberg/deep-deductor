import unittest
from pyker.cards import *
from pyker.seat import *
from pyker.game import *
from pyker.agents.base import *
from pyker.cardValidator import *

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

        self.roundData.numOfBets = 1
        expectedMoves = self.roundData.expectedMoves(0)
        self.assertEqual(expectedMoves, [Move.BLIND])

        #check for normal round functionality
        self.roundData.numOfBets = 4
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

        self.roundData.numOfBets = 1
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.BLIND in moves)
        self.assertTrue(len(moves) == 1)

        #normal
        self.roundData.numOfBets = 4
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.QUIT in moves)
        self.assertTrue(Move.BET in moves)
        self.assertTrue(Move.CHECK in moves)
        self.assertTrue(Move.FOLD in moves)
        self.assertTrue(len(moves) == 4)

        #under pot
        self.roundData.setCurrentPot(10)
        seat.player.cash = 100
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.QUIT in moves)
        self.assertTrue(Move.RAISE in moves)
        self.assertTrue(Move.CALL in moves)
        self.assertTrue(Move.FOLD in moves)
        self.assertTrue(len(moves) == 4)

        #not enough money for bet
        self.roundData.setCurrentPot(15)
        seat.player.cash = 15
        moves = self.roundData.affordableMoves(seat)
        self.assertTrue(Move.QUIT in moves)
        self.assertTrue(Move.CALL in moves)
        self.assertTrue(Move.FOLD in moves)
        self.assertTrue(len(moves) == 3)

class TestCardValidatorClass(unittest.TestCase):
    def setUp(self):
        self.cardValidator = CardValidator()

    def testStraightFlushCheck(self):
        cards = [
        Card(Rank.FOUR,     Suit.DIAMOND),
        Card(Rank.SIX,      Suit.DIAMOND),
        Card(Rank.KING,     Suit.HEART),
        Card(Rank.FIVE,     Suit.DIAMOND),
        Card(Rank.FIVE,     Suit.SPADE),
        Card(Rank.EIGHT,    Suit.DIAMOND),
        Card(Rank.SEVEN,    Suit.DIAMOND)]

        
        self.assertTrue(self.cardValidator.checkForStraightFlush(cards) ==  10000 + Rank.FOUR * 10 + Suit.DIAMOND)

        cards = [
        Card(Rank.FOUR,     Suit.DIAMOND),
        Card(Rank.SIX,      Suit.HEART),
        Card(Rank.KING,     Suit.HEART),
        Card(Rank.FIVE,     Suit.DIAMOND),
        Card(Rank.FIVE,     Suit.SPADE),
        Card(Rank.EIGHT,    Suit.DIAMOND),
        Card(Rank.SEVEN,    Suit.DIAMOND)]
        self.assertFalse(self.cardValidator.checkForStraightFlush(cards))

        cards = [
        Card(Rank.FOUR,     Suit.DIAMOND),
        Card(Rank.SIX,      Suit.DIAMOND),
        Card(Rank.KING,     Suit.HEART),
        Card(Rank.NINE,     Suit.DIAMOND),
        Card(Rank.FIVE,     Suit.DIAMOND),
        Card(Rank.EIGHT,    Suit.DIAMOND),
        Card(Rank.SEVEN,    Suit.DIAMOND)]
        self.assertTrue(self.cardValidator.checkForStraightFlush(cards) == 10000 + Rank.FIVE * 10 + Suit.DIAMOND)

        cards = [
        Card(Rank.QUEEN,    Suit.DIAMOND),
        Card(Rank.JACK,      Suit.DIAMOND),
        Card(Rank.KING,     Suit.DIAMOND),
        Card(Rank.FIVE,     Suit.DIAMOND),
        Card(Rank.FIVE,     Suit.SPADE),
        Card(Rank.TEN,      Suit.DIAMOND),
        Card(Rank.ACE,    Suit.DIAMOND)]
        
        self.assertTrue(self.cardValidator.checkForStraightFlush(cards) == 10000 + Rank.TEN * 10 + Suit.DIAMOND)

        cards = [
        Card(Rank.QUEEN,  Suit.DIAMOND),
        Card(Rank.JACK,   Suit.HEART),
        Card(Rank.KING,   Suit.DIAMOND),
        Card(Rank.FIVE,   Suit.DIAMOND),
        Card(Rank.FIVE,   Suit.SPADE),
        Card(Rank.TEN,    Suit.DIAMOND),
        Card(Rank.ACE,    Suit.DIAMOND)]
        
        self.assertFalse(self.cardValidator.checkForStraightFlush(cards))

    def testFourOfKind(self):

        cards = [
        Card(Rank.JACK,  Suit.DIAMOND),
        Card(Rank.JACK,   Suit.HEART),
        Card(Rank.JACK,   Suit.SPADE),
        Card(Rank.JACK,   Suit.CLUB),
        Card(Rank.FIVE,   Suit.SPADE),
        Card(Rank.TEN,    Suit.DIAMOND),
        Card(Rank.ACE,    Suit.DIAMOND)]
        
        self.assertTrue(self.cardValidator.checkForFourOfKind(cards) == 9_000 + 10 * Rank.JACK + Suit.CLUB)
        
        cards = [
        Card(Rank.FOUR,  Suit.DIAMOND),
        Card(Rank.FOUR,   Suit.HEART),
        Card(Rank.FOUR,   Suit.SPADE),
        Card(Rank.FOUR,   Suit.CLUB),
        Card(Rank.FIVE,   Suit.SPADE),
        Card(Rank.FIVE,   Suit.HEART),
        Card(Rank.FIVE,   Suit.DIAMOND),
        Card(Rank.FIVE,   Suit.DIAMOND),
        Card(Rank.TEN,    Suit.DIAMOND),
        Card(Rank.ACE,    Suit.DIAMOND)]
        
        self.assertTrue(self.cardValidator.checkForFourOfKind(cards) == 9_000 + 10 * Rank.FIVE + Suit.DIAMOND)

    def testFullHouse(self):
        cards = [
        Card(Rank.JACK,  Suit.DIAMOND),
        Card(Rank.JACK,   Suit.HEART),
        Card(Rank.JACK,   Suit.SPADE),
        Card(Rank.FIVE,   Suit.CLUB),
        Card(Rank.FIVE,   Suit.SPADE),
        Card(Rank.TEN,    Suit.DIAMOND),
        Card(Rank.ACE,    Suit.DIAMOND)]
        
        self.assertTrue(self.cardValidator.CheckForFullHouse(cards) == 8_000 + Rank.JACK * 10 + Rank.FIVE)

        cards = [
        Card(Rank.JACK,  Suit.DIAMOND),
        Card(Rank.JACK,   Suit.HEART),
        Card(Rank.JACK,   Suit.SPADE),
        Card(Rank.FIVE,   Suit.CLUB),
        Card(Rank.FIVE,   Suit.SPADE),
        Card(Rank.FIVE,    Suit.DIAMOND),
        Card(Rank.ACE,    Suit.DIAMOND)]
        
        self.assertTrue(self.cardValidator.CheckForFullHouse(cards) == 8_000 + Rank.JACK * 10 + Rank.FIVE)


class TestGameClass(unittest.TestCase):
    def testThrowingBrokenPlayers(self):
        players = [Agent(1, "foo"), Agent(1, "bar"), Agent(1, "fun")]

        game = Game(players, 12)
        game.throwBrokenPlayers()
        self.assertTrue(len(game.players) == 0)



if __name__ == '__main__':
    unittest.main()
