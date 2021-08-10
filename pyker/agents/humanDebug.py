from pyker.agents.base import*
from pyker.moveValidator import MoveValidator

class HumanDebug(Agent):
    def bet(self, communityData, playerPot :int):
        print('name -> ', self.name, '\tbalance -> ', self.balance, ' hand -> ', end = ' ')
        print('\nsmall bets per hands played -> ', self.smallBets/self.handsPlayed if self.handsPlayed > 0 else 0)
        for card in self.hand:
            print(card.asString(), end=' ')

        print("\ncommunity cards ->",end=' ')
        for card in communityData.communityCards:
            print(card.asString(), end=' ')
        print('\n---=======---')

        moves = MoveValidator.legalMoves(communityData, playerPot)
        for action in communityData.actions[-1]:
            print("player -> ", action[0]," action -> ", action[1])

        print("---=======---\nchoose your move: ")
        moveDict = dict()
        for i, move in enumerate(moves):
            moveDict[i] = move
            print("press ", i, " to ", move)
        move = moveDict[int(input("choose action > "))]
        print(chr(27) + "[2J")
        return move

    def showdown(self, winners: list, all: list):
        print(chr(27) + "[2J", '- showdown')
        for player in all:
            print('-- player -> ', player.agent.name, '\thand ->',end=' ')
            for card in player.agent.hand:
                print(card.asString(), end=' ')
            print()
        print('\n- winners')
        for winner in winners:
            print('-- ', winner)
        print()
