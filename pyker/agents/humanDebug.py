from pyker.agents.base import*

class HumanDebug(Agent):
    def bet(self, moves, roundData):
        print("you are as player ", self.name)
        print("you account: ", self.cash)
        print("you hand: ")
        for card in self.hand:
            print(card.asString())

        print("choose your move: ")
        moveDict = dict()
        for i, move in enumerate(moves):
            moveDict[i] = move
            print("press ", i, " to ", move)
        
        return moveDict[int(input("choose action > "))]


