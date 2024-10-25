import sys
from math import log2
data=list()
filename=sys.argv[1]
with open(filename) as f:
    first=True
    for line in f:
        if first:
            CATEGORIES=tuple(line.strip().split(','))
            first=False
            continue
        else:
            data.append(tuple(line.strip().split(',')))
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
        if self.depth==0:
            print(f"* Starting Entropy: {calcEntropy(data)}",end="")
        print('\n'+self.depth*"  "+f"* {self.threshold} (information gain: {self.info_gain})")
        for key in self.children:
            if self.children[key][0].isLeaf():
                print((self.depth+1)*"  "+f"* {key}",end="")
                self.children[key][0].print()
        for key in self.children:
            if not self.children[key][0].isLeaf():
                print((self.depth+1)*"  "+f"* {key} (with current entropy {self.children[key][1]})",end="")
                self.children[key][0].print()
    def isLeaf(self):
        return False

class Leaf:
    def __init__(self,value):
        self.value=value
    def print(self):
        print(f" --> {self.value}")
    def isLeaf(self):
        return True

# print(e:=calcEntropy(data))
# print(CATEGORIES[:-1])
def makeTree(data, depth):
    entropy=calcEntropy(data)
    if(entropy==0):
        node= Leaf(data[0][-1])
        return (node,0)
    bestCategory=""
    maxInformationGain=0
    for category in CATEGORIES[:-1]:
        informationGain=entropy-calcEntropyForFeature(data,category)
        if informationGain>maxInformationGain:
            maxInformationGain=informationGain
            bestCategory=category
    next_data=dict()
    index=CATEGORIES.index(bestCategory)
    for val in data:
        if val[index] not in next_data:
            next_data[val[index]]=list()
        next_data[val[index]].append(val)
    children=dict()
    for key in next_data:
        children[key]=makeTree(next_data[key],depth+2)
    node= (Node(index, bestCategory, children, maxInformationGain,depth),entropy)
    return node

    
    

tree=makeTree(data,0)[0]
original_stdout = sys.stdout
tree.print()

with open('treeout.txt', 'w') as f:
    sys.stdout = f
    tree.print()
    sys.stdout=original_stdout