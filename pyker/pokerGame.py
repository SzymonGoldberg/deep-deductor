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

class GameData:
    """Structure with data which can be accessed in any time by any player
    """
    def __init__(self):
        self.communityCards = []
        self.actions = dict()
        self.stage = 0

class Seat:
    def __init__(self, player):
        self.waitToBet = False
        self.folded = False
        self.underPot = 0
        self.player = player

    def isWaiting(self):
        return self.waitToBet
        
class CashService:
    def __init__(self, limit):
        self.blimit = limit
        self.slimit = limit/2
        self.pot = 0

    def legalMoves(self, stage, underPot, position):
        if stage == 0 and (position == 0 or position == 1):
            return [Move.BLIND]

        return [Move.FOLD , Move.CALL, Move.RAISE
        ] if (underPot > 0) else [Move.FOLD, Move.CHECK, Move.BET]

    def moveToCash(self, stage, seat, position, move):
        if move == Move.FOLD:   return 0
        if move == Move.CALL:   return 0
        if move == Move.QUIT:   return 0
        if move == Move.CHECK:  return seat.underPot

        if move == Move.BLIND and position == 0:    return self.slimit/2
        if move == Move.BLIND and position == 1:    return self.slimit

        if move == Move.BET:
            return self.slimit if stage in [0, 1] else self.blimit

        if move == Move.RAISE:
            return seat.underPot + (self.slimit if gameData.stage in [0, 1] else self.blimit)

    def checkAffordability(self, stage, seat, position):
        legalMoves = self.legalMoves(stage, seat.underPot, position)
        affordableMoves = [x for x in legalMoves if seat.player.cash >= self.moveToCash(stage, seat, position, x)]

        return affordableMoves if len(affordableMoves) > 0 else [Move.QUIT]

    def makeMove(self, seatWhichBet, seats, stage, position):
        move = seatWhichBet.player.bet(self.checkAffordability(stage, seatWhichBet, position))
        moveValue = self.betToCash(stage,seatWhichBet, position, move)

        if move == Move.FOLD:
            seatWhichBet.folded = True
            return

        if move == Move.BLIND or move == move.BET or move == Move.RAISE:
            for x in seats:
                if x != seatWhichBet:
                    x.underPot += moveValue
                    x.waitToBet = True
            
        seatWhichBet.player.cash -= moveValue
        seatWhichBet.underPot = 0
        seatWhichBet.waitToBet = False
        self.pot += moveValue
            
class Game:
    def __init__(self, players, limit):
        assert(len(players) > 2)
        self.data = GameData()
        self.seats = [Seat(player) for player in players]
        self.cashservice = CashService(limit)

    def turn(self):

        position = 0
        while sum([x.isWaiting for x in self.players]):
            for seat in self.seats:
                CashService.makeMove(seat, self.seats, self.data.stage, position)
                position += 1