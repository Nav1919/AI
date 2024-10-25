import sys
from math import log2
import matplotlib.pyplot as plt
from random import sample
from random import randrange as rr
from random import shuffle
DATA=list()
filename=sys.argv[1]
with open(filename) as f:
    first=True
    for line in f:
        if first:
            CATEGORIES=tuple(line.strip().split(','))
            first=False
            continue
        else:
            DATA.append(tuple(line.strip().split(',')))

def calcEntropy(data):
    options=dict()
    for val in data:
        if val[-1] not in options:
            options[val[-1]]=1
        else:
            options[val[-1]]+=1
    entropy=0
    for total in options.values():
        prob=total/len(data)
        entropy-=(prob*log2(prob))
    return entropy

def calcEntropyForFeature(data, feature):
    index=CATEGORIES.index(feature)
    options=dict()
    for val in data:
        if val[index] not in options:
            options[val[index]]=dict()
            options[val[index]][val[-1]]=1
        elif val[-1] not in options[val[index]]:
            options[val[index]][val[-1]]=1
        else:
            options[val[index]][val[-1]]+=1
    entropy=0
    for option in options:
        total=sum(options[option].values())
        categoricalEntropy=0
        for result in options[option].values():
            prob=result/total
            categoricalEntropy-=(prob*log2(prob))
        weight=total/len(data)
        entropy+=weight*categoricalEntropy
    return entropy
class Node:
    def __init__(self, feature_index, threshold, children, info_gain, depth):
        self.feature_index=feature_index    
        self.threshold=threshold
        self.children=children
        self.info_gain=info_gain
        self.depth=depth
    def print(self):
        print('\n'+self.depth*"  "+f"* {self.threshold}")
        for key in self.children:
            if self.children[key].isLeaf():
                print((self.depth+1)*"  "+f"* {key}",end="")
                self.children[key].print()
        for key in self.children:
            if not self.children[key].isLeaf():
                print((self.depth+1)*"  "+f"* {key}",end="")
                self.children[key].print()
    def isLeaf(self):
        return False
    def traverse(self, feature_vector):
        if feature_vector[self.feature_index] in self.children:
            return self.children[feature_vector[self.feature_index]]
        else:
            return sample(list(self.children.values()),1)[0]

class Leaf:
    def __init__(self,value):
        self.value=value
    def print(self):
        print(f" --> {self.value}")
    def isLeaf(self):
        return True

def makeTree(data, depth):
    entropy=calcEntropy(data)
    if(entropy==0):
        node= Leaf(data[0][-1])
        return node
    bestCategory=""
    maxInformationGain=0
    for category in CATEGORIES[:-1]:
        informationGain=entropy-calcEntropyForFeature(data,category)
        if informationGain>maxInformationGain:
            maxInformationGain=informationGain
            bestCategory=category
    if maxInformationGain==0:
        node=Leaf(data[rr(0,len(data))][-1])
        return node

    next_data=dict()
    index=CATEGORIES.index(bestCategory)
    for val in data:
        if val[index] not in next_data:
            next_data[val[index]]=list()
        next_data[val[index]].append(val)
    children=dict()
    for key in next_data:
        children[key]=makeTree(next_data[key],depth+2)
    node= Node(index, bestCategory, children, maxInformationGain,depth)
    return node
def classify(root: Node, point):
    traversal=root
    while not traversal.isLeaf():
        traversal=traversal.traverse(point)
    return traversal.value
shuffle(DATA)
test_size=int(sys.argv[2])
TEST=DATA[-test_size:]
DATA=DATA[:-test_size]
min_training_size=int(sys.argv[3])
max_training_size=int(sys.argv[4])
training_step=int(sys.argv[5])
#Normal
sizeVsAccuracyNormal=list()
for SIZE in range(min_training_size,max_training_size+1,training_step):
    TRAIN=sample(DATA,SIZE)
    while(calcEntropy(TRAIN)==0):
        TRAIN=sample(DATA,SIZE)
    tree=makeTree(TRAIN,0)
    total_correct=0
    for val in TEST:
        classification=classify(tree,val)
        if classification==val[-1]:
            total_correct+=1
    sizeVsAccuracyNormal.append((SIZE,total_correct/len(TEST)))
plt.scatter(*zip(*sizeVsAccuracyNormal),color="red",label="Normal")
#Random Forests
sizeVsAccuracyRandomForests=list()
forestSize=10
for SIZE in range(min_training_size,max_training_size+1,training_step):
    freq_table=list()
    for i in range(test_size):
        freq_table.append(dict())
    for i in range(forestSize):
        TRAIN=sample(DATA,SIZE//10)
        while(calcEntropy(TRAIN)==0):
            TRAIN=sample(DATA,SIZE//10)
        tree=makeTree(TRAIN,0)
        total_correct=0
        index=0
        for val in TEST:
            classification=classify(tree,val)
            if classification not in freq_table[index]:
                freq_table[index][classification]=1
            else:
                freq_table[index][classification]+=1
            index+=1
    total_correct=0 
    for i in range(test_size):
        max=0
        bestGuess=""
        d=freq_table[i]
        for key in d:
            if d[key]>max:
                max=d[key]
                bestGuess=key
        if bestGuess==TEST[i][-1]:
            total_correct+=1
    sizeVsAccuracyRandomForests.append((SIZE,total_correct/len(TEST)))
plt.scatter(*zip(*sizeVsAccuracyRandomForests),color="blue",label="Random Forests")

plt.title(filename[:-4])
plt.legend()
plt.xlabel("TRAINING SET SIZE")
plt.ylabel("ACCURACY")
plt.show()