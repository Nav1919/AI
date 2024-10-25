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
    #print(graph)
    return graph==find_goal(graph)

def BFS(graph):
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
        for child in get_children(board, 4):
            if not (child in visited):
                visited.add(child)
                fringe.append(f"{moves} {child}")
    return -1 

def k_DFS(graph, k):
    fringe=deque()
    ancestor=set()
    ancestor.add(graph)
    fringe.append((graph,0,ancestor))
    while fringe:
        v=fringe.pop()
        if goal_test(v[0]):
            return v
        if(v[1]<k):
            for c in get_children(v[0],4):
                if c not in v[2]:
                    temp=v[2].copy()
                    temp.add(c)
                    fringe.append((c,v[1]+1,temp))
    return None
def ID_DFS(start):
    max_depth=0
    result=None
    while result is None:
        result=k_DFS(start,max_depth)
        max_depth+=1
    return result[1]

 
def main():
    #filename=sys.argv[1]
    filename="Unit 1/1a/15_puzzles.txt"
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    linenum=0
    for line in line_list:

        start = perf_counter()
        print(f"Line {linenum}: {line}, BFS - {BFS(line)} moves found in {perf_counter()-start} seconds")
        start2=perf_counter()
        print(f"Line {linenum}: {line}, ID-DFS - {ID_DFS(line)} moves found in {perf_counter()-start2} seconds")
        print()
        linenum+=1

if __name__== "__main__":
    main()
 