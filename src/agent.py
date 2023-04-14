from gamemap import Board, Player
import random, math

class MinimaxAgentOffensive1():
    def __init__(self, player):
        self.player = player

    def evaluate(self, board):
        if self.player == Player.A:
            countB = board.countPlayerB()
            return 2 * (30 - countB) + random.random()
        elif self.player == Player.B:
            countA = board.countPlayerA()
            return 2 * (30 - countA) + random.random()
            
    def minimax(self, board, player, depth):
        stack = [(board, depth, player)]
        while stack:
            board, depth, player = stack.pop()
            if depth == 0:
                return self.evaulate(board)
            
            if player == self.player:
                bestValue = -math.inf
                for move in self.getMoves(board):
                    newBoard = board.testMoveReturningBoard(self.player, (move[0], move[1]), (move[2], move[3])) 
                    stack.append((newBoard, depth-1, -1 * self.player.value))
                    value = self.evaluate(newBoard)
                    if value > bestValue:
                        bestValue = value
                        bestMove = move
                if depth == 2:
                    return bestMove
                return bestValue

            else:
                bestValue = math.inf
                for move in self.getOpponentMoves(board):
                    newBoard = board.testMoveReturningBoard(-1 * self.player.value, (move[0], move[1]), (move[2], move[3]))
                    stack.append((newBoard, depth-1, self.player.value))
                    value = self.evaluate(newBoard)
                    if value < bestValue:
                        bestValue = value
                        bestMove = move
                if depth == 2:
                    return bestMove
                return bestValue

    def makeMove(self, board, move):
        return board.testMoveReturningBoard(self.player, (move[0], move[1]), (move[2], move[3]))

    def makeOpponentMove(self, board, move):
        return board.testMoveReturningBoard(-1 * self.player.value, (move[0], move[1]), (move[2], move[3]))

    def getBestMove(self, board, depth):
        bestValue = self.minimax(board, self.player, depth)
        bestMoves = []
        for move in self.getMoves(board):
            newBoard = self.makeMove(board, move)
            value = self.evaluate(newBoard)
            if value == bestValue:
                bestMoves.append(move)
       
        if not bestMoves:
            return random.choice(self.getMoves(board))

        bestMove = random.choice(bestMoves)
        return bestMove

    
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
        
        
        



