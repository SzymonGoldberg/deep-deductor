
class Agent:
    """ Player card which contain points and hand (cards)
    """
    def __init__(self, startCash, playerName):
        assert(startCash > 0)
        self.cash = startCash
        self.name = playerName
        self.hand = []

    def bet(self, legalMoves, GameData):
        raise NotImplementedError()