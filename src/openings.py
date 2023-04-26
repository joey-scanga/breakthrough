from gamemap import Player
import copy

#List of Breakthrough openings to be used by agents
middle = [[6, 1, 5, 2],[6, 6, 5, 5],[6, 0, 5, 1],[6, 7, 5, 6],[7, 0, 6, 1],[7, 7, 6, 6]]

pedestal = [[1, 4, 2, 4],[1, 5, 2, 5],[1, 1, 2, 2],[1, 6, 2, 5],[1, 0, 2, 1],[1, 7, 2, 6]]

openingsList = [ middle, 
            pedestal
       ]

#Will reverse the direction of opening if necessary
def setMoveDirection(player, moves):
    if player == Player.A and getMoveDirection(moves) == Player.B:
        return reverseMoves(moves)
    elif player == Player.B and getMoveDirection(moves) == Player.A:
        return reverseMoves(moves)
    return moves

#Gets default direction of opening
def getMoveDirection(moves):
    if moves[0][0] == 0 or moves[0][0] == 1:
        return Player.B
    return Player.A

#Reverses opening to be used by opponent
def reverseMoves(moves):
    newmoves = copy.deepcopy(moves)
    for move in newmoves:
        move[0] = 7 - move[0]
        move[2] = 7 - move[2]
    return newmoves
    
            

    '''
    openings = {
            "middle": middle,
            "pedestal": pedestal
        }
    '''


