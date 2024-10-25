import sys
from collections import deque
from time import perf_counter

def find_children(word_set):
    children=dict()
    for word in word_set:
        if word not in children:
            children[word]=set()
        for i in range(6):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if letter!=word[i] and (test:=(word[:i]+letter+word[i+1:])) in word_set:
                    if test not in children:
                        children[test]=set()
                    children[word].add(test)
                    children[test].add(word)
    return children

def get_children(childrenDict, parent):
    return childrenDict[parent]

def BFS(start, end, childrenDict):
    fringe=deque()
    visited=set()
    fringe.append(start)
    visited.add(start)
    prevPair=dict()
    prevPair[start]="None"
    pathFound=False
    while fringe:
        word=fringe.popleft()
        if word==end:
            pathFound=True
            break
        for child in get_children(childrenDict, word):
            if not (child in visited):
                visited.add(child)
                fringe.append(child)
                prevPair[child]=word
    if pathFound:
        state=end
        ret=[]
        while(state!="None"):
            ret.append(state)
            state=prevPair[state]
        return ret[::-1]
    return "No solution"

def BFS_findallconnected(start, childrenDict):
    fringe=deque()
    visited=set()
    fringe.append(start)
    visited.add(start)
    while fringe:
        word=fringe.popleft()
        for child in get_children(childrenDict, word):
            if not (child in visited):
                visited.add(child)
                fringe.append(child)
    return visited  

def BFS_findmaxpath(start, childrenDict):
    fringe=deque()
    visited=set()
    fringe.append(start)
    visited.add(start)
    prevPair=dict()
    prevPair[start]="None"
    while fringe:
        word=fringe.popleft()
        for child in get_children(childrenDict, word):
            if not (child in visited):
                visited.add(child)
                fringe.append(child)
                prevPair[child]=word
    state=word
    ret=[]
    while(state!="None"):
        ret.append(state)
        state=prevPair[state]
    return ret[::-1]
def main():
    #filename=sys.argv[1]
    filename="words_06_letters.txt"
    with open(filename) as f:
        line_set = {line.strip() for line in f}
    children=find_children(line_set)
    with open("puzzles_normal.txt") as f:
        testVals=[tuple(line.strip().split()) for line in f]
    for start, end in testVals:
        print(BFS(start, end, children)) 
    singletonCount=0
    for val in children:
        if(len(children[val])==0):
            singletonCount+=1
    print(f"#OfSingletons: {singletonCount}")
    #1568 singletons
    clumps=list()
    clumpLengths=list()
    visited=set()
    largestConLength=0
    for startPos in children:
        if len(children[startPos])!=0 and startPos not in visited:
            findClump=BFS_findallconnected(startPos,children)
            clumps.append(findClump)
            clumpLengths.append(len(findClump))
            if(len(findClump)>largestConLength):
                largestConLength=len(findClump)
                largestConClump=findClump
            visited.update(findClump)

    print(f"Largest connected subcomponent: {largestConLength}")
    #1625 words in largest connected subcomponent
    print(f"#Clumps: {len(clumps)}")
    #450 clumps
    print(len(line_set))
    #for clump in clumps:
    maxPathLength=0
    for val in largestConClump:
        path=BFS_findmaxpath(val,children)
        if(len(path)>maxPathLength):
            maxPathLength=len(path)
            maxPath=path
    print(maxPath)
    print(len(maxPath))



if __name__=="__main__":
    main()