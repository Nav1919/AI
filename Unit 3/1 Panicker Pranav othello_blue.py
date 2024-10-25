#from othello_imports import make_move, possible_moves
import sys
import time

directions = [-9, -8, -7, -1, 1, 7, 8, 9]

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

def find_next_move(board, player, depth):
   bestmove=0
   bestresult=-10000000000000
   for move in possible_moves(board, player):
      opponent='xo'.replace(player,"")
      curr=step(make_move(board, player, move), opponent, player, depth-1)
      if curr==None: continue
      if curr*get_multiplier(player)>bestresult:
         bestresult=curr*get_multiplier(player)
         bestmove=move
   return bestmove

  
def step(board: str, player: str, opponent: str, depth: int):
   if depth==0:
      return board_score(board)
   if game_over(board):
      xtiles=board.count('x') 
      otiles=board.count('o')
      return (xtiles-otiles)*100000
   results=list()
   for move in possible_moves(board, player):
      curr=step(make_move(board, player, move), opponent, player, depth-1)
      if curr!=None:
         results.append(curr)
         
   if len(results)==0 or results==None:
      return None
   elif player=='o':
      return min(results)
   else:
      return max(results)
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
   score=0
   score=len(possible_moves(board, 'x'))-len(possible_moves(board,'o'))
   for i in range(len(board)):
      mult=get_multiplier(board[i])
      if(mult==0):
         continue
      if i in corners:
         score+=1000*mult
      elif i in adjacents:
         if(get_multiplier(board[adjacents[i]])==mult):
            score+=100*mult
         else:
            score-=100*mult
      elif 0<i<7 or 56<i<63 or i%8==0 or i%8==7:            
         score+=10*mult
   return score
   # score=0
   # for i in range(len(board)):
   #    mult=get_multiplier(board[i])
   #    if(mult==0):
   #       continue
   #    if i in corners:
   #       score+=1000000*mult
   #    elif i in adjacents:
   #       if get_multiplier(board[adjacents[i]])==0:
   #             score-=100000*mult
   #       else:
   #          score+=2*mult
   #    elif 0<i<7 or 56<i<63 or i%8==0 or i%8==7:            
   #       score+=100*mult
         
   #    else:
   #       score+=mult
   # score += 10000*(len(possible_moves(board,'x'))-len(possible_moves(board,'o')))
   # return score


# All your other functions
def on_board(checkpos, dir):
    if 0<=checkpos<64:
        horizontalopos=(checkpos-dir)%8
        horizontalnpos=checkpos%8
        return abs(horizontalnpos-horizontalopos)<=1
    return False

board=sys.argv[1]
player=sys.argv[2]
# board = '...........................ox......xx.......x...................'
# player = 'o'

depth = 1

for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   # print(board_score(make_move(board,'x',9)))
   # print(possible_moves(board, player))
   print(find_next_move(board, player, depth))

   print()
   depth += 1
# results = []
# with open("Unit 3\\boards_timing.txt") as f:
#    for line in f:
#       board, token = line.strip().split()
#       temp_list = [board, token]
#       print(temp_list)
#       for count in range(1, 7):
#          print("depth", count)
#          start = time.perf_counter()
#          find_next_move(board, token, count)
#          end = time.perf_counter()
#          temp_list.append(str(end - start))
#       print(temp_list)
#       print()
#       results.append(temp_list)
# with open("boards_timing_my_results.csv", "w") as g:
#    for l in results:
#       g.write(", ".join(l) + "\n")