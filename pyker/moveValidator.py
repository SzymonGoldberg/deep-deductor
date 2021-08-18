from pyker.betQueue import Move, CommunityData

class MoveValidator:
    @classmethod
    def moveToCash(cls, commData :CommunityData, playerPot :int, move :Move) -> int:
        return {
            **dict.fromkeys([Move.FOLD, Move.CHECK, Move.QUIT], 0),
            Move.CALL:  commData.maxPot - playerPot,
            Move.BET:   commData.limit,
            Move.RAISE: commData.limit + commData.maxPot - playerPot,
            Move.BLIND: commData.limit / (1 if commData.getNumOfBlinds() else 2)}[move]

    @classmethod
    def availableAndLegalMoves(cls, commData :CommunityData, pot :int, balance :int):
        return list(filter(lambda x: cls.moveToCash(commData,pot,x) < balance, cls.legalMoves(commData, pot)))

    @classmethod
    def legalMoves(cls, commData :CommunityData, playerPot :int) -> list(Move):
        if commData.getNumOfBlinds() < 2:
            return [Move.QUIT, Move.BLIND]
        elif commData.maxPot > playerPot:
            return [Move.FOLD , Move.CALL, Move.RAISE, Move.QUIT] 
        return [Move.FOLD, Move.CHECK, Move.BET, Move.QUIT]