#Modelling Challenge I
#Pranav Panicker, Ryan Park

from heapq import heappop, heappush
from time import perf_counter
import sys


def find_goal():
    return (1,1,1,1,1,1)

def get_children(graph, dim, cubeindex, cubestate):
    retList=[]
    top,bottom,left,right,front,back=cubestate
    if (cubeindex+1)%dim!=0: #Right
        if(graph[cubeindex+1]=="." and right==1):
            newBottom=0
            newGraph=graph[:cubeindex+1]+"@"+graph[cubeindex+2:]
        elif(graph[cubeindex+1]=="@" and right==0):
            newBottom=1
            newGraph=graph[:cubeindex+1]+"."+graph[cubeindex+2:]
        else:
            newBottom=right
            newGraph=graph
        newState=(left, newBottom, bottom, top, front, back)
        index=cubeindex+1

        retList.append((newGraph, newState, index))
    if cubeindex%dim!=0:#Left
        if(graph[cubeindex-1]=="." and left==1):
            newBottom=0
            newGraph=graph[:cubeindex-1]+"@"+graph[cubeindex:]
        elif(graph[cubeindex-1]=="@" and left==0):
            newBottom=1
            newGraph=graph[:cubeindex-1]+"."+graph[cubeindex:]
        else:
            newBottom=left
            newGraph=graph
        newState=(right, newBottom, top, bottom, front, back)
        index=cubeindex-1
        retList.append((newGraph, newState, index))
    if cubeindex+dim<len(graph):#Down
        if(graph[cubeindex+dim]=="." and front==1):
            newBottom=0
            newGraph=graph[:cubeindex+dim]+"@"+graph[cubeindex+dim+1:]
        elif(graph[cubeindex+dim]=="@" and front==0):
            newBottom=1
            newGraph=graph[:cubeindex+dim]+"."+graph[cubeindex+dim+1:]
        else:
            newBottom=front
            newGraph=graph
        newState=(back,newBottom,left, right, top,bottom)
        index=cubeindex+dim
        retList.append((newGraph, newState, index))
    if cubeindex-dim>=0:#Up
        if(graph[cubeindex-dim]=="." and back==1):
            newBottom=0
            newGraph=graph[:cubeindex-dim]+"@"+graph[cubeindex-dim+1:]
        elif(graph[cubeindex-dim]=="@" and back==0):
            newBottom=1
            newGraph=graph[:cubeindex-dim]+"."+graph[cubeindex-dim+1:]
        else:
            newBottom=back
            newGraph=graph
        newState=(front,newBottom,left, right, bottom,top)
        index=cubeindex-dim
        retList.append((newGraph, newState, index))
    return retList

def heuristic(cubestate):
    return 6 - sum(cubestate)

def a_star(size, board, cubePos, cubeState):
    closed=set()
    goal=find_goal()
    startNode=(heuristic(cubeState),0,board,cubePos, cubeState, [])
    fringe=[]
    heappush(fringe, startNode)
    while fringe:
        _, depth, boardState, cubeIndex, state, path= heappop(fringe)
        if(state==goal):
            path.append(cubeIndex)
            return path
        if (boardState, state, cubeIndex) not in closed:
            closed.add((boardState, state, cubeIndex))
            for child in get_children(boardState, size, cubeIndex, state):
                if child not in closed:
                    newBoard, new_state, new_index = child
                    copyPath = path.copy()
                    copyPath.append(cubeIndex)
                    heappush(fringe,(heuristic(new_state)+depth+1, depth+1, newBoard, new_index, new_state, copyPath))
    return []

#filename = 'cube_puzzles.txt'
filename=sys.argv[1]
with open(filename) as f:
    line_list = [(line.strip()).split(' ') for line in f]     

for i in range(len(line_list)):
    start = perf_counter()
    cubeState = (0,0,0,0,0,0)
    num_moves = a_star(int(line_list[i][0]), line_list[i][1], int(line_list[i][2]), cubeState)
    end = perf_counter()
    print('Line ' + str(i) + ": " + line_list[i][1] + ', A* - ' + str(len(num_moves) -1) + ' moves found in ' + str(end - start) + ' seconds')
    dir_moves=list()
    for i in range(len(num_moves)-1):
        dpos=num_moves[i+1]-num_moves[i]
        if(dpos==1):
            dir_moves.append("Right")
        elif(dpos==-1):
            dir_moves.append("Left")
        elif(dpos<0):
            dir_moves.append("Up")
        else:
            dir_moves.append("Down")
    print(f"Starting from position {num_moves[0]}")
    print(dir_moves)
    print()
 
