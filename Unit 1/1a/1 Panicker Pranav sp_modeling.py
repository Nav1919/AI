import sys

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
    if curr>=dim:
        retList.append(graph[:curr-dim]+graph[curr]+graph[curr-dim+1:curr]+graph[curr-dim]+graph[curr+1:])
    return retList
 
def main():
    filename=sys.argv[1]
    #filename="slide_puzzle_tests.txt"
    with open(filename) as f:
        line_list = [line.strip() for line in f]

    lineNum=0
    for line in line_list:
        print(f"Line {lineNum} start state:")
        print_puzzle(line[2:],int(line[0]))
        print(f"Line {lineNum} goal state: {find_goal(line[2:])}")
        print(f"Line {lineNum} children: {get_children(line[2:],int(line[0]))}")
        print("")
        lineNum+=1

if __name__== "__main__":
    main()
