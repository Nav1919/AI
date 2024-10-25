import sys
def game_over(board: str):
    if(board.find('.')<0):
        return True
    elif abs(get_score(board))==1:
        return True
    else:
        return False
def get_score(board: str):
    for x in range(3):
        if(board[3*x:3*(x+1)]=='XXX' or board[x::3]=='XXX'):
            return 1
        elif(board[3*x:3*(x+1)]=='OOO' or board[x::3]=='OOO'):
            return -1
    if(board[0:9:4]=='XXX' or board[2:7:2]=='XXX'):
        return 1
    elif(board[0:9:4]=='OOO' or board[2:7:2]=='OOO'):
        return -1
    else:
        return 0

boardSet=set()
def find_boards(board, whosemove):
   # print(board)

    if(game_over(board)):
        boardSet.add(board)
        return 1
    totalGames=0
    tile=''
    if(whosemove>0):
        tile='X'
    else:
        tile='O'

    for i in range(9):
        if board[i]=='.':
            totalGames+=find_boards(board[:i]+tile+board[i+1:], -1*whosemove)
    return totalGames
def countMoves(board):
    moves=0
    for i in board:
        if i!='.':
            moves+=1
    return moves
def checkDraws(board):
    if get_score(board)==0:
        return True
    else:
        return False

def max_step(board):
    if game_over(board):
        return get_score(board)
    results=list()
    for i in range(9):
        if board[i]=='.':
            results.append(min_step(board[:i]+'X'+board[i+1:]))
    return max(results)
def min_step(board):
    if game_over(board):
        return get_score(board)
    results=list()
    for i in range(9):
        if board[i]=='.':
            results.append(max_step(board[:i]+'O'+board[i+1:]))
    return min(results)
def print_board(board: str):
    print("Current board:")
    print(board[:3]+"\t"+"012")
    print(board[3:6]+"\t"+"345")
    print(board[6:]+"\t"+"678")
    print()
def get_moves(board: str):
    pos_moves=list()
    for i in range(9):
        if board[i]=='.':
            pos_moves.append(i)
    return pos_moves
def tictactoe():    
    
    board=sys.argv[1]
    user=''
    computer=''
    if board=='.'*9:
        computer=input("Should I be X or O? ")
        user='XO'.replace(computer,'')
        print("")
    else:
        if(countMoves(board)%2==0):
            user='O'
            computer='X'
        else:
            user='X'
            computer='O'
        if(game_over(board)):
            print_board(board)
            score=get_score(board)
            if(score==0):
                print("We tied!")
            userWinVal=-1
            if(user=='X'):
                userWinVal=1
            if(score==userWinVal):
                print("You win!")
            else:
                print("I win!")
            return
    userMove=1
    userDesiredScore=-1
    if(user=='X'):
        userMove=0
        userDesiredScore=1
    while not game_over(board):
        print_board(board)
        list_moves=get_moves(board)
        movecount=9-len(list_moves)
        if(movecount%2==userMove):
            print(f"You can move to any of these spaces: {str(list_moves)[1:-1]}")
            choice=int(input("Your choice? "))
            print("")
            board=board[:choice]+user+board[choice+1:]
        else:
            bestPos=-1
            bestMove=-100
            if computer=='O':
                bestMove=100
            
            for move in list_moves:
                moveEffect=0
                if(computer=='X'):
                    moveEffect=min_step(board[:move]+'X'+board[move+1:])
                    
                else:
                    moveEffect=max_step(board[:move]+'O'+board[move+1:])
                    
                if abs(moveEffect+userDesiredScore)<abs(bestMove):
                    bestPos=move
                    bestMove=abs(moveEffect+userDesiredScore)
                moveWord='tie'
                if(moveEffect==userDesiredScore):
                    moveWord='loss'
                elif(moveEffect!=0):
                    moveWord='win'
                print(f"Moving at {move} results in a {moveWord}. ")
            print("")
            print(f"I choose space {bestPos}.")
            print("")
            board=board[:bestPos]+computer+board[bestPos+1:]


    print_board(board)
    userWinVal=-1
    if(user=='X'):
        userWinVal=1
    score=get_score(board)

    if(score==0):
        print("We tied!")
    elif(score==userWinVal):
        print("You win!")
    else:
        print("I win!")



    # print(find_boards(board,1))
    # print(len(boardSet))
    # winInN=[0]*5
    # drawCou(nt=0
    # for board in boardSet:
    #     if(checkDraws(board)):
    #         drawCount+=1
    #     else:
    #         moves=countMoves(board)
    #         winInN[moves-5]=winInN[moves-5]+1
    # print(drawCount)
    # print(winInN)
    # print(sum(winInN)+drawCount)

tictactoe()