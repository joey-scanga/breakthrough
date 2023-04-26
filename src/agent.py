from gamemap import Board, Player
from openings import openingsList, setMoveDirection
import random, math, time

'''Interfaces'''
class IAgent:
    def __init__(self, player, depth):
        self.player = player
        self.depth = depth
        self.movequeue = [] #Only for agents with opening strategies
        self.nodesExpanded = 0
        self.averageNodesExpanded = 0
    
    #Evaluation function to be implemented by class children
    def evaluate(self, board):
        pass

    #Returns the best move found by minimax, alpha-beta pruning, or greedy search. Implemented
    #by class children.
    def getBestMove(self, board, depth=1):
        pass
    
    #Returns all possible moves for this player given a board state. 
    def getMoves(self, board):
        if self.player == Player.A:
            moves = board.getMovesForPlayerA()
        elif self.player == Player.B:
            moves = board.getMovesForPlayerB()
        return moves

    #Returns all possible opponent moves given a board state. 
    def getOpponentMoves(self, board):
        if self.player == Player.A:
            moves = board.getMovesForPlayerB()
        elif self.player == Player.B:
            moves = board.getMovesForPlayerA()
        return moves

    #Theoretically makes a move from one square to another, returning the new board state.
    def makeMove(self, board, move):
        return board.testMoveReturningBoard(self.player, (move[0], move[1]), (move[2], move[3]))

    #Similar to makeMove() but moves an opponent piece.
    def makeOpponentMove(self, board, move):
        return board.testMoveReturningBoard(-1 * self.player.value, (move[0], move[1]), (move[2], move[3]))

class IGreedy(IAgent):
    #Will evaluate all moves at a depth of 1, evaluate them, and return the move with the highest
    #eval score. Keeps track of nodes expanded, time to make the move, and average nodes expanded.
    def getBestMove(self, board):
        board.incrementMoveCount(self.player)
        startTime = time.time()
        bestValue = -math.inf
        bestMove = None
        for move in self.getMoves(board):
            self.nodesExpanded += 1
            newBoard = self.makeMove(board, move) 
            if self.evaluate(newBoard) > bestValue:
                bestValue = self.evaluate(newBoard)
                bestMove = move
            bestValue = max(self.evaluate(newBoard), bestValue)
        endTime = time.time()
        if self.player == Player.A:
            self.averageNodesExpanded = self.nodesExpanded / board.moveCountA
        else:
            self.averageNodesExpanded = self.nodesExpanded / board.moveCountB
        return (bestMove, endTime - startTime)

class IMinimax(IAgent):
    #Finds the best move choice according to an eval function at a given depth (default is 3). 
    #Keeps track of nodes expanded.
    def minimax(self, depth, board, player):
        if depth == 0:
            return self.evaluate(board)

        if player == self.player:
            bestValue = -math.inf
            for move in self.getMoves(board):
                newBoard = board.testMoveReturningBoard(self.player, (move[0], move[1]), (move[2], move[3])) 
                self.nodesExpanded += 1
                value = self.minimax(depth-1, newBoard, -1 * self.player)
                bestValue = max(bestValue, value)
            return bestValue

        else:
            bestValue = math.inf
            for move in self.getOpponentMoves(board):
                newBoard = board.testMoveReturningBoard(-1 * self.player, (move[0], move[1]), (move[2], move[3]))
                self.nodesExpanded += 1
                value = self.minimax(depth-1, newBoard, self.player)
                bestValue = min(bestValue, value)
            return bestValue

    #Uses above minimax function to determine the best move choice at the current board state, 
    #given an eval function. Keeps track of time to make move and average number of nodes 
    #expanded.
    def getBestMove(self, board):
        board.incrementMoveCount(self.player)
        startTime = time.time()
        if self.movequeue:
            endTime = time.time()
            return (self.movequeue.pop(), endTime - startTime)
        depth = self.depth
        player = self.player
        bestValue = self.minimax(depth, board, self.player)
        moves = self.getMoves(board)
        bestMoves = []

        #Skips turn if no valid moves
        if not moves:
            endTime = time.time()
            return (None, (endTime - startTime))
        
        for move in moves:
            newBoard = self.makeMove(board, move)
            value = self.minimax(depth-1, newBoard, -player)
            if value == bestValue:
                bestMoves.append(move)

        if self.player == Player.A:
            self.averageNodesExpanded = self.nodesExpanded / board.moveCountA
        else:
            self.averageNodesExpanded = self.nodesExpanded / board.moveCountB

        if not bestMoves:
            endTime = time.time()
            return (random.choice(self.getMoves(board)), (endTime - startTime))
       
        bestMove = random.choice(bestMoves)
        endTime = time.time()
        return (bestMove, endTime - startTime)

class IAlphaBeta(IAgent):
    # Alpha-beta pruning minimax function, similar to minimax but includes pruning.
    def alphaBeta(self, board, player, depth, alpha, beta):
        if depth == 0:
            return self.evaluate(board)

        if player == self.player:
            bestValue = -math.inf
            for move in self.getMoves(board):
                newBoard = board.testMoveReturningBoard(self.player, (move[0], move[1]), (move[2], move[3]))
                self.nodesExpanded += 1
                value = self.alphaBeta(newBoard, -self.player, depth-1, alpha, beta)
                bestValue = max(value, bestValue)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return bestValue

        else:
            bestValue = math.inf
            for move in self.getOpponentMoves(board):
                newBoard = board.testMoveReturningBoard(-self.player, (move[0], move[1]), (move[2], move[3]))
                self.nodesExpanded += 1
                value = self.alphaBeta(newBoard, self.player, depth-1, alpha, beta)
                bestValue = min(value, bestValue)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return bestValue

    #Same as minimax getBestMove but uses alphaBeta()
    def getBestMove(self, board):
        board.incrementMoveCount(self.player)
        startTime = time.time()
        if self.movequeue:
            endTime = time.time()
            return (self.movequeue.pop(), endTime - startTime)
        player = self.player
        depth = self.depth
        alpha = math.inf
        beta = -math.inf
        bestValue = self.alphaBeta(board, player, depth, alpha, beta)
        bestMoves = []
        moves = self.getMoves(board)

        if not moves:
            endTime = time.time()
            return (None, endTime - startTime)

        #Skips turn if no valid moves
        for move in moves:
            newBoard = self.makeMove(board, move)
            value = self.alphaBeta(newBoard, -player, depth-1, alpha, beta)
            if value == bestValue:
                bestMoves.append(move)

        if self.player == Player.A:
            self.averageNodesExpanded = self.nodesExpanded / board.moveCountA
        else:
            self.averageNodesExpanded = self.nodesExpanded / board.moveCountB

        if not bestMoves:
            endTime = time.time()
            return (random.choice(self.getMoves(board)), endTime - startTime)

        bestMove = random.choice(bestMoves)
        endTime = time.time()
        return (bestMove, endTime - startTime)

'''Agents'''
#This agent uses the default offensive strategy provided.
class AlphaBetaAgentOffensive1(IAlphaBeta):
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() == 0:
            return -math.inf
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) + random.random()
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) + random.random()

#This agent uses the default defensive strategy provided.
class AlphaBetaAgentDefensive1(IAlphaBeta):
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() != 0:
            return -math.inf
        if self.player == Player.A:
            countA = board.countPlayerA()
            return (2 * countA) + random.random()
        elif self.player == Player.B:
            countB = board.countPlayerB()
            return (2 * countB) + random.random()

#Greedy agent, implementing AlphaBetaAgentOffensive2's strategy.
class GreedyAgentOffensive2(IGreedy):
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() != 0:
            return -math.inf
        rowScoreA = board.getPlayerARowScore()
        rowScoreB = board.getPlayerBRowScore()
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) - 2 * rowScoreA
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) - 2 * rowScoreB

#Improves upon the level 1 offensive strategy by tending to make moves that also move pieces
#as far up the board as possible.
class AlphaBetaAgentOffensive2(IAlphaBeta):
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() != 0:
            return -math.inf
        rowScoreA = board.getPlayerARowScore()
        rowScoreB = board.getPlayerBRowScore()
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) - 2 * rowScoreA
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) - 2 * rowScoreB

#Improves upon the level 1 defensive strategy by tending to make moves that also move pieces
#as far up the board as possible.
class AlphaBetaAgentDefensive2(IAlphaBeta):
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() != 0:
            return -math.inf
        rowScoreA = board.getPlayerARowScore()
        rowScoreB = board.getPlayerBRowScore()
        if self.player == Player.A:
            countA = board.countPlayerB()
            return (2 * countA) - 2 * rowScoreB
        elif self.player == Player.B:
            countB = board.countPlayerA()
            return (2 * countB) - 2 * rowScoreA

#This agent utilizes the same strategy as AlphaBetaAgentOffensive2, but has a choice from a 
#couple of popular Breakthrough openings that it will perform before doing any alpha-beta pruning.
class AlphaBetaAgentOffensive2WithOpening(IAlphaBeta):
    def __init__(self, player, depth):
        self.player = player
        self.depth = depth
        self.movequeue = setMoveDirection(self.player, random.choice(openingsList))
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() != 0:
            return -math.inf
        rowScoreA = board.getPlayerARowScore()
        rowScoreB = board.getPlayerBRowScore()
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) + (20 * rowScoreA) - (15 * rowScoreB) + random.random()
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) + (20 * rowScoreB) - (15 * rowScoreB) + random.random()

#This agent utilizes the same strategy as AlphaBetaAgentDefensive2, but has a choice from a 
#couple of popular Breakthrough openings that it will perform before doing any alpha-beta pruning.
class AlphaBetaAgentDefensive2WithOpening(IAlphaBeta):
    def __init__(self, player, depth):
        self.player = player
        self.depth = depth
        self.movequeue = setMoveDirection(self.player, random.choice(openingsList))
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() != 0:
            return -math.inf
        if self.player == Player.A:
            countA = board.countPlayerB()
            rowScoreA = board.getPlayerARowScore()
            return (2 * countA) + (3 * rowScoreA) + random.random()
        elif self.player == Player.B:
            countB = board.countPlayerA()
            rowScoreB = board.getPlayerBRowScore()
            return (2 * countB) + (3 * rowScoreB) + random.random()

#Minimax agent using the default offensive strategy.
class MinimaxAgentOffensive1(IMinimax):
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() != 0:
            return -math.inf
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) + random.random()
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) + random.random()
           
#Minimax agent using the default defensive strategy.
class MinimaxAgentDefensive1(IMinimax):
    def evaluate(self, board):
        if board.checkWin() == self.player:
            return math.inf
        elif board.checkWin() != 0:
            return -math.inf
        if self.player == Player.A:
            countA = board.countPlayerA()
            return (2 * countA) + random.random()
        elif self.player == Player.B:
            countB = board.countPlayerB()
            return (2 * countB) + random.random()


    
        
        
        



