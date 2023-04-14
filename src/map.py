import sys

class Player(Enum):
    HUMAN = 1
    AGENT = 2

'''
Returns a 2D array of characters with the initial board position. 
Blank squares are denoted with a '.', your pieces are denoted by 'O', 
and the AI's pieces are denoted by 'X'.
'''

def initializeBoard():
    return [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
            ]

'''
Checks if either side has won
'''
def checkWin(board):
    if board[0].contains('O'):
        return 0
    elif board[-1].contains('X'):
        return 1
    else: 
        return -1


def checkValidMove(board, player, fromSquare, toSquare):
    if player == Player.HUMAN:
        if board[fromSquare[0]][fromSquare[1]] != 'O':
            return False
        if board[toSquare[0]][toSquare[1]] != '.':
            return False
        if fromSquare[0] - toSquare[0] != 1:
            return False
        if abs(fromSquare[1] - toSquare[1]) > 1:
            return False
        return True
    elif player == Player.AGENT:
        if board[fromSquare[0]][fromSquare[1]] != 'X':
            return False
        if board[toSquare[0]][toSquare[1]] != '.':
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
def movePiece(board, player, fromSquare, toSquare):
    if checkValidMove(board, player, fromSquare, toSquare):
        board[fromSquare[0]][fromSquare[1]] = '.'
        if player == Player.HUMAN:
            board[toSquare[0]][toSquare[1]] = 'O'
        elif player == Player.AGENT:
            board[toSquare[0]][toSquare[1]] = 'X'
        if checkWin(board) == 0:
            print("Human won!")
            sys.exit(0)
        elif checkWin(board) == 1:
            print("Agent won!")
            sys.exit(0)

    else:
        return False


