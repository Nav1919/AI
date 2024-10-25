import sys
from time import perf_counter
from heapq import heappush, heappop, heapify

def getInvCount(puzzle):
    inv_count = 0
    empty_value = "."
    for i in range(0, len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[j] != empty_value and puzzle[i] != empty_value and puzzle[i] > puzzle[j]:
                inv_count += 1
    return inv_count

#returns True if puzzle is solvable
def checkParity(puzzle, dim):
    invCount=getInvCount(puzzle)
    if(dim%2==1):
        if(invCount%2==0):
            return True
    elif(invCount%2==0):
        if (puzzle.find(".")//dim)%2==1:
            return True
    elif (puzzle.find(".")//dim)%2==0:
        return True
    return False
def find_goal(graph):
    goal=''.join(sorted(graph))
    goal=goal[1:]+goal[0]
    return goal
def taxicabDistance(puzzle, dim, goalState, goalPos):
    dist=0
    goal=goalState
    for i in goal:
        if(i=="."):
            continue
        pos=puzzle.find(i)
        goalpos=goal.find(i)
        currRow=pos//dim
        currCol=pos%dim
        goalRow=goalpos//dim
        goalCol=goalpos%dim
        dist+=abs(currRow-goalRow)
        dist+=abs(currCol-goalCol)
    


    return dist
def countRowColConflicts(puzzle,dim,goalState,goalPos):
    for row in range(dim):
        incorrrow=""
        for col in range(4):
            

def get_children(graph: str, dim: int, goalPos: dict):
    curr=graph.index(".")
    retList=[]
    if (curr+1)%dim!=0:
        heuristicInc=abs(goalPos[graph[curr+1]][0]-curr%dim)-abs(goalPos[graph[curr+1]][0]-(curr+1)%dim)
        retList.append((graph[:curr]+graph[curr+1]+graph[curr]+graph[curr+2:],heuristicInc))
    if curr%dim!=0:
        heuristicInc=abs(goalPos[graph[curr-1]][0]-curr%dim)-abs(goalPos[graph[curr-1]][0]-(curr-1)%dim)
        retList.append((graph[:curr-1]+graph[curr]+graph[curr-1]+graph[curr+1:],heuristicInc))
    if curr+dim<len(graph):
        heuristicInc=abs(goalPos[graph[curr+dim]][1]-curr//dim)-abs(goalPos[graph[curr+dim]][1]-(curr+dim)//dim)
        retList.append((graph[:curr]+graph[curr+dim]+graph[curr+1:curr+dim]+graph[curr]+graph[curr+dim+1:],heuristicInc))
    if curr-dim>=0:
        heuristicInc=abs(goalPos[graph[curr-dim]][1]-curr//dim)-abs(goalPos[graph[curr-dim]][1]-(curr-dim)//dim)
        retList.append((graph[:curr-dim]+graph[curr]+graph[curr-dim+1:curr]+graph[curr-dim]+graph[curr+1:],heuristicInc))
    return retList

def a_star(start: str,dim: int):
    closed=set()
    goalPos=dict()
    
    goal=find_goal(start)
    for row in range(dim):
        for col in range(dim):
            goalPos[goal[dim*row+col]]=(col,row)
    startNode=(taxicabDistance(start,dim, goal, goalPos),0,start)
    fringe=[]
    heappush(fringe, startNode)
    while fringe:
        (heuristic, depth, state)=heappop(fringe)
        if state==goal:
            return depth
        if state not in closed:
            closed.add(state)
            for child,heuristic_inc in get_children(state,dim,goalPos):
                if child not in closed:
                    temp=(heuristic+heuristic_inc+1,depth+1,child)
                    heappush(fringe,temp)
    return None

def main():
    #filename=sys.argv[1]
    filename="Unit 1/1a/15_puzzles.txt"
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    linenum=0
    for line in line_list:
#        vals=line.split()
        #dim=int(vals[0])
        dim=4
 #       graph=vals[1]
        graph=line
        
        

        #Front, Back, Left, Right, Top Bottom
        start = perf_counter()
        print(f"Line {linenum}: {graph}", end=", ")
        if(checkParity(graph,dim)):
            print(f"A* - {a_star(graph,dim)} moves in {perf_counter()-start} seconds",end="\n\n")
        else:
            print(f"no solution determined in {perf_counter()-start} seconds",end="\n\n")
        linenum+=1
        
if __name__=="__main__":
    main()