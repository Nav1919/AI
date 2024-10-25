from math import log
import random
import sys

#ALPHABET="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET="ETAOINSRHLDCUMFPGWYBVKXJQZ"
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8
POS=list(range(26))


cipher="XRPHIWGSONFQDZEYVJKMATUCLB"
alphdict=dict()
cipherdict=dict()
for i in range(26):
    alphdict[ALPHABET[i]]=i
    cipherdict[cipher[i]]=i

def encode(word: str, cipher: str):
    word=word.upper()
    ret=""
    for char in word:
        if char in ALPHABET:
            ret+=cipher[ALPHABET.index(char)]
        else:
            ret+=char
    return ret
def decode(word: str, cipher: str):
    ret=""
    for char in word:
        if char in ALPHABET:
            ret+=ALPHABET[cipher.index(char)]
        else:
            ret+=char
    return ret

GRAMSCORES=dict()
with open(f"ngrams.txt") as ngrams_file:
    for line in ngrams_file:
        vals=line.split()
        GRAMSCORES[vals[0]]=log(int(vals[1]),2)

def fitness(n, decoded_string):
    fitnessScore=0
    for i in range(n,len(decoded_string)+1):
        ngram=decoded_string[i-n:i]
        if ngram in GRAMSCORES:
            fitnessScore+=GRAMSCORES[ngram]
    return fitnessScore


encoded_message="""
NU XTZEIMYTNEVZ INUHU YM, ZML SPYVI NXILNFFZ XNFF IVPU N API VNTD. NU PI ILTWU MLI, P XNW YM N FMWY JNZ
JPIVMLI LUPWY NWZ MC IVNI YFZEV IVNI ITNDPIPMWNFFZ CMFFMJU 'D' NI NFF. PUW'I IVNI ULTETPUPWY? P CMLWD
IVPU ULTETPUPWY, NWZJNZ! NW NLIVMT JVM NFUM CMLWD IVPU ULTETPUPWY, FMWY NYM, NXILNFFZ FMUI SNWZ SMWIVU
JTPIPWY N AMMH - N CLFF CPXIPMWNF UIMTZ - JPIVMLI IVNI YFZEV NI NFF. NSNRPWY, TPYVI?"""#sys.argv[1]
def generate_cipher():
    return ''.join(random.sample(ALPHABET,len(ALPHABET)))
def mutate(currcipher):
    swap=random.sample(POS,2)
    if swap[1]<swap[0]:
        curr=swap[1]
        swap[1]=swap[0]
        swap[0]=curr
    testcipher=currcipher[:swap[0]]+currcipher[swap[1]]+currcipher[swap[0]+1:swap[1]]+currcipher[swap[0]]+currcipher[swap[1]+1:]
    return testcipher

def hill_climbing(encoded_message):
    maxFitnessScore=0
    testcipher=generate_cipher()
    # print(testcipher)
    currcipher=""
    while(True):
        # print(testcipher)
        decoded_message=decode(encoded_message,testcipher)
        fitnessScore=fitness(4,decoded_message)+fitness(3,decoded_message)+fitness(1,decoded_message)
        if fitnessScore>maxFitnessScore:
            maxFitnessScore=fitnessScore
            currcipher=testcipher
            print(decoded_message)
            print()
        testcipher=mutate(currcipher,POS)
# hill_climbing(encoded_message)
def generate_population():
    pop_list=list()
    i=0
    while i<POPULATION_SIZE:
        new=generate_cipher()
        if new not in pop_list:
            pop_list.append(new)
            i+=1
    return pop_list
def find_clones(population, population_scores):
    clones=list()
    for val in population:
        if len(clones)==NUM_CLONES and population_scores[clones[-1]]>population_scores[val]:
            continue
        for i in range(NUM_CLONES):
            if i>=len(clones):
                clones.append(val)
                break
            elif population_scores[clones[i]]<population_scores[val]:
                curr=val
                val=clones[i]
                clones[i]=curr
    return clones
def get_population_scores(population):
    return {i:fitness(4,m:=decode(encoded_message,i))+fitness(3,m)+fitness(1,m) for i in population}
def rank(tourney,population_scores):
    if len(tourney) > 1:
  
         # Finding the mid of the array
        mid = len(tourney)//2
  
        # Dividing the array elements
        l = tourney[:mid]
  
        # into 2 halves
        r = tourney[mid:]
  
        # Sorting the first half
        rank(l,population_scores)
  
        # Sorting the second half
        rank(r,population_scores)
  
        i = j = k = 0
  
        # Copy data to temp arrays L[] and R[]
        while i < len(l) and j < len(r):
            if population_scores[l[i]] >= population_scores[r[j]]:
                tourney[k] = l[i]
                i += 1
            else:
                tourney[k] = r[j]
                j += 1
            k += 1
  
        # Checking if any element was left
        while i < len(l):
            tourney[k] = l[i]
            i += 1
            k += 1
  
        while j < len(r):
            tourney[k] = r[j]
            j += 1
            k += 1
  
def run_tournament(population, population_scores):
    tourneypop=random.sample(population,TOURNAMENT_SIZE*2)
    pop1=tourneypop[:TOURNAMENT_SIZE]
    pop2=tourneypop[TOURNAMENT_SIZE:]
    # print(pop1)
    rank(pop1,population_scores)
    # print(pop1)
    rank(pop2,population_scores)
    i=0
    while random.random()>TOURNAMENT_WIN_PROBABILITY and i!=TOURNAMENT_SIZE-1:
        i+=1
    j=0
    while random.random()>TOURNAMENT_WIN_PROBABILITY and j!=TOURNAMENT_SIZE-1:
        j+=1
    return (pop1[i],pop2[j])
def breed(parent1,parent2):
    child=" "*26 #new
    # child=[""]*26
    crossovers=random.sample(POS,CROSSOVER_LOCATIONS)
    for val in crossovers:
        child=child[:val]+parent1[val]+child[val+1:] #new
        # child[val]=parent1[val]
    currPos=0
    for val in parent2:
        while currPos<len(child) and child[currPos]!=" ":
            currPos+=1
        if(currPos>=len(child)):
            break
        if val not in child:
            child=child[:currPos]+val+child[currPos+1:]
            # child[currPos]=val
    return child #"".join(child)
    
def breeding(parent1, parent2, next_generation):
    while len(next_generation)<POPULATION_SIZE:
        new=breed(parent1,parent2)
        if random.random()<MUTATION_RATE:
            new=mutate(new)
            # pos=random.randint(0,24)
            # print(pos)
            # new=new[:pos]+new[pos+1]+new[pos]+new[pos+2:]
            # print(new[pos+2:])
        if new not in next_generation:
            next_generation.append(new)

def print_decoded(encoded_message,population_scores):
    best=""
    bestScore=0
    for cipher in population_scores:
        if population_scores[cipher]>bestScore:
            bestScore=population_scores[cipher]
            best=cipher
    print(decode(encoded_message,best))

def genetic_algorithm(message):
    population=generate_population()
    i=0
    for i in range(500):
        print(i)
        population_scores=get_population_scores(population)
        print_decoded(message,population_scores)
        next_generation=find_clones(population,population_scores)
        # print(population_scores)
        # print(next_generation)
        (parent1,parent2)=run_tournament(population,population_scores)
        breeding(parent1,parent2,next_generation)
        population=next_generation

genetic_algorithm(encoded_message)