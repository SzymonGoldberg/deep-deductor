class Agent:
    """ Player card which contain points and hand (cards)
    """
    def __init__(self, startCash :int, playerName :str) -> None:
        assert(startCash > 0)
        self.balance = startCash
        self.name = playerName
        self.clearHand()
        self.smallBets = 0
        self.handsPlayed = 0

    def bet(self, communityData, playerPot :int):
        raise NotImplementedError()

    def showdown(self, winners :list, all :list):
        raise NotImplementedError()

    def clearHand(self):
        self.hand = []