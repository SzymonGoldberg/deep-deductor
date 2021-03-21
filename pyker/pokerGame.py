from pokerTypes import Deck

#           pre-flop    flop    trun    river
stages = [  'pf',       'f',    't',    'r']

class Game:
    def __init__(self, playerList, smallLimit, bigLimit):
        self.playerList = playerList
        self.sLimit = smallLimit
        self.bLimit = bigLimit

    def betting(self):
        pass