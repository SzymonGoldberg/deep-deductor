from pyker.betQueue import Move, CommunityData

class MoveValidator:
    @classmethod
    def moveToCash(cls, communityData :CommunityData, playerPot :int, move :Move) -> int:
        toCashDict = { 
            Move.FOLD:  0,
            Move.CHECK: 0,
            Move.QUIT:  0,
            Move.CALL:  communityData.maxPot - playerPot,
            Move.BET:   communityData.limit,
            Move.RAISE: communityData.limit + communityData.maxPot - playerPot,
            Move.BLIND: communityData.limit / (1 if communityData.getNumOfBlinds() else 2)
        }
        return toCashDict[move]

    @classmethod
    def legalMoves(cls, communityData :CommunityData, playerPot :int) -> list(Move):
        val = []
        if communityData.getNumOfBlinds() < 2:
            val = [Move.QUIT, Move.BLIND]
        elif communityData.maxPot - playerPot > 0:
            val = [Move.FOLD , Move.CALL, Move.RAISE, Move.QUIT] 
        else:
            val = [Move.FOLD, Move.CHECK, Move.BET, Move.QUIT]
        return val