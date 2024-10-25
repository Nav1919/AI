import sys
import time
import math

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
def game_over(board):
   return '.' not in board
def get_multiplier(token):
   if token=='x':
      return 1
   elif token=='o':
      return -1
   else:
      return 0
corners={0,7,56,63}
adjacents={1:0,6:7,8:0, 9:0, 14:7, 15:7,48:56, 49:56, 54: 63, 55:63,57:56,62:63}
def board_score(board: str):
    scores = 0  
    d = {6: 7, 14: 7, 1: 0, 9: 0, 15: 7, 62: 63, 49: 56, 48: 56, 54: 63, 8: 0, 55: 63, 57: 56}
    for k in d.keys(): #corner adjacents
        if board[k] == "o":
            if "o" != board[d[k]]:
                scores += 5000
        elif board[k] == "x":
            if board[d[k]]!="x":
                scores -= 5000
            else:
                scores+=-1*0

    x = possible_moves(board,"x")
    o = possible_moves(board,"o")

    for c in [0,7,56,63]:
        if board[c] == "o":
            scores -= 50000
        elif board[c] == "x":
            scores += 50000

    for e in [16,24,32,40,58,59,60,61,2,3,4,5,23,31,39,47]:
        if board[e] == "o":
            scores -= 50
        elif board[e] == "x":
            scores += 50         
    co = board.count("o")
    cx = board.count("x")
    scores += 5*(len(x) - len(o))
    return (cx - co) * (10000000) if game_over(board) == True else scores

def step(board: str, player: str, opponent: str, depth: int, alpha: int, beta: int):
   if depth==0:
      return board_score(board)
   if game_over(board):
      xtiles=board.count('x') 
      otiles=board.count('o')
      return (xtiles-otiles)*1000000
   if player=='x':
      max=-math.inf
      for move in possible_moves(board, player):
         curr=step(make_move(board, player, move), opponent, player, depth-1, alpha, beta)
         if curr is None:
            continue
         if curr>max:
            max=curr
         if max>alpha: #"ALPHA/BETA PRUNING HERE"
            alpha=max
         if alpha>beta:
            return max
      return max
   if player=='o':
      min=math.inf
      for move in possible_moves(board, player):
         curr=step(make_move(board, player, move), opponent, player, depth-1, alpha, beta)
         if curr is None:
            continue
         if curr<min:
            min=curr
         if min<beta: #"ALPHA/BETA PRUNING HERE"
            beta=min
         if alpha>beta:
            return min
      return min
   return None       

def find_next_move(board, player, depth):
   bestmove=-1
   bestresult=-math.inf
   for move in possible_moves(board, player):
      opponent='xo'.replace(player,"")
      curr=step(make_move(board, player, move), opponent, player, depth-1, -math.inf, math.inf)
      if curr==None or abs(curr)==math.inf: continue
      if curr*get_multiplier(player)>bestresult:
         bestresult=curr*get_multiplier(player)
         bestmove=move
   if bestmove<0:
      return find_next_move(board, player, depth-1)
   else:
      return bestmove

board=sys.argv[1]
player=sys.argv[2]


depth = 1

for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   move=find_next_move(board, player, depth)
   if move>=0:
      print(move)
      print()
      depth += 1
