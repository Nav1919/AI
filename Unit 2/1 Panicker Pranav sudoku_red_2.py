import sys
from time import perf_counter

def initializeGlobals(board):
    global length, subblockheight, possible_answers, subblockwidth, symbolset, neighbors, subblockneighbors, verticalneighbors, horizontalneighbors, constraint_dictionary
    verticalneighbors, horizontalneighbors, subblockneighbors = [], [], []
    constraint_dictionary = {}
    possible_answers = {}
    constraints = []
    neighbors = []
    length = int(len(board)**0.5)
    chars = "123456789ABCDEFGHIJKLMNOPQRSTUVVWXYZ" 
    symbolset = chars[0:int(length)] 
    n, d = (len(board)**0.5), ((len(board)**0.5)**0.5)
    if(n%d == 0):
        subblockwidth, subblockheight = d, d
    else:
        c= int(n**0.5) + 1
        while(n%c != 0):
            c += 1
        d = int(n/c)
        subblockwidth = c
        subblockheight = d 
    n = int(n)
    d = int(d)
    for x in range(0, len(board), length):
        horizontalneighbors.append([y for y in range(x, x + length)])
    for x in range(length):
        temp = []
        verticalneighbors.append([y for y in range(x, len(board), length)])
    subblockwidth = int(subblockwidth)
    subblockheight = int(subblockheight)
    dx = int(length//subblockwidth)
    dy = int(length//subblockheight)
    for v in range(dy):
        initialval = v*length*subblockheight
        for w in range(dx):
            next = initialval + w*subblockwidth
            temp = []
            for x in range((subblockwidth)):
                after = next + x
                for y in range((subblockheight)):
                    then = after + length*y
                    temp.append((then))
            subblockneighbors.append((temp))
    for l in range(len(board)):
        constraints = set()
        for x in verticalneighbors[l%length]:
            constraints.add(x)
        for x in horizontalneighbors[int(l/length)]:
            constraints.add(x)
        for x in subblockneighbors:
            if l in x:
                for a in x:
                    constraints.add(a)
                break
        constraints.remove(l)
        constraint_dictionary[l] = constraints
    for x in range(len(board)):
        poss = list(symbolset)
        for y in constraint_dictionary[x]:
            if(board[y] in poss):
                poss.remove(board[y])
        possible_answers[x] = list(poss)

def goalTest(dictionary):
    for key in dictionary:
        if(len(dictionary[key]) != 1):
            return False
    return True

def getMostConstrainedVar(dictionary):
    min = len(dictionary)
    minindex = -1
    for key in dictionary:
        if(len(dictionary[key]) < min and len(dictionary[key]) > 1):
            min = len(dictionary[key])
            minindex = key
    return (minindex)

def forwardLooking(dictionary, solved):
    new_dict = dictionary
    listofsolvedvalues = set()
    for key in new_dict:
        if(len(new_dict[key]) == 1 and key not in solved):
            listofsolvedvalues.add(key)
            solved.append(key)
    if(len(listofsolvedvalues) == 0):
        return new_dict
    for y in listofsolvedvalues:
        neighbors = set(constraint_dictionary[y])
        for a in neighbors:
            if((new_dict[y][0]) in new_dict[(a)]):
                new_dict[(a)].remove((new_dict[y][0]))
            if(len(new_dict[a]) == 0):
                return None
        solved.append(y)
    for key in dictionary:
        if(len(new_dict[key]) == 1 and key not in solved):
            return forwardLooking(new_dict, solved)
    return new_dict

def sudokuBacktracking(dictionary):
    if(goalTest(dictionary) == True): return dictionary
    var = getMostConstrainedVar(dictionary)
    x = set(dictionary[var])
    if(len(x) == 2 or len(x) == 3 or len(x) == 4):
        for val in x:
            new_dict = {x: dictionary[x].copy() for x in dictionary}
            new_dict[var] = [val]
            h = forwardLooking(new_dict, [])
            if(h is not None):
               boarder, solved = constraintProp(h)
               while (h != boarder):
                   h = forwardLooking(boarder, solved)
                   if(h is not None):
                        boarder, solved = constraintProp(h)
            if(h is not None):
                returned_board = sudokuBacktracking(h)
                if returned_board is not None:
                    return returned_board
    return None

def checkRow(board):
    solved = []
    ans = symbolset
    for x in horizontalneighbors:
        diction = {}
        for xo in list(ans):
            diction[xo] = 0
        for l in x:
            for y in board[l]:
                if(y in diction):
                    diction[y] += 1
        for z in x:
            for d in board[z]:
                if(diction[d] == 1):
                    board[z] = [d]
                    solved.append(z)
    return board, solved

def checkCol(board):
    solved = []
    ans = symbolset     
    for x in verticalneighbors:
        diction = {}
        for xo in list(ans):
            diction[xo] = 0
        for l in x:
            for y in board[l]:
                if(y in diction):
                    diction[y] += 1
        for z in x:
            for d in board[z]:
                if(diction[d] == 1):
                    board[z] = [d]
                    solved.append(z)
    return board, solved

def checkBlock(board):
    solved = []
    ans = symbolset
    for x in subblockneighbors:
        diction = {}
        for xo in list(ans):
            diction[xo] = 0
        for l in x:
            for y in board[l]:
                if(y in diction):
                    diction[y] += 1
        for z in x:
            for d in board[z]:
                if(diction[d] == 1):
                    board[z] = [d]
                    solved.append(z)
    return board, solved

def constraintProp(board):
    board, solveda = checkRow(board)
    board, solvedb = checkCol(board)
    board, solvedc = checkBlock(board)
    solved = list(set(solveda + solvedb + solvedc))
    return board, solved

def printBoard(board):
    length = int(len(board)**0.5)
    for x in range(length):
        print(''.join(board[0 + x*length: x*length + length]))
    print()
    print()

def main():
    # filename = sys.argv[1]
    filename="Unit 2/puzzles_6_variety_hard.txt"
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    start = perf_counter()
    linenum=0
    for x in line_list:
        initializeGlobals(list(x))
        a = sudokuBacktracking(possible_answers)
        temp = []
        for key in a:
            temp.append(a[key][0])
        print(f"Line {linenum}: {''.join(temp)}")
        linenum+=1
    end = perf_counter()
    print(end - start)

if __name__=="__main__":
    main()