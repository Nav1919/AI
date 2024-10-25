import sys
from time import perf_counter
def print_puzzle(board, N):
    i=0
    while i<len(board):
        print(" ".join(board[i:i+N]))
        i+=N

def count_symbols(board,symbol_set):
    result = {}
    for i in board:
        if i in result:
            result[i] += 1
        else:
            result[i] = 1
    equals=result['1']
    validSol=True
    for val in symbol_set:
        if val not in result:
            result[val]=0
            validSol=False
        if(result[val]!=equals):
            validSol=False
    print(result)
    return validSol


def get_possible_values(state, symbol_set: set, pos_conflicts: set):
    possibleVals=symbol_set.copy()
    for pos in pos_conflicts:
        if(state[pos] in possibleVals):
            possibleVals.remove(state[pos])
    return possibleVals

def get_board_specs(board):
    N=int(len(board)**0.5)
    if(N**0.5==int(N**0.5)):
        subblock_width=subblock_height=int(N**0.5)
    else:
        subblock_height=int(N**0.5)
        subblock_width=subblock_height+1
        while(N%subblock_height!=0):
            subblock_height-=1
        while(N%subblock_width!=0):
            subblock_width+=1
    possible_symbols="123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbol_set={possible_symbols[i] for i in range(N)}
    return (N,subblock_width, subblock_height, symbol_set)

def get_pos_constraints(N, subblock_height, subblock_width):
    constrain_sets=list()
    for i in range(N):
        row_set=set()
        row_set.update([j for j in range(i*N,(i+1)*N)])
        col_set=set()
        col_set.update([i+j*N for j in range(N)])
        constrain_sets.append(row_set)
        constrain_sets.append(col_set)
    for j in range(0, N, subblock_height):
        for i in range(0, N, subblock_width):
            block_set=set()
            block_set.update([N*(j+hinc)+i+winc for hinc in range(subblock_height) for winc in range(subblock_width)])
            constrain_sets.append(block_set)
    pos_constraints=list()
    for i in range(len(board)):
        curr_pos_constraints=set()
        for j in constrain_sets:
            if(i in j):
                curr_pos_constraints.update(j)
        curr_pos_constraints.remove(i)
        pos_constraints.append(curr_pos_constraints)
    return pos_constraints
def make_board_list(board: str, pos_constraints: list, symbol_set: set):
    board_list=list()
    for i in range(len(board)):
        board_list.append(get_possible_values(board, symbol_set, pos_constraints[i]))
    return board_list
def get_most_constrained_var(board_list: list):
    min_constraints=10000
    min_pos=-1
    for i in range(0,len(board_list)):
        if(isinstance(board_list[i],set) and len(board_list[i])<min_constraints):
            min_constraints=len(board_list[i])
            min_pos=i
    return min_pos
def forward_looking(board_list: list, start: int, pos_constraints: list):
    # for var in pos_list:
    #     val=board_list[var]
    #     #print(pos_constraints)
    #     for pos in pos_constraints[var]:
    #         if isinstance(board_list[pos], set) and val in board_list[pos]:
    #             #print(pos, val)
    #             board_list[pos]=board_list[pos].copy()
    #             board_list[pos].remove(val)
    #             if not board_list[pos]:
    #                 return None
        
    #Added
    pos_list=list()
    pos_list.append(start)
    while pos_list:
        var=pos_list.pop()
        if isinstance(board_list[var],set):
            board_list[var]=next(iter(board_list[var]))
        val=board_list[var]
        #print(pos_constraints)
        for pos in pos_constraints[var]:
            if isinstance(board_list[pos], set) and val in board_list[pos]:
                #print(pos, val)
                board_list[pos]=board_list[pos].copy()
                board_list[pos].remove(val)
                if not board_list[pos]:
                    return None
                if len(board_list[pos])==1:
                    pos_list.append(pos)
    return board_list
# def constraint_prop(board_list: list, constraint_sets: list):
#     for group in constraint_sets:
#         countVals=dict()
#         for pos in group:
#             if isinstance(board_list[pos],set):


def sudoku_backtracking(board_list: list, symbol_set: set, pos_constraints: list):
    var=get_most_constrained_var(board_list)
    #print(board_list[var])
    if(var==-1):
        return board_list
    for val in board_list[var]:
        new_board=board_list.copy()
        #print(new_board[var])
        new_board[var]=val
        #print(new_board[var])
        #print("")
        checked_board=forward_looking(new_board, var, pos_constraints)
        if checked_board is not None:
            result=sudoku_backtracking(new_board, symbol_set, pos_constraints)
            if result is not None:
                return result
    return None


#filename=sys.argv[1]
filename="Unit 2/puzzles_5_standard_hard.txt"
with open(filename) as file:
    boards=[line.strip() for line in file]
nonecount=0
functional=0
start=perf_counter()
for board in boards:

    (N, subblock_width, subblock_height, symbol_set)=get_board_specs(board)
    pos_constraints=get_pos_constraints(N, subblock_height, subblock_width)
    board_list=make_board_list(board, pos_constraints, symbol_set)
    #print(N)
    #print(board_list)
   # print(board_list)
    #print(board_list)
    mostConstrainedPos=get_most_constrained_var(board_list)
    while mostConstrainedPos>=0 and len(board_list[mostConstrainedPos])==1:
        checked_board=forward_looking(board_list, mostConstrainedPos, pos_constraints)
        if checked_board is not None:
            board_list=checked_board
        mostConstrainedPos=get_most_constrained_var(board_list)
    
    result=sudoku_backtracking(board_list, symbol_set, pos_constraints) 
    if(result==None):
        nonecount+=1
    else:
        functional+=1
    print(result)
    print(count_symbols(result, symbol_set))
    #print(len(result))
print(perf_counter()-start)
print(nonecount)
print(functional)
