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
        val=board[pos]
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

def make_move(board,token,index):
    ret_board=board[:index]+token+board[index+1:]
    opposite='xo'.replace(token,"")
    for dir in directions:
        checkpos=index+dir
        if not on_board(checkpos, dir):
            continue
        if(ret_board[checkpos]!=opposite):
            continue
        flipTokens=False
        while(on_board(checkpos,dir)):
            if(ret_board[checkpos]=='.'):
                break
            if(ret_board[checkpos]==token):
                flipTokens=True
                break
            checkpos+=dir
        if(flipTokens):
            checkpos=index+dir
            while(ret_board[checkpos]!=token):
                ret_board=ret_board[:checkpos]+token+ret_board[checkpos+1:]
                checkpos+=dir
    return ret_board
