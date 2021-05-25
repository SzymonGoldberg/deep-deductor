from pyker.agents.base import*

class HumanDebug(Agent):
    def bet(self, moves, roundData):
        for action in roundData.actions:
            print("player -> ", action[0]," action -> ", action[1])

        print("you are as player ", self.name)
        print("you account: ", self.cash)
        print("you hand: ")
        for card in self.hand:
            print(card.asString(), end=' ')

        print("\ncommunity cards: ")
        for card in roundData.communityCards:
            print(card.asString(), end=' ')

        print("\nchoose your move: ")
        moveDict = dict()
        for i, move in enumerate(moves):
            moveDict[i] = move
            print("press ", i, " to ", move)
        
        return moveDict[int(input("choose action > "))]