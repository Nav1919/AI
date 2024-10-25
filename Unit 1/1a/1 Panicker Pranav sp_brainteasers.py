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
    minMoves=dict()
    minMoves[graph]=0
    while fringe:
        v=fringe.popleft()
        moves=int(v[:v.find(" ")])
        board=v[v.find(" ")+1:]
        moves+=1
        for child in get_children(board, dim):
            if not (child in visited):
                visited.add(child)
                fringe.append(f"{moves} {child}")
                minMoves[child]=moves
    return minMoves

def BFS_FindFullLengthPath(goal_state, dim):
    fringe=deque()
    visited=set()
    start="12345678."
    fringe.append(start)
    visited.add(start)
    prevPair=dict()
    prevPair[start]="None"
    while fringe:
        board=fringe.popleft()        
        if(goal_state==board):
            break
        for child in get_children(board, dim):
            if not (child in visited):
                visited.add(child)
                fringe.append(child)
                prevPair[child]=board
    state=goal_state
    ret=[]
    while(state!="None"):
        ret.append(state)
        state=prevPair[state]
    return ret

def BFSrecurFindPath(graph, visited):
    if graph in visited:
        return False
    
    elif goal_test(graph):
        print(graph)
        return True
    else:
        visited.add(graph)
        children=get_children(graph, 3)
        return BFSrecurFindPath(children[0], visited) or BFSrecurFindPath(children[1], visited) or BFSrecurFindPath(children[2], visited) or BFSrecurFindPath(children[3], visited)

 
def main():
    boards2x2=BFS("123.",2)

    numMoves=BFS("12345678.",3)
    print(f"num of solvable 2x2 boards: {len(boards2x2)}")
    print(f"num of solvable 3x3 boards: {len(numMoves)}")
   # print("21345678." in boards3x3)
    #print(max([BFS(graph, 3) for graph in boards3x3]))
    filename="15_puzzles.txt"
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    linenum=0
    for line in line_list:
        dim=4
        graph=line
        start = perf_counter()
        print(f"Line {linenum}: {graph}, {BFS(graph, dim)} moves found in {perf_counter()-start} seconds")
        linenum+=1

    #line_list=[]
    #line_list.append("3 .25187643")
    '''moves1=BFS_FindFullLengthPath("8672543.1",3)
    moves2=BFS_FindFullLengthPath("64785.321",3)
    print(moves1)
    print(len(moves1)-1)
    print(moves2)
    print(len(moves2)-1)
    set10=set()
    setMax=set()
    maxVal=0
    for key in numMoves:
        if(maxVal<numMoves[key]):
            maxVal=numMoves[key]
            setMax={key}
        if(maxVal==numMoves[key]):
            setMax.add(key)
        if(numMoves[key]==10):
            set10.add(key)
    print(f"# of boards w min solve in 10 steps: {len(set10)}")
    print(setMax)
    print(maxVal)
'''
    #Code gets to line 21 before it bogs down (line 0 is first)'''



if __name__== "__main__":
    main()
