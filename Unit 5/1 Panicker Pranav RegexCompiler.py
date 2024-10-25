import sys

def displaydfa(dfa, alphabet):
    print("*",end="")
    for letter in alphabet:
        print("\t"+letter,end="")
    print()
    for key in dfa:
        print(key, end="")
        for letter in alphabet:
            if letter in dfa[key]:
                print(f"\t{dfa[key][letter]}",end="")
            else:
                print("\t_",end="")
        print()
def testVal(dfa, finalNodes, test):
    currNode=0
    for letter in test:
        if letter in dfa[currNode]:
            currNode=dfa[currNode][letter]
        else:
            return False
    if currNode in finalNodes:
        return True
    else:
        return False
def regexToNFAwE(regex):
    nfawe=dict()
    currNode=0
    finalNodes=list()
    nfawe[currNode]=dict()
    inGroup=False
    group=""
    for val in regex:
        

        
        if(val=="("):
            inGroup=True
        elif(val==")"):
            inGroup=False
            nfawe[currNode][group]=currNode+1
        elif inGroup:
          group+=val
          continue
        elif(val=="a"|val=="b"):
            nfawe[currNode][val]==currNode+1
            currNode+=1
        elif(val=="?"):
            nfawe[currNode-1]["eps"]=currNode

        


def main():
    regex=sys.argv[1]
    dfaTest=sys.argv[2]
    alphabet="ab"
    displaydfa(dfa,alphabet)
    print(f"Final nodes: {finalNodes}")
    with open(arg2) as dfaTest:
        for line in dfaTest:
            print(f"{testVal(dfa,finalNodes,line.strip())} {line.strip()}") 