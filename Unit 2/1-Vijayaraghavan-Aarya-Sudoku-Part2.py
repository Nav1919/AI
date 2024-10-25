import sys
import math
import random

N, blockheight, blockwidth = 0, 0, 0
fullsymbolist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B",
                 "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
symbollist = []
colsetlist = []  # so it's a list of columns.. columns are sets of points
rowsetlist = []
blocksetlist = []
constraints = dict()


def displayBoard(puzzle, N):
    a = 0
    for i in range(N):
        line = ""
        for j in range(N):
            space = N+1-len(puzzle[a])

            line += (puzzle[a] + (" "*space))
            a += 1
        print(line)


def copy(puzzle):  # copies dictionary
    newpuzz = dict()
    for key in puzzle:
        newpuzz[key] = puzzle[key]

    return newpuzz


def makeConstraints(N, blockheight, blockwidth):  # CHANGE THESE TO LIST
    for i in range(N):
        rowsetlist.append([])
        colsetlist.append([])

    for row in range(N // blockheight):
        blocksetlist.append([])
        for col in range(N // blockwidth):
            blocksetlist[row].append([])

    for row in range(N):
        for col in range(N):
            rowsetlist[row].append(row * N + col)
            colsetlist[col].append(row * N + col)
            blocksetlist[row // blockheight][col // blockwidth].append(row * N + col)

    for row in range(N):
        for col in range(N):
            #constraints[row * N + col] = rowsetlist[row].union(colsetlist[col], blocksetlist[row // blockheight][col // blockwidth])
            nums = rowsetlist[row][:]
            for idx in colsetlist[col]:
                if idx not in nums: nums.append(idx)
            for idx in blocksetlist[row // blockheight][col // blockwidth]:
                if idx not in nums: nums.append(idx)
            constraints[row * N + col] = nums[:]
            constraints[row * N + col].remove(row * N + col)


def get_most_constrainedvar(puzzle):
    mindexes = [0]
    minlen = math.inf
    for ind in range(1, len(puzzle)):
        if (lenposs := len(puzzle[ind])) > 1:  # if it is not solved
            if lenposs == minlen: mindexes.append(ind)
            elif lenposs < minlen: 
                mindexes = [ind]
                minlen = lenposs

    if len(mindexes) == 1: return mindexes[0]
    else: return random.choice(mindexes)


def get_sortedvals(puzzle, pos):  # pos is the int position of the coordinate
    constraintset = constraints[pos]
    # shallow copy.. not deepcopy.. it's a diff set so it doesn't affect the original symbollist
    possiblevals = symbollist.copy()
    for constraintpos in constraintset:   # for every position that constraints this square
        # if that position has some value, this square cannot have it
        if (len(tmp := puzzle[constraintpos]) == 1) and tmp in possiblevals:
            possiblevals.remove(tmp)

    return possiblevals


def checkGoal(puzzle, N, blockheight, blockwidth):  # So to fix it, I need to loop through each constraint set and make sure that it works
    for key in puzzle:
        if len(puzzle[key]) != 1:
            return False

    for i in range(N):
        rowset = set()
        for j in range(N):
            if puzzle[i * N + j] in rowset: 
                # print("here in rows", puzzle[i * N + j], "Coordinates are", i, j)
                # sys.exit(0)
                return False
            rowset.add(puzzle[i * N + j])
    for j in range(N):
        colset = set()
        for i in range(N):
            if puzzle[i * N + j] in colset: 
                # print("here in cols", puzzle[i * N + j], "Coordinates are", i, j)
                # sys.exit(0)
                return False
            colset.add(puzzle[i * N + j]) 
    for bigi in range(0, N, blockheight):
        for bigj in range(0, N, blockwidth):
            blckset = set()
            for i in range(0, blockheight):
                for j in range(0, blockwidth):
                    if puzzle[(bigi + i) * N + (bigj + j)] in blckset: 
                        # print("here in blocks", puzzle[i * N + j], "Coordinates are", i, j)
                        # sys.exit(0)
                        return False
                    blckset.add(puzzle[(bigi + i) * N + (bigj + j)])

    return True


def forwardLook(puzzle, solvedindices):
    for solvedindex in solvedindices:  # for every solved index
        constraintset = constraints[solvedindex]  # The neighbors of this solved index
        for constraintind in constraintset:  # I need to remove the value of the solved index in each neighbor
            oldpuzzle = puzzle[constraintind]  # I need this to see if replace changed anything
            puzzle[constraintind] = puzzle[constraintind].replace(puzzle[solvedindex], "")
            if (oldpuzzle != puzzle[constraintind]):  # If something actually changed right now in this replace
                if len(puzzle[constraintind]) == 1:
                    solvedindices.append(constraintind)

            if len(puzzle[constraintind]) == 0: # If no val works here, it's a bad puzzle so we need to backtrack
                return None
            
    return puzzle


def constraintPropagation(puzzle):
    solvedindices = []
    for possival in symbollist:
        for row in rowsetlist:
            occurcnt, changeind = 0, -1
            for rowind in row:  # for each rowindex in the current row
                if possival in puzzle[rowind]: occurcnt, changeind = occurcnt + 1, rowind
                if occurcnt > 1: break  # if it appears more than two times in one row, than we cannot do our operation.. onto the next row
            if occurcnt == 0: return None, []  # in each row, the possival must appear at least once
            elif occurcnt == 1:  # if it only occurs once in this row, then set it to that position
                puzzle[changeind] = possival
                solvedindices.append(changeind)

        for col in colsetlist:
            occurcnt, changeind = 0, -1
            for colind in col:  # for each colindex in the current column
                if possival in puzzle[colind]: occurcnt, changeind = occurcnt + 1, colind
                if occurcnt > 1: break  # if it appears more than two times in one row, than we cannot do our operation.. onto the next column
            if occurcnt == 0: return None, []  # in each column , the possival must appear at least once
            elif occurcnt == 1:  # if it only occurs once in this column, then set it to that position
                puzzle[changeind] = possival
                solvedindices.append(changeind)

        for blockrow in blocksetlist:  # so blocksetlist is blockrow, blockrow, blockrow.. something like that.. even though it looks like n cubed, it's actually not.. just nsquare
            for block in blockrow:
                occurcnt, changeind = 0, -1
                for blockind in block:  # for each blockindex in the current block
                    if possival in puzzle[blockind]: occurcnt, changeind = occurcnt + 1, blockind 
                    if occurcnt > 1: break  # if it appears more than two times in one row, than we cannot do our operation.. onto the next block
                if occurcnt == 0: return None, []  # in each block, the possival must appear at least once
                elif occurcnt == 1:  # if it only occurs once in this block, then set it to that position
                    puzzle[changeind] = possival 
                    solvedindices.append(changeind)

    if forwardLook(puzzle, solvedindices) == None: return None, []

    return puzzle, solvedindices

# Place the thing and forward look and then constraint propagation, and then forward look from there.. each time checking for failure

def backTracking(puzzle, N, blockheight, blockwidth):
    if checkGoal(puzzle, N, blockheight, blockwidth): 
        return puzzle

    emptpos = get_most_constrainedvar(puzzle)
    for possival in get_sortedvals(puzzle, emptpos): # possival is a string symbol
        newpuzzle = copy(puzzle)
        newpuzzle[emptpos] = possival

        # print("POSITION OF CHANGE", emptpos // 9, emptpos % 9, possival)
        # displayBoard(newpuzzle, 9)
        # input()

        forwardboard = forwardLook(newpuzzle, [emptpos])
        if forwardboard != None:
            constboard, solvedindxs = constraintPropagation(forwardboard)
            while forwardboard != constboard:
                forwardboard = forwardLook(constboard, solvedindxs)
                if forwardboard != None:
                    constboard, solvedindxs = constraintPropagation(forwardboard)
            
        if forwardboard != None:
            newboard = backTracking(forwardboard, N, blockheight, blockwidth)
            if newboard != None: return newboard

    return None
def printBoard(board):
    length = int(len(board)**0.5)
    for x in range(length):
        print(''.join(board[0 + x*length: x*length + length]))
    print()
    print()

def checkBoard(board):
    for rowset in rowsetlist:
        counter=[]


# filename=sys.argv[1]
filename="Unit 2/puzzles_6_variety_hard.txt"
with open(filename) as f:
    puzzles_list = [line.strip() for line in f]
    for puzzle in puzzles_list:
        N = int(len(puzzle) ** 0.5)
        blockheight = int(N ** 0.5)
        while N % blockheight != 0:
            blockheight -= 1
        blockwidth = N // blockheight
        symbollist = list(fullsymbolist[:N])
        
        dictpuzzle = dict()
        presolved = []
        possvals = "".join(symbollist)
        for i in range(len(puzzle)):
            if puzzle[i] != ".":
                dictpuzzle[i] = puzzle[i]
                presolved.append(i)
            else:
                dictpuzzle[i] = possvals

        makeConstraints(N, blockheight, blockwidth)

        forwardLook(dictpuzzle, presolved)
        goalpuzzle = backTracking(dictpuzzle, N, blockheight, blockwidth)
        strgpuzz = ""
        for key in goalpuzzle:
            strgpuzz += goalpuzzle[key]
        #printBoard(strgpuzz)
        #displayBoard(strgpuzz, N)
        print("")

        rowsetlist.clear()
        colsetlist.clear()
        blocksetlist.clear()
        constraints.clear()

# puzzle = "..............3.85..1.2.......5.7.....4...1...9.......5......73..2.1........4...9"
# N = int(len(puzzle) ** 0.5)
# blockheight = int(N ** 0.5)
# while N % blockheight != 0:
#     blockheight -= 1
# blockwidth = N // blockheight
# symbollist = list(fullsymbolist[:N])
  
# dictpuzzle = dict()
# presolved = []
# possvals = "".join(symbollist)
# for i in range(len(puzzle)):
#     if puzzle[i] != ".":
#         dictpuzzle[i] = puzzle[i]
#         presolved.append(i)
#     else:
#         dictpuzzle[i] = possvals

# makeConstraints(N, blockheight, blockwidth)

# forwardLook(dictpuzzle, presolved)
# goalpuzzle = backTracking(dictpuzzle, N, blockheight, blockwidth)
# strgpuzz = ""
# for key in goalpuzzle:
#     strgpuzz += goalpuzzle[key]
# print(strgpuzz)
# displayBoard(strgpuzz, N)
# print("")

# rowsetlist.clear()
# colsetlist.clear()
# blocksetlist.clear()
# constraints.clear()



# puzzle = ".1....1..3....4."
# #puzzle = ".1.............."
# N = int(len(puzzle) ** 0.5)
# blockheight = int(N ** 0.5)
# while N % blockheight != 0:
#     blockheight -= 1
# blockwidth = N // blockheight
# symbollist = list(fullsymbolist[:N])

# dictpuzzle = dict()
# possvals = "".join(symbollist)
# for i in range(len(puzzle)):
#     if puzzle[i] != ".":
#         dictpuzzle[i] = puzzle[i]
#     else:
#         dictpuzzle[i] = possvals

# #dictpuzzle[5] = "21"

# makeConstraints(N, blockheight, blockwidth)
# #forwardLook(dictpuzzle)
# #print(dictpuzzle)
# goalpuzzle = backTracking(dictpuzzle)
# strgpuzz = ""
# for key in goalpuzzle:
#     strgpuzz += goalpuzzle[key]
# displayBoard(strgpuzz, N)


# puzzle = ".1....1..3....4."
# #puzzle = "................"
# N = int(len(puzzle) ** 0.5)
# blockheight = int(N ** 0.5)
# while N % blockheight != 0:
#     blockheight -= 1
# blockwidth = N // blockheight
# symbollist = list(fullsymbolist[:N])

# dictpuzzle = dict()
# possvals = "".join(symbollist)
# for i in range(len(puzzle)):
#     if puzzle[i] != ".":
#         dictpuzzle[i] = puzzle[i]
#     else:
#         dictpuzzle[i] = possvals

# # dictpuzzle[0] = "23"
# # dictpuzzle[1] = "342"
# # dictpuzzle[2] = "1234"
# # dictpuzzle[3] = "23"
# # dictpuzzle[4] = "23"
# # dictpuzzle[5] = "23"
# # dictpuzzle[8] = "23"
# # dictpuzzle[12] = "23"

# makeConstraints(N, blockheight, blockwidth)
# # print(constraintPropagation(dictpuzzle))
# # print(dictpuzzle)


# puzzle = ".7..23....2....1.147.......81......68.......326.6....8....53..1."
# N = int(len(puzzle) ** 0.5)
# blockheight = int(N ** 0.5)
# while N % blockheight != 0:
#     blockheight -= 1
# blockwidth = N // blockheight
# symbollist = list(fullsymbolist[:N])

# print(puzzle, N, blockheight, blockwidth)
# makeConstraints(N, blockheight, blockwidth)
# print(backTracking(puzzle))

# #puzzle = "1234348437373842"
# puzzle = "3..414......4..3"
# N = int(len(puzzle) ** 0.5)
# blockheight = int(N ** 0.5)
# while N % blockheight != 0:
#     blockheight -= 1
# blockwidth = N // blockheight
# symbollist = list(fullsymbolist[:N])
# displayBoard(puzzle, N)
# makeConstraints(puzzle, N, blockheight, blockwidth)
# # print(rowsetlist)
# # print(colsetlist)
# # print(blocksetlist)
# # print(constraints)

# # print(get_next_unassignedvar(puzzle))
# # print(get_sortedvals(puzzle, 8))

# print(backTracking(puzzle, N))
