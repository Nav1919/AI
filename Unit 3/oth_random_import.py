from random import choice
import sys
directions = [-9, -8, -7, -1, 1, 7, 8, 9]

def on_board(checkpos, dir):
    if 0<=checkpos<64:
        horizontalopos=(checkpos-dir)%8
        horizontalnpos=checkpos%8
        return abs(horizontalnpos-horizontalopos)<=1
    return False
def possible_moves(board,token):
    possible_moves=list()
    for pos in range(len(board)):

        if board[pos]!='.':
            continue
        validpos=False
        for dir in directions:
            checkpos=pos+dir
            if not on_board(checkpos, dir):
                continue
            if board[checkpos]==token or board[checkpos]=='.':
                continue 
            checkpos+=dir
            while(on_board(checkpos, dir)):
                if(board[checkpos]==token):
                    validpos=True
                    break
                if(board[checkpos]=='.'):
                    break
                checkpos+=dir
            if(validpos):
                possible_moves.append(pos)
                break
    return possible_moves
board = sys.argv[1]
player = sys.argv[2]
# board = 'xxoxxxxxxxooxxxxxxooooxxxxxooooxxxoxxoxxxoxxxxxxo.ooo..o.ooo....'
# player = 'o'
print(choice(possible_moves(board, player)))