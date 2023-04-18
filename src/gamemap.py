import sys, copy, pprint
from enum import Enum

class Player(Enum):
    A = 1
    B = -1

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
        if 'O' in self.board[0]:
            return Player.A
        elif 'X' in self.board[-1]:
            return Player.B
        else: 
            return 0

    def getColumnsForPlayerA(self):
        columnScore = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i+1 <= 7 and i-1 >= 0:
                    if self.board[i][j] == 'O' and self.board[i+1][j] == 'O' and self.board[i-1][j] == 'O':
                        columnScore += 2
                    elif self.board[i][j] == 'O' and self.board[i+1][j] == 'O':
                        columnScore += 1
                    elif self.board[i][j] == 'O' and self.board[i-1][j] == 'O':
                        columnScore += 1
        return columnScore
                
    def getColumnsForPlayerB(self):
        columnScore = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i+1 <= 7 and i-1 >= 0:
                    if self.board[i][j] == 'X' and self.board[i+1][j] == 'X' and self.board[i-1][j] == 'O':
                        columnScore += 2
                    elif self.board[i][j] == 'X' and self.board[i+1][j] == 'X':
                        columnScore += 1
                    elif self.board[i][j] == 'X' and self.board[i-1][j] == 'X':
                        columnScore += 1
        return columnScore

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

    def getMovesForPlayerA(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'O':
                    if self.checkValidMove(Player.A, (i, j), (i-1, j)):
                        moves.append((i, j, i-1, j))
                    if self.checkValidMove(Player.A, (i, j), (i-1, j-1)):
                        moves.append((i, j, i-1, j-1))
                    if self.checkValidMove(Player.A, (i, j), (i-1, j+1)):
                        moves.append((i, j, i-1, j+1))
        return moves


    def getMovesForPlayerB(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'X':
                    if self.checkValidMove(Player.B, (i, j), (i+1, j)):
                        moves.append((i, j, i+1, j))
                    if self.checkValidMove(Player.B, (i, j), (i+1, j-1)):
                        moves.append((i, j, i+1, j-1))
                    if self.checkValidMove(Player.B, (i, j), (i+1, j+1)):
                        moves.append((i, j, i+1, j+1))
        return moves

    def getPlayerARowScore(self):
        if '0' in self.board[0]:
            return 10000000
        elif 'O' in self.board[1]:
            return 5000000
        score = 7
        for row in self.board[1:]:
            if not 'O' in row:
                score -= 1
       
        return score

    def getPlayerBRowScore(self):
        if 'X' in self.board[-1]:
            return 10000000
        elif 'X' in self.board[-2]:
            return 5000000
        score = 7
        for row in self.board[-2::-1]:
            if not 'X' in row:
                score -= 1

        return score
    
    def checkValidMove(self, player, fromSquare, toSquare):
        if -1 in fromSquare or -1 in toSquare or 8 in fromSquare or 8 in toSquare:
            return False
        if player == Player.A:
            if self.board[fromSquare[0]][fromSquare[1]] != 'O':
                return False
            if self.board[toSquare[0]][toSquare[1]] != '.':
                return False
            if self.board[toSquare[0]][toSquare[1]] == 'X' and abs(fromSquare[1] - toSquare[1]) != 1:
                return False 
            if fromSquare[0] - toSquare[0] != 1:
                return False
            if abs(fromSquare[1] - toSquare[1]) > 1:
                return False
            return True
        elif player == Player.B:
            if self.board[fromSquare[0]][fromSquare[1]] != 'X':
                return False
            if self.board[toSquare[0]][toSquare[1]] != '.':
                return False
            if self.board[toSquare[0]][toSquare[1]] == '0' and abs(fromSquare[1] - toSquare[1]) != 1:
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
        if self.checkValidMove(player, fromSquare, toSquare):
            self.board[fromSquare[0]][fromSquare[1]] = '.'
            if player == Player.A:
                self.board[toSquare[0]][toSquare[1]] = 'O'
            elif player == Player.B:
                self.board[toSquare[0]][toSquare[1]] = 'X'

        else:
            return False

    def testCurrentBoard(self):
        testData = {}
        testData["countA"] = testBoard.countPlayerA()
        testData["countB"] = testBoard.countPlayerB()
        testData["rowScoreA"] = testBoard.getPlayerARowScore()
        testData["rowScoreB"] = testBoard.getPlayerBRowScore()
        return testData

    def testMoveReturningBoard(self, player, fromSquare, toSquare):
        testBoard = copy.deepcopy(self)
        testBoard.movePiece(player, fromSquare, toSquare)
        return testBoard

    def testMoveReturningData(self, player, fromSquare, toSquare):
        testBoard = Board(self.board)
        testBoard.movePiece(player, fromSquare, toSquare)
        testData = {}         
        testData["countA"] = testBoard.countPlayerA()
        testData["countB"] = testBoard.countPlayerB()
        testData["rowScoreA"] = testBoard.getPlayerARowScore()
        testData["rowScoreB"] = testBoard.getPlayerBRowScore()
        return testData

    def printBoard(self):
        for row in self.board:
            print(' '.join(row)+'\n')
        print()




