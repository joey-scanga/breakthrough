import sys, copy 
from enum import IntEnum

#This IntEnum instance keeps track of which player is which, by assigning Players A and B to 1 and
#-1, respectively. This allows for easily switching players by negating the one given.
class Player(IntEnum):
    A = 1
    B = -1

#Board object responsible for keeping track of game state.
class Board:
    #Board initializer.
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

        #Long board option, if board="Long".
        elif board == "Long":
            self.board = [['X', 'X', 'X', 'X', 'X'],
                          ['X', 'X', 'X', 'X', 'X'],
                          ['.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.'],
                          ['.', '.', '.', '.', '.'],
                          ['O', 'O', 'O', 'O', 'O'],
                          ['O', 'O', 'O', 'O', 'O']]

        else:
            self.board = board
        
        #Various game statistics to keep track of during play.
        self.initialPiecesPlayerA = self.countPlayerA()
        self.initialPiecesPlayerB = self.countPlayerB()
        self.nodesExpandedPlayerA = 0
        self.nodesExpandedPlayerB = 0
        self.averageNodesExpandedPlayerA = 0
        self.averageNodesExpandedPlayerB = 0
        self.averageTimePlayerA = 0
        self.averageTimePlayerB = 0
        self.moveCountA = 0
        self.moveCountB = 0

    #Checks if a player has won based on the current ruleset.
    def checkWin(self, threePieces=False):
        if threePieces:
            if self.board[0].count('O') >= 3:
                return Player.A
            elif self.board[-1].count('X') >= 3:
                return Player.B
            else:
                return 0

        if 'O' in self.board[0]:
            return Player.A
        elif 'X' in self.board[-1]:
            return Player.B
        else: 
            return 0

    #Increments move count for given player. 
    def incrementMoveCount(self, player):
        if player == Player.A:
            self.moveCountA += 1
        else:
            self.moveCountB += 1

    #Returns number of player A's pieces.
    def countPlayerA(self):
        count = 0
        for row in self.board:
            for square in row:
                if square == 'O':
                    count += 1
        return count
    
    #Returns number of player B's pieces.
    def countPlayerB(self):
        count = 0
        for row in self.board:
            for square in row:
                if square == 'X':
                    count += 1
        return count

    #Returns list of valid moves for player A.
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

    #Returns list of valid moves for player B.
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

    #Returns the number of rows away from home the furthest piece is. Used in level 2 eval
    #function.
    def getPlayerARowScore(self):
        score = 7
        for row in self.board[1:]:
            if not 'O' in row:
                score -= 1
       
        return score

    #Returns the number of rows away from home the furthest piece is. Used in level 2 eval
    #function.
    def getPlayerBRowScore(self):
        score = 7
        for row in self.board[-2::-1]:
            if not 'X' in row:
                score -= 1

        return score
    
    #Returns True if a move is valid.
    def checkValidMove(self, player, fromSquare, toSquare):
        if -1 in fromSquare or -1 in toSquare or len(self.board) == fromSquare[0] or len(self.board[0]) == fromSquare[1] or len(self.board) == toSquare[0] or len(self.board[0]) == toSquare[1]:
            return False
        if player == Player.A:
            if self.board[fromSquare[0]][fromSquare[1]] != 'O':
                return False
            if self.board[toSquare[0]][toSquare[1]] == 'O':
                return False
            if self.board[toSquare[0]][toSquare[1]] == 'X' and abs(fromSquare[1] - toSquare[1]) == 0:
                return False 
            if fromSquare[0] - toSquare[0] != 1:
                return False
            if abs(fromSquare[1] - toSquare[1]) > 1:
                return False
            return True
        elif player == Player.B:
            if self.board[fromSquare[0]][fromSquare[1]] != 'X':
                return False
            if self.board[toSquare[0]][toSquare[1]] == 'X':
                return False
            if self.board[toSquare[0]][toSquare[1]] == '0' and abs(fromSquare[1] - toSquare[1]) == 0:
                return False 
            if toSquare[0] - fromSquare[0] != 1:
                return False
            if abs(fromSquare[1] - toSquare[1]) > 1:
                return False
            return True

    #If valid, moves a piece from one square to another.
    def movePiece(self, player, fromSquare, toSquare):
        if self.checkValidMove(player, fromSquare, toSquare):
            self.board[fromSquare[0]][fromSquare[1]] = '.'
            if player == Player.A:
                self.board[toSquare[0]][toSquare[1]] = 'O'
            elif player == Player.B:
                self.board[toSquare[0]][toSquare[1]] = 'X'
        else:
            return False
    

    #Given a move, will return a copy of the current board after the move is made.
    def testMoveReturningBoard(self, player, fromSquare, toSquare):
        testBoard = copy.deepcopy(self)
        testBoard.movePiece(player, fromSquare, toSquare)
        return testBoard

    #Prints out current board state.
    def printBoard(self):
        for row in self.board:
            print(' '.join(row)+'\n')
        print()




