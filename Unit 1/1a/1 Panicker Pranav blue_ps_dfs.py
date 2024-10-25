from collections import deque
from time import perf_counter
def get_children(board,moves):
    total=14-moves
    count=0
    children=set()
    for i in range(len(board)):
        if(count==total):
            break
        if(board[i]=="0"):
            count+=1
            if(i+10<len(board) and board[i+5]=='1' and board[i+10]=='1'):
                children.add(board[:i]+"1"+board[i+1:i+5]+"0"+board[i+6:i+10]+"0"+board[i+11:])
            if(i+12<len(board) and board[i+6]=='1' and board[i+12]=='1'):
                children.add(board[:i]+"1"+board[i+1:i+6]+"0"+board[i+7:i+12]+"0"+board[i+13:])
            if(i+2<len(board) and board[i+1]=="1" and board[i+2]=="1"):
                children.add(board[:i]+"100"+board[i+3:])
            if(i-2>=0 and board[i-1]=="1" and board[i-2]=="1"):
                children.add(board[:i-2]+"001"+board[i+1:])
            if(i-12>=0 and board[i-6]=='1' and board[i-12]=='1'):
                children.add(board[:i-12]+'0'+board[i-11:i-6]+'0'+board[i-5:i]+'1'+board[i+1:])
            if(i-10>=0 and board[i-5]=='1' and board[i-10]=='1'):
                children.add(board[:i-10]+'0'+board[i-9:i-5]+'0'+board[i-4:i]+'1'+board[i+1:])

    return children

def print_puzzle(board: str):
    for i in range(0,len(board),5):
        curr=' '.join(board[i:i+5].replace('.',''))
        while(len(curr)<9):
            curr=" "+curr+" "
        print(curr)

def check_goal(board):
    count1=0
    for i in board:
        if i=="1":
            count1+=1
        if(count1>1):
            return False
    return True

def DFS(graph, goal_state):
    fringe=deque()
    visited=set()
    fringe.append((graph,0))
    visited.add(graph)
    prevPair=dict()
    prevPair[graph]="None"
    while fringe:
        board=fringe.pop()
        visited.add(board[0])
        if(goal_state==board[0]):
            break
        for child in get_children(board[0],board[1]):
            if not (child in visited):
                fringe.append((child,board[1]+1))
                prevPair[child]=board[0]
    state=goal_state
    ret=[]
    while(state!="None"):
        ret.append(state)
        state=prevPair[state]
    return ret[::-1]

def BFS(graph, goal_state):
    fringe=deque()
    visited=set()
    fringe.append((graph,0))
    visited.add(graph)
    prevPair=dict()
    prevPair[graph]="None"
    while fringe:
        board=fringe.popleft()
        visited.add(board[0])
        if(goal_state==board[0]):
            break
        for child in get_children(board[0],board[1]):
            if not (child in visited):
                fringe.append((child,board[1]+1))
                prevPair[child]=board[0]
    state=goal_state
    ret=[]
    while(state!="None"):
        ret.append(state)
        state=prevPair[state]
    return ret[::-1]

def main():
    board="0....11...111..1111.11111"
    goal="1....00...000..0000.00000"
    #'.' is unused position, '1' is filled tile, '0' is unfilled tile

    print("DFS:")
    for path in DFS(board, goal):
        print_puzzle(path)
        print()
    print("BFS:")
    for path in BFS(board,goal):
        print_puzzle(path)
        print()

    
if __name__=="__main__":
    main()