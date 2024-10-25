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
    sourceFringe.append(graph)
    goalFringe=deque()
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
    #filename=sys.argv[1]
    filename="Unit 1/1a/15_puzzles.txt"
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    linenum=0
    for line in line_list:
        dim=4
        graph=line
        start = perf_counter()
        print(f"Line {linenum}: {graph}, BFS - {BFS(graph, dim)} moves found in {perf_counter()-start} seconds")
        print()
        if perf_counter()-start>60:
            break

        linenum+=1

if __name__== "__main__":
    main()

'''
1) Bi-BFS is consistently running in less than a 100th of the time it takes for BFS to run.
2) Code gets to line 41 before it bogs down using Bi-BFS, vs line 21 for BFS
3) Time gains were less apparent improving by a factor of 2/3 on average
4) A second dictionary was used to keep track of progress from the goalside and once an intersection was found you find the string of words that take you from start to the intersect in the first dict and the words that take you from intersect to goal in the second dict.
5) Bi-BFS is most useful in situations where there are consistently a lot of children generated or no decrease in the number of children as you increase depth in the search. This is because the consistent addition of children makes the number of boards checked become wider so going from both sides reduces the recursion depth from n to n/2 and for x children generated on average each phase it goes from x^n children generated to 2x^(n/2) which is more significant as depth n increases. 
'''
  