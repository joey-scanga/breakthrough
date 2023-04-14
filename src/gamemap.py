import sys
from enum import Enum

class Player(Enum):
    A = 1
    B = 2

'''
Returns a 2D array of characters with the initial board position. 
Blank squares are denoted with a '.', your pieces are denoted by 'O', 
and the AI's pieces are denoted by 'X'.
'''

class Board:
    def __init__(self, board=None):
        if not board:
            self.board = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
                ]
        else:
            self.board = board

    def checkWin(self):
        if self.board[0].contains('O'):
            return 0
        elif self.board[-1].contains('X'):
            return 1
        else: 
            return -1

    def countPlayerA(self):
        count = 0
        for row in self.board:
            for square in row:
                if square == 'O':
                    count += 1
        return count

    def countPlayerB(self):
        count = 0
        for row in self.board:
            for square in row:
                if square == 'X':
                    count += 1
        return count

    def getPlayerARowScore(self):
        score = 8
        for row in self.board:
            if not row.contains('O'):
                score -= 1
        return score

    def getPlayerBRowScore(self):
        score = 8
        for row in self.board[-1::-1]:
            if not row.contains('O'):
                score -= 1
        return score
    
    def checkValidMove(self, player, fromSquare, toSquare):
        if player == Player.A:
            if self.board[fromSquare[0]][fromSquare[1]] != 'O':
                return False
            if self.board[toSquare[0]][toSquare[1]] != '.' or self.board[toSquare[0]][toSquare[1]] != 'X':
                return False
            if fromSquare[0] - toSquare[0] != 1:
                return False
            if abs(fromSquare[1] - toSquare[1]) > 1:
                return False
            return True
        elif player == Player.B:
            if self.board[fromSquare[0]][fromSquare[1]] != 'X':
                return False
            if self.board[toSquare[0]][toSquare[1]] != '.' or self.board[toSquare[0]][toSquare[1]] != 'O':
                return False
            if toSquare[0] - fromSquare[0] != 1:
                return False
            if abs(fromSquare[1] - toSquare[1]) > 1:
                return False
            return True


    '''
    Moves a piece on the board list from one square to another square.
    Checks if the piece is an AI or human piece, and takes in the initial
    piece position and where it's moving to. Returns True if a successful move
    is made, returns False if not.
    '''
    def movePiece(self, player, fromSquare, toSquare):
        if checkValidMove(player, fromSquare, toSquare):
            self.board[fromSquare[0]][fromSquare[1]] = '.'
            if player == Player.A:
                self.board[toSquare[0]][toSquare[1]] = 'O'
            elif player == Player.B:
                self.board[toSquare[0]][toSquare[1]] = 'X'
            if checkWin() == 0:
                print("Human won!")
                sys.exit(0)
            elif checkWin() == 1:
                print("Agent won!")
                sys.exit(0)

        else:
            return False

    def testMove(self, player, fromSquare, toSquare):
        testBoard = Board(self.board)
        testBoard.movePiece(player, fromSquare, toSquare)
        testData = {}         
        testData["countA"] = testBoard.countPlayerA()
        testData["countB"] = testBoard.countPlayerB()
        testData["rowScoreA"] = testBoard.getPlayerARowScore()
        testData["rowScoreB"] = testBoard.getPlayerBRowScore()



