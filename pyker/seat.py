class Seat:
    def __init__(self, player):
        self.isWaiting = True
        self.localPot = 0
        self.player = player
        self.move = None
        self.moveValue = 0

    def bet(self, roundData):
        self.move = self.player.bet(roundData.legalMoves(self), roundData)
        underpot = roundData.getCurrentPot() - self.localPot
        self.moveValue = roundData.moveToCash(underpot, self.move)

        self.player.cash -= self.moveValue
        self.localPot += self.moveValue
        
        self.isWaiting = False

        roundData.bankroll += self.moveValue
        return self.moveValue
    
    def updateWaiting(self, pot):
        if pot > self.localPot: self.isWaiting = True

    def stageReset(self):
        self.localPot = 0
        self.isWaiting = True

#TODO this class is taking care about all seats
class Table:
    def __init__(self, players):
        self.seats = [Seat(player) for player in players]

    def updateWaiting(self):
        for seat in self.seats: seat.updateWaiting(self.maxLocalPot())

    def stageReset(self):
        for seat in self.seats: seat.stageReset()

    def clearAllHands(self):
        for seat in self.seats: seat.player.clearHand()

    def isSomeoneWaiting(self):
        return bool(max([x.isWaiting for x in self.seats]))

    def maxLocalPot(self):
        return max(x.localPot for x in self.seats)

    def numOfActiveSeats(self):
        return len(self.seats)
