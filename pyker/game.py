from .cards import Deck
from .seat import Seat, Table
from .roundData import RoundData, Move

#NOT DONE YET
class Game:
    def __init__(self, players, limit):
        assert(len(players) > 1)
        self.limit = limit
        self.players = players
        self.deck = None
        self.roundData = None

    def makeBet(self, table):
        seatWhoBet = table.seats.pop(0)
        lastBetValue = seatWhoBet.bet(self.roundData)

        if seatWhoBet.move == Move.QUIT:    self.players.remove(seatWhoBet.player)
        elif seatWhoBet.move != Move.FOLD:  table.seats.append(seatWhoBet)

        self.roundData.setCurrentPot(table.maxLocalPool())
        table.updateWaiting(self.roundData.getCurrentPot())

        self.roundData.numOfBets += 1
        print("current pot  = ", self.roundData.getCurrentPot(), " player pot = ", table.seats[-1].localPot)  #debug

    def throwBrokenPlayers(self):
        self.players = [x for x in self.players if x.cash >= self.limit]

    def bettingLoop(self, table):
        self.makeBet(table)
        if table.isSomeoneWaiting(): self.bettingLoop(table)

    def preFlopStage(self, table):
        for i in range(2): self.makeBet(table) #small and big blinds
        for seat in table.seats: seat.player.hand = self.deck.draw(2) #every player now get cards
        self.bettingLoop(table)

        self.roundData.communityCards.extend(self.deck.draw(3)) #flop going onto the table

    def flopStage(self, table):
        self.bettingLoop(table)
        self.roundData.communityCards.extend(self.deck.draw(1))
        self.roundData.raiseLimit()

    def turnStage(self, table):
        self.bettingLoop(table)
        self.roundData.communityCards.extend(self.deck.draw(1))

    def riverStage(self, table):
        self.bettingLoop(table)
        self.showdown()

    def showdown(self):
        pass

    def stage(self, table):
        StagesFuncs = [
            self.preFlopStage, 
            self.flopStage, 
            self.turnStage, 
            self.riverStage
        ]
        print("stage = ", self.roundData.stage)     #debug
        StagesFuncs[self.roundData.stage](table)
        table.stageReset()

        self.roundData.stage += 1

    def StartRound(self):
        self.throwBrokenPlayers()
        self.deck = Deck()
        self.roundData = RoundData(self.limit)
        table = Table(self.players)
        for i in range(4): self.stage(table)