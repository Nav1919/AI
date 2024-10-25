import sys
from collections import deque
from time import perf_counter


def print_puzzle(graph, dim):   
    for i in range(dim):
        for j in range(dim):
            print(graph[dim*i+j], end=" ")
        print("")

def find_goal(graph):
    goal=''.join(sorted(graph))
    goal=goal[1:]+goal[0]
    return goal

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
    
def goal_test(graph):
    return graph==find_goal(graph)

def BFS(graph, dim):
    fringe=deque()
    visited=set()
    fringe.append("0 "+graph)
    visited.add(graph)
    while fringe:
        v=fringe.popleft()
        moves=int(v[:v.find(" ")])
        board=v[v.find(" ")+1:]
        if goal_test(board):
            return moves
        moves+=1
        for child in get_children(board, dim):
            if not (child in visited):
                visited.add(child)
                fringe.append(f"{moves} {child}")
    return -1 
def BiBFS(graph, dim):
    goal=find_goal(graph)
    sourceFringe=deque()
#    sourceVisited=set()
   # sourceFringe.append((graph,0))
    sourceFringe.append(graph)
    goalFringe=deque()
 #   goalVisited=set()
   # goalFringe.append((goal,0))
    goalFringe.append(goal)
    movesDictSource=dict()
    movesDictGoal=dict()
    movesDictSource[graph]=0
    movesDictGoal[goal]=0
    while sourceFringe and goalFringe:
        fromSource=sourceFringe.popleft()
        fromGoal=goalFringe.popleft()
        if fromSource in movesDictGoal:
            return movesDictSource[fromSource]+movesDictGoal[fromSource]
        if fromGoal in movesDictSource:
            return movesDictSource[fromGoal]+movesDictGoal[fromGoal]
        for sourceSideChild in get_children(fromSource,dim):
            if not (sourceSideChild in movesDictSource):
                movesDictSource[sourceSideChild]=movesDictSource[fromSource]+1
                sourceFringe.append(sourceSideChild)
        for goalSideChild in get_children(fromGoal,dim):
            if not (goalSideChild in movesDictGoal):
                movesDictGoal[goalSideChild]=movesDictGoal[fromGoal]+1
                goalFringe.append(goalSideChild)
    return -1


 
def main():
    filename=sys.argv[1]
    #filename="Unit 1/1a/slide_puzzle_tests.txt"
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    linenum=0
    for line in line_list:
        vals=line.split()
        dim=int(vals[0])
        graph=vals[1]
        start = perf_counter()
        print(f"Line {linenum}: {graph}, BFS - {BFS(graph, dim)} moves found in {perf_counter()-start} seconds")
        start=perf_counter()
        print(f"Line {linenum}: {graph}, Bi-BFS - {BiBFS(graph, dim)} moves found in {perf_counter()-start} seconds")
        print()

        linenum+=1

if __name__== "__main__":
    main()
 