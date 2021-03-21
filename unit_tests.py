import unittest
from pyker.pokerTypes import Suit, Rank, Card, Deck

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

if __name__ == '__main__':
    unittest.main()