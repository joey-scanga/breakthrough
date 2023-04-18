import sys, time, pprint
from gamemap import Board, Player
from agent import *

DEPTH = 3

pp = pprint.PrettyPrinter(indent=4)

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
                if move:
                    self.board.movePiece(self.agent1.player, (move[0], move[1]), (move[2], move[3]))
                else:
                    print("Player A skips!")
                turn = Player.B
                self.board.printBoard()
                time.sleep(0.1)
            elif turn == self.agent2.player:
                move = self.agent2.getBestMove(self.board, DEPTH)
                if move:
                    self.board.movePiece(self.agent2.player, (move[0], move[1]), (move[2], move[3]))
                else:
                    print("Player B skips!")
                turn = Player.A
                self.board.printBoard()
                time.sleep(0.1)
            
            if self.board.checkWin() == Player.A:
                print("Player A wins!")
                sys.exit(0)
            elif self.board.checkWin() == Player.B:
                print("Player B wins!")
                sys.exit(0)

    def manygames(self, gameno):
        awins = 0
        bwins = 0
        for i in range(gameno):
            self.board = Board()
            turn = Player.A
            while self.board.checkWin() == 0:
                if turn == self.agent1.player:
                    move = self.agent1.getBestMove(self.board, DEPTH)
                    self.board.movePiece(self.agent1.player, (move[0], move[1]), (move[2], move[3]))
                    turn = Player.B
                elif turn == self.agent2.player:
                    move = self.agent2.getBestMove(self.board, DEPTH)
                    self.board.movePiece(self.agent2.player, (move[0], move[1]), (move[2], move[3]))
                    turn = Player.A
                
                if self.board.checkWin() == Player.A:
                    awins += 1
                elif self.board.checkWin() == Player.B:
                    bwins += 1

        print(f"A wins: {awins}")
        print(f"B wins: {bwins}")



game = GameInstance(AlphaBetaAgentOffensive2(Player.A), AlphaBetaAgentDefensive1(Player.B))
#game.gameloop()
game.manygames(100)
