import sys
#Pranav Panicker, Mihir Kulshreshtha
def score(word, word_set, start_parity):
    if word in word_set:
        if len(word)%2==start_parity:
            return 1
        else:
            return -1
    return 0
def get_possible_moves(word, word_set):
    return {pos[:len(word)+1] for pos in word_set}
def update_set(word, word_set):
    return {pos for pos in word_set if len(pos)>=len(word) and pos[:len(word)]==word}
def player_move(word, word_set, start_parity):
    curr_score=score(word, word_set, start_parity)
    if curr_score!=0:
        return curr_score
    max=-2
    for move in get_possible_moves(word, word_set):

        curr=opponent_move(move, update_set(move, word_set), start_parity)
        if curr>max:
            max=curr
        if max==1:
            break
    return max

def opponent_move(word, word_set, start_parity):
    curr_score=score(word, word_set, start_parity)
    if curr_score!=0:
        return curr_score
    min=2

    for move in get_possible_moves(word, word_set):

        curr=player_move(move, update_set(move, word_set), start_parity)
        if curr<min:
            min=curr
        if min==-1:
            break
    return min

def find_winning_moves(start, word_set, start_parity):
    winning_moves=[]
    for move in get_possible_moves(start, word_set):
        curr=opponent_move(move, update_set(move, word_set), start_parity)
        if(curr==1):
            winning_moves.append(move[-1:])
        
    return winning_moves
filename=sys.argv[1]
with open(filename) as words_file:
    word_list=[line.strip().upper() for line in words_file]
min_length=int(sys.argv[2])
state=""
if(len(sys.argv)>3):
    state=sys.argv[3].upper()


word_set = {word for word in word_list if word.isalpha() and len(word)>=len(state) and state==word[:len(state)] and len(word)>=min_length}
start_parity = len(state)%2

winning_moves=find_winning_moves(state, word_set, start_parity)

if(len(winning_moves)==0):
    print("Next player will lose!")
else:
    print(f"Next player can guarantee victory by playing any of these letters: {winning_moves}")