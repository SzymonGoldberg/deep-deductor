class Seat:
    def __init__(self, player):
        self.isWaiting = False
        self.localPot = 0
        self.player = player
        self.move = None
        self.moveValue = 0

    def bet(self, roundData):
        self.move = self.player.bet(roundData.legalMoves(self), roundData)
        self.moveValue = roundData.moveToCash(self.underPot, self.move)

        self.doneBet()
        roundData.addAction(self)
        return self.moveValue

    def doneBet(self):
        self.player.cash -= self.moveValue
        self.localPot += self.moveValue

    def someoneBetted(self, value):
        print("waiting? ", self.isWaiting, " player ", self.player.name, "underpot? ", self.underPot) #debug