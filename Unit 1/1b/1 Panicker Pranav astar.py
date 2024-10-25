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
def taxicabDistance(puzzle, dim, goalState):
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

def get_children(graph, dim):
    curr=graph.index(".")
    retList=[]
    if (curr+1)%dim!=0:
        retList.append(graph[:curr]+graph[curr+1]+graph[curr]+graph[curr+2:])
    if curr%dim!=0:
        retList.append(graph[:curr-1]+graph[curr]+graph[curr-1]+graph[curr+1:])
    if curr+dim<len(graph):
        retList.append(graph[:curr]+graph[curr+dim]+graph[curr+1:curr+dim]+graph[curr]+graph[curr+dim+1:])
    if curr-dim>=0:
        retList.append(graph[:curr-dim]+graph[curr]+graph[curr-dim+1:curr]+graph[curr-dim]+graph[curr+1:])
    return retList

def a_star(start,dim):
    closed=set()
    goal=find_goal(start)
    startNode=(taxicabDistance(start,dim, goal),0,start)
    fringe=[]
    heappush(fringe, startNode)
    while fringe:
        (_, depth, state)=heappop(fringe)
        if state==goal:
            return depth
        if state not in closed:
            closed.add(state)
            for child in get_children(state,dim):
                if child not in closed:
                    temp=(taxicabDistance(child, dim, goal)+depth+1,depth+1,child)
                    heappush(fringe,temp)
    return None

def main():
    #filename=sys.argv[1]
    filename="Unit 1/1a/15_puzzles.txt"
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    linenum=0
    for line in line_list:
        # vals=line.split()
        # dim=int(vals[0])
        # graph=vals[1]
        dim=4
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