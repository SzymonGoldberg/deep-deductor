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
        self.winner = None

    def checkForWinner(self):
        if len(self.players) < 2:
            self.winner = self.players[0]    

    def makeBet(self, table):
        if self.winner != None: return

        seatWhoBet = table.seats.pop(0)
        seatWhoBet.bet(self.roundData)

        if seatWhoBet.move == Move.QUIT:    
            self.players.remove(seatWhoBet.player)
            self.checkForWinner()
            return
        elif seatWhoBet.move != Move.FOLD:  table.seats.append(seatWhoBet)

        self.roundData.betUpdate(table.maxLocalPot())
        table.updateWaiting()

    def bettingLoop(self, table):
        self.makeBet(table)
        if table.isSomeoneWaiting() and self.winner == None: self.bettingLoop(table)

    def waitForBlinds(self, table):
        self.makeBet(table)
        if self.roundData.numOfBets > 2 and self.winner == None: self.waitForBlinds(table)

    def preFlopStage(self, table):
        self.waitForBlinds(table)
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

    def start(self):
        self.deck = Deck()
        self.roundData = RoundData(self.limit)
        table = Table(self.players)
        for i in range(4): self.stage(table)
        
        if self.winner == None:
            self.start()
        return self.winner