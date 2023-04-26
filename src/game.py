import sys, time 
from gamemap import Board, Player
from agent import *

#In order for the recursion-based minimax functions to work, we must raise the 
#recursion limit slightly higher than the maximum depth of 3 for a minimax agent.
sys.setrecursionlimit(120000)

#Default depths for agents
MINIMAX_DEPTH = 3
ALPHA_BETA_DEPTH = 10

#List of agents for user to choose from
agents = {
        1: ["AlphaBetaOffensive1", AlphaBetaAgentOffensive1, ALPHA_BETA_DEPTH],
        2: ["AlphaBetaDefensive1", AlphaBetaAgentDefensive1, ALPHA_BETA_DEPTH],
        3: ["AlphaBetaOffensive2", AlphaBetaAgentOffensive2, ALPHA_BETA_DEPTH],
        4: ["AlphaBetaDefensive2", AlphaBetaAgentDefensive2, ALPHA_BETA_DEPTH],
        5: ["MinimaxOffensive1", MinimaxAgentOffensive1, MINIMAX_DEPTH],
        6: ["MinimaxDefensive1", MinimaxAgentDefensive1, MINIMAX_DEPTH],
        7: ["AlphaBetaOffensive2WithOpening", AlphaBetaAgentOffensive2WithOpening, ALPHA_BETA_DEPTH],
        8: ["AlphaBetaDefensive2WithOpening", AlphaBetaAgentDefensive2WithOpening, ALPHA_BETA_DEPTH],
        9: ["GreedyOffensive2", GreedyAgentOffensive2, 1]
        }

print("Choose agent A: ")
for key in agents.keys():
    print(f"{key}: {agents[key][0]}")
agenta = agents[int(input())]
print("Choose agent B: ")
for key in agents.keys():
    print(f"{key}: {agents[key][0]}")
agentb = agents[int(input())]

#Updates average time per move
def updateAverageTime(avgTime, newTime, moveCount):
    return ((avgTime + newTime) / moveCount)

class GameInstance:
    #Initializes board, as well as the two given agents.
    def __init__(self, agentA, agentB):
        self.board = Board()
        self.agentA = agentA
        self.agentB = agentB

    #Main loop, will display the board in real time if display=True.
    def gameloop(self, display=True, threePieces=False, long=False):
        avgTimeAgentA = 0
        avgTimeAgentB = 0
        if long:
            self.board = Board(board="Long")
        if display:
            self.board.printBoard()
        turn = Player.A
        while self.board.checkWin(threePieces=threePieces) == 0:
            if turn == self.agentA.player:
                move, timeA = self.agentA.getBestMove(self.board)
                if move:
                    self.board.movePiece(self.agentA.player, (move[0], move[1]), (move[2], move[3]))
                else:
                    print("Player A skips!")
                avgTimeAgentA = updateAverageTime(avgTimeAgentA, timeA, self.board.moveCountA)
                turn = Player.B
                if display:
                    self.board.printBoard()
                    time.sleep(0.1)
            elif turn == self.agentB.player:
                move, timeB = self.agentB.getBestMove(self.board)
                if move:
                    self.board.movePiece(self.agentB.player, (move[0], move[1]), (move[2], move[3]))
                else:
                    print("Player B skips!")
                avgTimeAgentB = updateAverageTime(avgTimeAgentB, timeB, self.board.moveCountB)
                turn = Player.A
                if display:
                    self.board.printBoard()
                    time.sleep(0.1)

            #Prints final board state/statistics
            if self.board.checkWin(threePieces=threePieces) == Player.A:
                if display:
                    print("Player A wins!")
                    print(f"Player A nodes expanded: {self.agentA.nodesExpanded}")
                    print(f"Average nodes expanded player A: {self.agentA.averageNodesExpanded}")
                    print(f"Player B nodes expanded: {self.agentB.nodesExpanded}")
                    print(f"Average nodes expanded player B: {self.agentB.averageNodesExpanded}")
                    print(f"Average time per turn player A: {round(avgTimeAgentA, 6)} seconds")
                    print(f"Average time per turn player B: {round(avgTimeAgentB, 6)} seconds")
                    print(f"Pieces taken by player A: {self.board.initialPiecesPlayerB - self.board.countPlayerB()}")
                    print(f"Pieces taken by player B: {self.board.initialPiecesPlayerA - self.board.countPlayerA()}")
                    print(f"# of moves: {self.board.moveCountA + self.board.moveCountB}")
                    sys.exit(0)
                else:
                    return Player.A
            elif self.board.checkWin(threePieces=threePieces) == Player.B:
                if display:
                    print("Player B wins!")
                    print(f"Player A nodes expanded: {self.agentA.nodesExpanded}")
                    print(f"Average nodes expanded player A: {self.agentA.averageNodesExpanded}")
                    print(f"Player B nodes expanded: {self.agentB.nodesExpanded}")
                    print(f"Average nodes expanded player B: {self.agentB.averageNodesExpanded}")
                    print(f"Average time per turn player A: {round(avgTimeAgentA, 6)} seconds")
                    print(f"Average time per turn player B: {round(avgTimeAgentB, 6)} seconds")
                    print(f"Pieces taken by player A: {self.board.initialPiecesPlayerB - self.board.countPlayerB()}")
                    print(f"Pieces taken by player B: {self.board.initialPiecesPlayerA - self.board.countPlayerA()}")
                    print(f"# of moves: {self.board.moveCountA + self.board.moveCountB}")
                    sys.exit(0)
                else:
                    return Player.B


    #Simulate a given number of games, returns number of wins for each opponent
    def manygames(self, gameno):
        awins = 0
        bwins = 0
        for i in range(gameno):
            win = self.gameloop(display=False)
            if win == Player.A:
                awins += 1
            elif win == Player.B:
                bwins += 1
            self.board = Board()
        print(f"A wins: {awins}")
        print(f"B wins: {bwins}")


#Game loop instances
game = GameInstance(agenta[1](Player.A, agenta[2]), agentb[1](Player.B, agentb[2]))
game.gameloop(threePieces=True)
#game.manygames(100)

