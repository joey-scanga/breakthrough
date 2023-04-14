import sys, time
from gamemap import Board, Player
from agent import *

DEPTH = 3

class GameInstance:
    def __init__(self, agent1, agent2):
        self.board = Board()
        self.agent1 = agent1
        self.agent2 = agent2

    def gameloop(self):
        self.board.printBoard()
        turn = Player.A
        while self.board.checkWin() == 0:
            if turn == self.agent1.player:
                move = self.agent1.getBestMove(self.board, DEPTH)
                self.board.movePiece(self.agent1.player, (move[0], move[1]), (move[2], move[3]))
                turn = Player.B
                self.board.printBoard()
                time.sleep(0.1)
            elif turn == self.agent2.player:
                move = self.agent2.getBestMove(self.board, DEPTH)
                self.board.movePiece(self.agent2.player, (move[0], move[1]), (move[2], move[3]))
                turn = Player.A
                self.board.printBoard()
                time.sleep(0.1)

            if self.board.checkWin() == Player.A:
                print("Player A wins!")
                sys.exit(0)
            elif self.board.checkWin() == Player.B:
                print("Player B wins!")
                sys.exit(0)


            


game = GameInstance(AlphaBetaAgentOffensive1(Player.A), MinimaxAgentOffensive1(Player.B))
game.gameloop()
