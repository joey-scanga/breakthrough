from gamemap import Board, Player
from openings import openingsList, setMoveDirection
import random, math

'''Interfaces'''
class IAgent:
    def __init__(self, player, depth):
        self.player = player
        self.depth = depth
        self.movequeue = []

    def evaluate(self, board):
        pass

    def getBestMove(self, board, depth):
        pass

    def getMoves(self, board):
        if self.player == Player.A:
            moves = board.getMovesForPlayerA()
        elif self.player == Player.B:
            moves = board.getMovesForPlayerB()
        return moves

    def getOpponentMoves(self, board):
        if self.player == Player.A:
            moves = board.getMovesForPlayerB()
        elif self.player == Player.B:
            moves = board.getMovesForPlayerA()
        return moves

    def makeMove(self, board, move):
        return board.testMoveReturningBoard(self.player, (move[0], move[1]), (move[2], move[3]))

    def makeOpponentMove(self, board, move):
        return board.testMoveReturningBoard(-1 * self.player.value, (move[0], move[1]), (move[2], move[3]))

class IMinimax(IAgent):
    def minimax(self, board, player):
        rootBoard = board
        currentNodesExpanded = 0
        stack = [(board, self.depth, player)]
        while stack:
            board, depth, player = stack.pop()
            
            if player == self.player and depth > 0:
                bestValue = -math.inf
                for move in self.getMoves(board):
                    newBoard = board.testMoveReturningBoard(self.player, (move[0], move[1]), (move[2], move[3])) 
                    stack.append((newBoard, depth-1, -1 * self.player.value))
                    currentNodesExpanded += 1
                    rootBoard.incrementNodesExpanded(self.player)
                    value = self.evaluate(newBoard)
                    if value > bestValue:
                        bestValue = value
                if not stack:
                    rootBoard.updateMovingNodeAverage(self.player, currentNodesExpanded)
                    return bestValue

            elif player != self.player and depth > 0:
                bestValue = math.inf
                for move in self.getOpponentMoves(board):
                    newBoard = board.testMoveReturningBoard(-1 * self.player.value, (move[0], move[1]), (move[2], move[3]))
                    stack.append((newBoard, depth-1, self.player.value))
                    currentNodesExpanded += 1
                    rootBoard.incrementNodesExpanded(self.player)
                    value = self.evaluate(newBoard)
                    if value < bestValue:
                        bestValue = value
                if not stack:
                    rootBoard.updateMovingNodeAverage(self.player, currentNodesExpanded)
                    return bestValue
        


    def getBestMove(self, board):
        board.incrementMoveCount(self.player)
        if self.movequeue:
            return self.movequeue.pop()
        bestValue = self.minimax(board, self.player)
        moves = self.getMoves(board)
        bestMoves = []

        #Skips turn if no valid moves
        if not moves:
            return

        for move in moves:
            newBoard = self.makeMove(board, move)
            value = self.evaluate(newBoard)
            if value == bestValue:
                bestMoves.append(move)

       
        if not bestMoves:
            return random.choice(self.getMoves(board))

        bestMove = random.choice(bestMoves)
        return bestMove

class IAlphaBeta(IAgent):
    # Alpha-beta pruning minimax function
    def alphaBeta(self, board, player, alpha, beta):
        rootBoard = board
        currentNodesExpanded = 0
        stack = [(board, self.depth, alpha, beta, player)]
        bestValue = None

        while stack:
            board, depth, alpha, beta, player = stack.pop()

            if player == self.player and depth > 0:
                bestValue = -math.inf
                for move in self.getMoves(board):
                    newBoard = board.testMoveReturningBoard(self.player, (move[0], move[1]), (move[2], move[3]))
                    stack.append((newBoard, depth-1, alpha, beta, -1 * self.player.value))
                    currentNodesExpanded += 1
                    rootBoard.incrementNodesExpanded(self.player)
                    value = self.evaluate(newBoard)
                    bestValue = max(bestValue, value)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        stack.pop()
                if not stack:
                    rootBoard.updateMovingNodeAverage(self.player, currentNodesExpanded)
                    return bestValue
            elif player != self.player and depth > 0:
                bestValue = math.inf
                for move in self.getOpponentMoves(board):
                    newBoard = board.testMoveReturningBoard(-1 * self.player.value, (move[0], move[1]), (move[2], move[3]))
                    stack.append((newBoard, depth-1, alpha, beta, self.player))
                    currentNodesExpanded += 1
                    rootBoard.incrementNodesExpanded(self.player)
                    value = self.evaluate(newBoard)
                    bestValue = min(bestValue, value)
                    beta = min(beta, value)
                    if alpha >= beta:
                        stack.pop()
                if not stack:            
                    rootBoard.updateMovingNodeAverage(self.player, currentNodesExpanded)
                    return bestValue

        


    def getBestMove(self, board):
        board.incrementMoveCount(self.player)
        if self.movequeue:
            return self.movequeue.pop()
        bestValue = self.alphaBeta(board, self.player, math.inf, -math.inf)
        bestMoves = []
        moves = self.getMoves(board)

        if not moves:
            return

        #Skips turn if no valid moves
        for move in moves:
            newBoard = self.makeMove(board, move)
            value = self.evaluate(newBoard)
            if value == bestValue:
                bestMoves.append(move)
       
        if not bestMoves:
            return random.choice(self.getMoves(board))

        bestMove = random.choice(bestMoves)
        return bestMove

'''Agents'''
class AlphaBetaAgentOffensive1(IAlphaBeta):
    def evaluate(self, board):
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) + random.random()
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) + random.random()

class AlphaBetaAgentDefensive1(IAlphaBeta):
    def evaluate(self, board):
        if self.player == Player.A:
            countA = board.countPlayerA()
            return (2 * countA) + random.random()
        elif self.player == Player.B:
            countB = board.countPlayerB()
            return (2 * countB) + random.random()

class AlphaBetaAgentOffensive2(IAlphaBeta):
    def evaluate(self, board):
        rowScoreA = board.getPlayerARowScore()
        rowScoreB = board.getPlayerBRowScore()
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) - 2 * rowScoreA
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) - 2 * rowScoreB

class AlphaBetaAgentDefensive2(IAlphaBeta):
    def evaluate(self, board):
        rowScoreA = board.getPlayerARowScore()
        rowScoreB = board.getPlayerBRowScore()
        if self.player == Player.A:
            countA = board.countPlayerB()
            return (2 * countA) - 2 * rowScoreB
        elif self.player == Player.B:
            countB = board.countPlayerA()
            return (2 * countB) - 2 * rowScoreA
    
class AlphaBetaAgentOffensive2WithOpening(IAlphaBeta):
    def __init__(self, player, depth):
        self.player = player
        self.depth = depth
        self.movequeue = setMoveDirection(self.player, random.choice(openingsList))
    def evaluate(self, board):
        rowScoreA = board.getPlayerARowScore()
        rowScoreB = board.getPlayerBRowScore()
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) + (20 * rowScoreA) - (15 * rowScoreB) + random.random()
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) + (20 * rowScoreB) - (15 * rowScoreB) + random.random()

class AlphaBetaAgentDefensive2WithOpening(IAlphaBeta):
    def __init__(self, player, depth):
        self.player = player
        self.depth = depth
        self.movequeue = setMoveDirection(self.player, random.choice(openingsList))
    def evaluate(self, board):
        if self.player == Player.A:
            countA = board.countPlayerB()
            rowScoreA = board.getPlayerARowScore()
            return (2 * countA) + (3 * rowScoreA) + random.random()
        elif self.player == Player.B:
            countB = board.countPlayerA()
            rowScoreB = board.getPlayerBRowScore()
            return (2 * countB) + (3 * rowScoreB) + random.random()

class MinimaxAgentOffensive1(IMinimax):
    def evaluate(self, board):
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) + random.random()
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) + random.random()
            
class MinimaxAgentDefensive1(IMinimax):
    def evaluate(self, board):
        if self.player == Player.A:
            countA = board.countPlayerA()
            return (2 * countA) + random.random()
        elif self.player == Player.B:
            countB = board.countPlayerB()
            return (2 * countB) + random.random()


    
        
        
        



