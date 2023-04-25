import sys, time 
from gamemap import Board, Player
from agent import *

MINIMAX_DEPTH = 3
ALPHA_BETA_DEPTH = 6

agents = {
        1: ["AlphaBetaOffensive1", AlphaBetaAgentOffensive1, ALPHA_BETA_DEPTH],
        2: ["AlphaBetaDefensive1", AlphaBetaAgentDefensive1, ALPHA_BETA_DEPTH],
        3: ["AlphaBetaOffensive2", AlphaBetaAgentOffensive2, ALPHA_BETA_DEPTH],
        4: ["AlphaBetaDefensive2", AlphaBetaAgentDefensive2, ALPHA_BETA_DEPTH],
        5: ["MinimaxOffensive1", MinimaxAgentOffensive1, MINIMAX_DEPTH],
        6: ["MinimaxDefensive1", MinimaxAgentDefensive1, MINIMAX_DEPTH],
        7: ["AlphaBetaOffensive2WithOpening", AlphaBetaAgentOffensive2WithOpening, ALPHA_BETA_DEPTH],
        8: ["AlphaBetaDefensive2WithOpening", AlphaBetaAgentDefensive2WithOpening, ALPHA_BETA_DEPTH]
        }

print("Choose agent A: ")
for key in agents.keys():
    print(f"{key}: {agents[key][0]}")
agenta = agents[int(input())]
print("Choose agent B: ")
for key in agents.keys():
    print(f"{key}: {agents[key][0]}")
agentb = agents[int(input())]

class GameInstance:
    def __init__(self, agent1, agent2):
        self.board = Board()
        self.agent1 = agent1
        self.agent2 = agent2

    #Main loop
    def gameloop(self, display=True):
        if display:
            self.board.printBoard()
        turn = Player.A
        while self.board.checkWin() == 0:
            if turn == self.agent1.player:
                move = self.agent1.getBestMove(self.board)
                if move:
                    self.board.movePiece(self.agent1.player, (move[0], move[1]), (move[2], move[3]))
                else:
                    print("Player A skips!")
                turn = Player.B
                if display:
                    self.board.printBoard()
                    time.sleep(0.1)
            elif turn == self.agent2.player:
                move = self.agent2.getBestMove(self.board)
                if move:
                    self.board.movePiece(self.agent2.player, (move[0], move[1]), (move[2], move[3]))
                else:
                    print("Player B skips!")
                turn = Player.A
                if display:
                    self.board.printBoard()
                    time.sleep(0.1)
            
            if self.board.checkWin() == Player.A:
                if display:
                    print("Player A wins!")
                    print(f"# of moves: {self.board.moveCountA + self.board.moveCountB}")
                    print(f"Player A nodes expanded: {self.board.nodesExpandedPlayerA}")
                    print(f"Average nodes expanded player A: {self.board.averageNodesExpandedPlayerA}")
                    print(f"Player B nodes expanded: {self.board.nodesExpandedPlayerB}")
                    print(f"Average nodes expanded player B: {self.board.averageNodesExpandedPlayerB}")
                    sys.exit(0)
                else:
                    return Player.A
            elif self.board.checkWin() == Player.B:
                if display:
                    print("Player B wins!")
                    print(f"# of moves: {self.board.moveCountA + self.board.moveCountB}")
                    print(f"Player A nodes expanded: {self.board.nodesExpandedPlayerA}")
                    print(f"Average nodes expanded player A: {self.board.averageNodesExpandedPlayerA}")
                    print(f"Player B nodes expanded: {self.board.nodesExpandedPlayerB}")
                    print(f"Average nodes expanded player B: {self.board.averageNodesExpandedPlayerB}")
                    sys.exit(0)
                else:
                    return Player.B

            #breakpoint()

            
    #Simulate a number of games
    def manygames(self, gameno):
        awins = 0
        bwins = 0
        stalemates = 0
        for i in range(gameno):
            win = self.gameloop(display=False)
            if win == Player.A:
                awins += 1
            elif win == Player.B:
                bwins += 1
            self.board = Board()
        print(f"A wins: {awins}")
        print(f"B wins: {bwins}")
        print(f"Stalemates: {stalemates}")


game = GameInstance(agenta[1](Player.A, agenta[2]), agentb[1](Player.B, agentb[2]))
game.gameloop()
#game.manygames(100)

