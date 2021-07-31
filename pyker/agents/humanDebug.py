from pyker.agents.base import*
from pyker.moveValidator import MoveValidator

class HumanDebug(Agent):
    def bet(self, communityData :CommunityData, playerPot :int):
        moves = MoveValidator.legalMoves(communityData, playerPot)
        for action in communityData.actions[-1]:
            print("player -> ", action[0]," action -> ", action[1])

        print("you are as player ", self.name)
        print("you account: ", self.balance)
        print("you hand: ")
        for card in self.hand:
            print(card.asString(), end=' ')

        print("\ncommunity cards: ")
        for card in communityData.communityCards:
            print(card.asString(), end=' ')

        print("\nchoose your move: ")
        moveDict = dict()
        for i, move in enumerate(moves):
            moveDict[i] = move
            print("press ", i, " to ", move)
        
        return moveDict[int(input("choose action > "))]