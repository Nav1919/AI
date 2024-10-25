import sys
from collections import deque
from time import perf_counter

def find_children(word_set):
    children=dict()
    for word in word_set:
        for i in range(6):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if letter!=word[i] and (test:=(word[:i]+letter+word[i+1:])) in word_set:
                    if word not in children:
                        children[word]=set()
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
        

def main():
    #dictFile="words_06_letters.txt"
    #btestFile="puzzles_normal.txt"
    dictFile="Unit 1/1a/words_06_letters.txt"
    testFile="Unit 1/1a/puzzles_normal.txt"
    startMakeDict=perf_counter()
    with open(dictFile) as f:
        line_set = {line.strip() for line in f}
    children=find_children(line_set)
    endMakeDict=perf_counter()
    print(f"Time to create the data structure was: {endMakeDict-startMakeDict} seconds")
    print(f"There are {len(children)} words in this dict.")
    print("")
    startSolve=perf_counter()
    with open(testFile) as f:
        testVals=[tuple(line.strip().split()) for line in f]
    linenum=0
    for start, end in testVals:
        print(f"Line: {linenum}")
        linenum+=1
        ladder=BFS(start, end, children)
        if(ladder=="No solution"):
            print("No solution")
        else:
            for val in ladder:
                print(val)
        print("")
    endSolve=perf_counter()
    print(f"Time to solve all of these puzzles was: {endSolve-startSolve} seconds")


if __name__=="__main__":
    main()