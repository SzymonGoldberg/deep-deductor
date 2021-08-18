class Agent:
    """ Player card which contain points and hand (cards)
    """
    def __init__(self, playerName :str) -> None:
        self.balance = self.smallBets = self.handsPlayed = 0
        self.name = playerName
        self.clearHand()

    def bet(self, communityData, playerPot :int):
        raise NotImplementedError()

    def showdown(self, winners :list, all :list):
        raise NotImplementedError()

    def clearHand(self):
        self.hand = []