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
        self.communityCards = []        #cards visible for every player
        self.stage = 0                  #current game stage (pref=0, flop=0, turn=0, river=0)
        self.numOfBets = 0              #number of bets in whole round               
        self.localLimit = limit         #limit for every betting tour
        self.pots = [0, 0, 0, 0]        #every tour pot
        self.actions = []               #not done yet - I will use this to save data to disk

    def raiseLimit(self):
        self.localLimit *= 2

    def getCurrentPot(self):
        return self.pots[self.stage]

    def setCurrentPot(self, value):
        self.pots[self.stage] = value

    def moveToCash(self, localPot, move):
        underPot = self.getCurrentPot() - localPot
        toCashDict = { 
            move.FOLD:  0,
            move.CHECK:  0,
            move.QUIT:  0,
            move.CALL: underPot,
            move.BET:   self.localLimit,
            move.RAISE: self.localLimit + underPot,
            move.BLIND: self.localLimit / (1 if self.numOfBets else 2)
        }
        return toCashDict[move]

    def expectedMoves(self, underPot):
        if self.numOfBets in [0, 1]:    #first two bets are small and big blind
            return [Move.BLIND]

        return [Move.FOLD , Move.CALL, Move.RAISE, Move.QUIT
        ] if (underPot > 0) else [Move.FOLD, Move.CHECK, Move.BET, Move.QUIT]

    def affordableMoves(self, seat):
        moves = self.expectedMoves(self.getCurrentPot() - seat.localPot)
        return [x for x in moves if seat.player.cash >= self.moveToCash(seat.localPot, x)]

    def legalMoves(self, seat):
        affordableMoves = self.affordableMoves(seat)
        return [Move.QUIT] if affordableMoves == [Move.FOLD] else affordableMoves
    
    def addAction(self, seat):
        self.actions.append([seat.player.name, seat.move, self.stage])