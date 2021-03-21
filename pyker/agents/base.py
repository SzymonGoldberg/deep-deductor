
class Agent:
    """ Player card which contain points and hand (cards)
    """
    def __init__(self, startingPoints):
        assert(startingPoints > 0)
        self.points = startingPoints
        self.hand = []
        self.communityCards = []

    def bet(self):
        raise NotImplementedError()