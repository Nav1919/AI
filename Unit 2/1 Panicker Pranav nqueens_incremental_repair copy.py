from time import perf_counter
import random

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True
def getWorstRow(state):
    mostConflicts=0
    worstStates=list()
    for row in range(len(state)):
        conflicts=countConflicts(state, row, state[row])
        if(conflicts>mostConflicts):
            mostConflicts=conflicts
            worstStates.clear()
            worstStates.append(row)
        elif(conflicts==mostConflicts):
            worstStates.append(row)
    return (random.choice(worstStates),mostConflicts)


def countConflicts(state, row, col):
    conflicts=0
    for r in range(len(state)):
        if r==row:
            continue
        if(state[r]==col):
            conflicts+=1
            continue
        c=state[r]
        rowdiff=r-row
        if(abs(rowdiff)==abs(col-c)):
            conflicts+=1
    
    return conflicts
def repairState(state, worstRow, leastConflicts):
    possibleCols=list()
    initialCol=state[worstRow]
    for newCol in range(len(state)):
        if newCol==initialCol:
            continue
        conflicts=countConflicts(state, worstRow, newCol)
        if(conflicts<leastConflicts):
            leastConflicts=conflicts
            possibleCols.clear()
            possibleCols.append(newCol)
        elif(conflicts==leastConflicts):
            possibleCols.append(newCol)
    if possibleCols:
        return random.choice(possibleCols)
    else:
        return -1
def countTotalConflicts(state):
    total=0
    for i in range(1,len(state)):
        for j in range(i):
            if(state[i]==state[j]):
                total+=1
            elif(abs(state[i]-state[j])==abs(i-j)):
                total+=1
    return total
def queens_incremental(state):
    worstRow,mostConflicts=getWorstRow(state)
    while(mostConflicts>0):
        print(f"{state}, conflicts: {countTotalConflicts(state)}")
        newCol=repairState(state, worstRow, mostConflicts)
        if(newCol<0):
            worstRow,mostConflicts=getWorstRow(state)
            continue
        state[worstRow]=newCol
        worstRow,mostConflicts=getWorstRow(state)

    print(f"{state}, conflicts: {mostConflicts}")
    return state
    

    
def main():
    #31,33
    for j in range(31,33):
        state=[i for i in range(j)]
        start=perf_counter()
        sol=queens_incremental(state)
        end=perf_counter()
        #sol=[23, 21, 10, 5, 7, 29, 13, 17, 22, 26, 16, 30, 6, 4, 1, 27, 9, 14, 3, 20, 0, 19, 11, 15, 8, 25, 2, 2, 24, 28, 18]
        # print(f"Solution valid: {test_solution(sol)}")
        print(f"Solution valid: {test_solution(sol)}")
        print(f"Runtime: {end-start} seconds\n")
      

if __name__ == "__main__":
    main()