from pyker.cards import Deck
from enum import IntEnum

class Move(IntEnum):
    BLIND   = 0
    FOLD    = 2
    CHECK   = 3
    BET     = 4
    CALL    = 5
    RAISE   = 6
    QUIT    = 7

#           pre-flop    flop    trun    river
stages = [  'pf',       'f',    't',    'r']

class SingleRoundData:
    """Structure with data which can be accessed in any time by any player
    """
    def __init__(self, limit):
        self.communityCards = []
        self.stage = 0
        self.position = 0
        self.localLimit = limit
        self.pots = [0, 0, 0, 0]
        self.actions = [] 

    def legalMoves(self, underPot):
        if self.stage == 0 and (self.position == 0 or self.position == 1):
            return [Move.BLIND]

        return [Move.FOLD , Move.CALL, Move.RAISE
        ] if (underPot > 0) else [Move.FOLD, Move.CHECK, Move.BET]

    def raiseLimit(self):
        self.limit *= 2

    def moveToCash(self, underPot, move):
        toCashDict = { 
            move.FOLD   : 0,
            move.CALL   : 0,
            move.QUIT   : 0,
            move.CHECK  : underPot,
            move.BET    : self.localLimit,
            move.RAISE  : self.localLimit + underPot,
            move.BLIND  : self.localLimit / (1 if self.position else 2)
        }
        return toCashDict[move]

    def getAffordableMoves(self, seat):
        cash = seat.player.cash

        #player is broken case
        if(cash < self.localLimit) return [Move.QUIT]
        
        legalMoves = self.legalMoves(seat.underPot)
        return [x for x in legalMoves if cash >= self.moveToCash(seat.underPot, x)]

    def addAction(self, seat):
        self.pots[self.stage] += seat.lastMoveValue
        self.actions.append([seat.player.name, seat.lastMove, self.stage])

class Seat:
    def __init__(self, player):
        self.isWaiting  = False
        self.underPot   = 0
        self.player     = player
        self.Move       = None
        self.MoveValue  = 0

    def bet(self, roundData):
        self.Move = self.player.bet(roundData.getAffordableMoves(self))
        self.moveValue = roundData.moveToCash(self.underPot, self.Move)

        self.player.cash -= moveValue
        self.underPot = 0
        self.isWaiting = False
        roundData.addAction(self)
    
#NOT DONE YET
class Game:
    def __init__(self, players, limit):
        assert(len(players) > 2)
        self.roundData = SingleRoundData(limit)
        self.seats = [Seat(player) for player in players]

    def turn(self):

        position = 0
        while sum([x.isWaiting for x in self.players]):
            for seat in self.seats:
                CashService.makeMove(seat, self.seats, self.data.stage, position)
                position += 1