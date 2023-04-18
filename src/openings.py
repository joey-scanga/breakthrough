from gamemap import Player
    
middle = [[6, 1, 5, 2],[6, 6, 5, 5],[6, 0, 5, 1],[6, 7, 5, 6],[7, 0, 6, 1],[7, 7, 6, 6]]

pedestal = [[1, 4, 2, 4],[1, 5, 2, 5],[1, 1, 2, 2],[1, 6, 2, 5],[1, 0, 2, 1],[1, 7, 2, 6]]

openingsList = [ middle, 
            pedestal
        ]

def getMoveDirection(moves):
    if moves[0][0] < 4:
        return Player.A
    return Player.B

def reverseMove(moves):
    for move in moves:
        move[0] = 7 - move[0]
        move[2] = 7 - move[2]
    
            

    '''
    openings = {
            "middle": middle,
            "pedestal": pedestal
        }
    '''


