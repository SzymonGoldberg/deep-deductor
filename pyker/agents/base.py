
from pyker.roundData import CommunityData


class Agent:
    """ Player card which contain points and hand (cards)
    """
    def __init__(self, startCash :int, playerName :str) -> None:
        assert(startCash > 0)
        self.balance = startCash
        self.name = playerName
        self.clearHand()

    def bet(self, communityData :CommunityData, playerPot :int):
        raise NotImplementedError()

    def clearHand(self):
        self.hand = []