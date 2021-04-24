from .cards import Deck
from .seat import Seat
from enum import IntEnum

class Move(IntEnum):
    BLIND = 0
    FOLD = 2
    CHECK = 3
    BET = 4
    CALL = 5
    RAISE = 6
    QUIT = 7


#         pre-flop, flop, turn, river
stages = ['pf', 'f', 't', 'r']


class RoundData:
    """Structure with data which can be accessed in any time by any player
    """
    def __init__(self, limit):
        self.communityCards = []
        self.stage = 0
        self.position = 0
        self.localLimit = limit
        self.pots = [0, 0, 0, 0]
        self.actions = [] 

    def raiseLimit(self):
        self.localLimit *= 2

    def moveToCash(self, underPot, move):
        toCashDict = { 
            move.FOLD:  0,
            move.CHECK:  0,
            move.QUIT:  0,
            move.CALL: underPot,
            move.BET:   self.localLimit,
            move.RAISE: self.localLimit + underPot,
            move.BLIND: self.localLimit / (1 if self.position else 2)
        }
        return toCashDict[move]

    def expectedMoves(self, underPot):
        if self.stage == 0 and (self.position == 0 or self.position == 1):
            return [Move.BLIND]

        return [Move.FOLD , Move.CALL, Move.RAISE, Move.QUIT
        ] if (underPot > 0) else [Move.FOLD, Move.CHECK, Move.BET, Move.QUIT]

    def affordableMoves(self, seat):
        moves = self.expectedMoves(seat.underPot)
        return [x for x in moves if seat.player.cash >= self.moveToCash(seat.underPot, x)]

    def legalMoves(self, seat):
        affordableMoves = self.AffordableMoves(seat)
        return [Move.QUIT] if affordableMoves == [Move.FOLD] else affordableMoves
    
    def addAction(self, seat):
        self.pots[self.stage] += seat.MoveValue
        self.actions.append([seat.player.name, seat.Move, self.stage])

#NOT DONE YET
class Game:
    def __init__(self, players, limit):
        assert(len(players) > 2)
        self.limit = limit
        self.players = players
        self.deck = None
        self.roundData = None

    def makeBet(self, seats):
        seatWhoBet = seats.pop(0)
        lastBetValue = seatWhoBet.bet(RoundData)
        for seat in seats: 
            seat.someoneBetted(lastBetValue)

        if seatWhoBet.move == Move.QUIT:    self.players.remove(seatWhoBet.player)
        elif seatWhoBet.move != Move.FOLD:  seats.append(seatWhoBet)

    def throwBrokenPlayers(self, entryValue):
        self.players = [x for x in self.players if x.cash >= entryValue]

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

    def bettingLoop(self, seats):
        while sum([seat.isWaiting for seat in seats]):
            self.makeBet(seats)
            self.roundData.position += 1

    def showdown(self):
        pass

    def stage(self, seats):
        StagesFuncs = [
            self.preFlopStage, 
            self.flopStage, 
            self.turnStage, 
            self.riverStage
        ]
        StagesFuncs[self.roundData.stage](seats)
        self.roundData.stage += 1

    def StartRound(self):
        self.throwBrokenPlayers(self.limit)
        self.deck = Deck()
        self.roundData = RoundData(self.limit)
        seats = [Seat(player) for player in self.players]
        for i in range(len(stages)): self.stage(seats)