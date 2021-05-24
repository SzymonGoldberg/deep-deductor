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
        self.table = None
        self.winner = None
        self.roundWinners = None

    def checkForRoundWinners(self):
        if self.table.numOfActiveSeats() < 2:
            self.roundWinners = [self.table.seats[0]]

    def checkForGameWinner(self):
        if len(self.players) < 2:
            self.winner = self.players[0]  

    def makeBet(self):
        seatWhoBet = self.table.seats.pop(0)
        seatWhoBet.bet(self.roundData)

        if seatWhoBet.move == Move.QUIT:    
            self.players.remove(seatWhoBet.player)
            self.checkForGameWinner()
            return

        elif seatWhoBet.move == Move.FOLD:  
            self.checkForRoundWinners()
            return

        self.table.seats.append(seatWhoBet)
        self.roundData.betUpdate(self.table.maxLocalPot())
        self.table.updateWaiting()

    def bettingLoop(self):
        if self.table.isSomeoneWaiting() and\
           self.roundWinners == None and\
           self.winner == None:
            self.makeBet()
            self.bettingLoop()

    def waitForBlinds(self):
        if self.roundData.numOfBets > 2 and\
           self.roundWinners == None and\
           self.winner == None: 
            self.makeBet()
            self.waitForBlinds()

    def preFlopStage(self):
        self.waitForBlinds()
        for seat in self.table.seats: 
            seat.player.hand = self.deck.draw(2) #every player now get cards    #smth is not ok here
        self.bettingLoop()

        self.roundData.communityCards.extend(self.deck.draw(3)) #flop going onto the table

    def flopStage(self):
        self.bettingLoop()
        self.roundData.communityCards.extend(self.deck.draw(1))
        self.roundData.raiseLimit()

    def turnStage(self):
        self.bettingLoop()
        self.roundData.communityCards.extend(self.deck.draw(1))

    def riverStage(self):
        self.bettingLoop()

    def showdown(self):
        print("showdown") #DEBUG

    def nextStage(self):
        StagesFuncs = [
            self.preFlopStage, 
            self.flopStage, 
            self.turnStage, 
            self.riverStage,
            self.showdown
        ]
        print("stage = ", self.roundData.stage)     #debug
        StagesFuncs[self.roundData.stage]()
        self.table.stageReset()

        self.roundData.stage += 1

    def roundReset(self):
        self.roundWinners = None
        self.deck = Deck()
        self.roundData = RoundData(self.limit)
        self.table = Table(self.players)
        self.table.clearAllHands()

    def start(self):
        self.roundReset()
        for i in range(5): self.nextStage()
        
        if self.winner == None:
            self.start()
        return self.winner