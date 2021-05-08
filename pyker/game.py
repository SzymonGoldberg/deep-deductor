from .cards import Deck
from .seat import Seat
from .roundData import RoundData, Move

#NOT DONE YET
class Game:
    def __init__(self, players, limit):
        assert(len(players) > 1)
        self.limit = limit
        self.players = players
        self.deck = None
        self.roundData = None


    ##TODO I have to change a lot of things in this function
    def makeBet(self, seats):
        seatWhoBet = seats.pop(0)
        lastBetValue = seatWhoBet.bet(self.roundData)

        if seatWhoBet.move == Move.QUIT:    self.players.remove(seatWhoBet.player)
        elif seatWhoBet.move != Move.FOLD:  seats.append(seatWhoBet)
        self.roundData.updatePot(seats)
        for seat in seats: 
            seat.updateWaiting(self.roundData.getCurrentPot())

        self.roundData.numOfBets += 1
        print("current pot  = ", self.roundData.getCurrentPot(), " player pot = ", seats[-1].localPot)

    def throwBrokenPlayers(self):
        self.players = [x for x in self.players if x.cash >= self.limit]

    def bettingLoop(self, seats):
        self.makeBet(seats)

        if max([x.isWaiting for x in seats]):
            self.bettingLoop(seats)

    def preFlopStage(self, seats):
        for i in range(2): self.makeBet(seats) #small and big blinds
        for seat in seats: seat.player.hand = self.deck.draw(2) #every player now get cards
        self.bettingLoop(seats)

        self.roundData.communityCards.extend(self.deck.draw(3)) #flop going onto the table

    def flopStage(self, seats):
        self.bettingLoop(seats)
        self.roundData.communityCards.extend(self.deck.draw(1))
        self.roundData.raiseLimit()

    def turnStage(self, seats):
        self.bettingLoop(seats)
        self.roundData.communityCards.extend(self.deck.draw(1))

    def riverStage(self, seats):
        self.bettingLoop(seats)
        self.showdown()

    def showdown(self):
        pass

    def stage(self, seats):
        StagesFuncs = [
            self.preFlopStage, 
            self.flopStage, 
            self.turnStage, 
            self.riverStage
        ]
        print("stage = ", self.roundData.stage)     #debug
        StagesFuncs[self.roundData.stage](seats)
        for seat in seats:
            seat.stageReset()

        self.roundData.stage += 1

    def StartRound(self):
        self.throwBrokenPlayers()
        self.deck = Deck()
        self.roundData = RoundData(self.limit)
        seats = [Seat(player) for player in self.players]
        for i in range(4): self.stage(seats)