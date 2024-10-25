import sys
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
    for val in symbol_set:
        if val not in result:
            result[val]=0
    print(result)
    
  
def get_next_unassigned_pos(state: str):
    if '.' in state:
        return state.index('.')
    return None

def goal_test(state: str):
    if(get_next_unassigned_pos(state) is None):
        return True
    return False
def get_sorted_values(state, next_pos, symbol_set: set, pos_conflicts: set):
    possibleVals=symbol_set.copy()
    possibleVals.remove('.')
    for pos in pos_conflicts:
        if(state[pos] in possibleVals):
            possibleVals.remove(state[pos])
    return possibleVals

def sudoku_backtracking(state, symbol_set, pos_constraints):
    if goal_test(state): 
        return state
    var=get_next_unassigned_pos(state)
    sortedVals=get_sorted_values(state, var, symbol_set, pos_constraints[var])
    for val in sortedVals:
        test=state[:var]+val+state[var+1:]
        result=sudoku_backtracking(test, symbol_set, pos_constraints)
        if result is not None:
            return result
    return None

#filename=sys.argv[1]
filename="Unit 2/puzzles_2_variety_easy.txt"
with open(filename) as file:
    boards=[line.strip() for line in file]
for board in boards:
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
    symbol_set.add('.')
    
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
    result=sudoku_backtracking(board, symbol_set, pos_constraints)
    print_puzzle(result, N)
    print("")