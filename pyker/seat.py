class Seat:
    def __init__(self, player):
        self.isWaiting  = False
        self.underPot   = 0
        self.player     = player
        self.move       = None
        self.moveValue  = 0

    def bet(self, roundData):
        self.move = self.player.bet(roundData.legalMoves(self))
        self.moveValue = roundData.moveToCash(self.underPot, self.move)

        self.doneBet(moveValue)
        roundData.addAction(self)
        return moveValue

    def doneBet(self):
        self.player.cash -= moveValue
        self.underPot = 0
        self.isWaiting = False

    def someoneBetted(self, value):
        self.underPot += value
        self.isWaiting = (value > 0)