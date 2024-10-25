from time import perf_counter


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
def get_next_unassigned_var(state):
    if None in state:
        return state.index(None)
    return None
def edgeOrder(state):
    size=len(state)


def goal_test(state):
    if(get_next_unassigned_var(state) is None):
        return True
    return False
def edgeOrder(vals):
    added=set()
    retOrder=list()
    for i in range(len(vals)):
        if(i==len(vals)//2 and len(vals)%2==1):
            retOrder.append(i)
            break
        elif len(vals)-i-1 not in added:
            retOrder.append(i)
            retOrder.append(len(vals)-i-1)
            added.add(i)
        else:
            break
    return retOrder
def middleOrder(vals):
    retOrder=list()
    start=len(vals)//2
    if len(vals)%2==1:
        retOrder.append(start)
        start+=1
    for i in range(start, len(vals)):
        retOrder.append(i)
        retOrder.append(len(vals)-i-1)
    return retOrder
def get_sorted_values(state, var):
    sortedVals=list()
    validPos=True
    row=var
    for col in range(len(state)):
        for r in range(row):
            rowdiff=row-r
            c=state[r]
            if(col==c or col==c-rowdiff or col==c+rowdiff):
                validPos=False
                break
        if validPos:
            sortedVals.append(col)
        validPos=True
    return sortedVals
        

        

def queens_backtracking(state, checkorder):
    if goal_test(state): 
        return state
    var=get_next_unassigned_var(state)
    copy=state.copy()
    sortedVals=get_sorted_values(state, var)
    if(checkorder):
        order=middleOrder(sortedVals)
    else:
        order=edgeOrder(sortedVals)
    for pos in order:
        copy[var]=sortedVals[pos]
        result=queens_backtracking(copy, not checkorder)
        if result is not None:
            return result
    return None
    
def main():
    for i in range(31,33):
        start=perf_counter()
        sol=queens_backtracking([None]*i,True)
        end=perf_counter()
        print(f"Sol for size {i}: \n{sol}\nin {end-start} seconds")
        print(f"Solution valid: {test_solution(sol)}\n")

if __name__ == "__main__":
    main()