import sys
# dfaSpecfile=sys.argv[1]
# dfaSpecfile="Unit 5\dfa_ex_spec.txt"
# dfaTestfile=sys.argv[2]
# dfaTestfile="Unit 5\dfa_ex_tests.txt"
arg1="5"#sys.argv[1]
arg2="Unit 5\\tests.txt"#sys.argv[2]
# arg1="1"
# arg2="Unit 5\tests.txt"

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

if(not arg1.isnumeric()):
    dfaSpecfile=arg1
    dfaTestfile=arg2
    with open(dfaSpecfile) as dfaSpec:
        spec=[line.strip() for line in dfaSpec]
    alphabet=spec[0]
    nodes=int(spec[1])
    finalNodes=list()
    for val in spec[2].split(" "):
        finalNodes.append(int(val))
    currNode=0
    dfa=dict()
    for i in range(nodes):
        dfa[i]=dict()
    for line in spec[4:]:
        line=line.strip()
        if len(line)==0:
            continue
        if line.isdigit():
            currNode=int(line)
        else:
            path=line.split(" ")
            dfa[currNode][path[0]]=int(path[1])    
    displaydfa(dfa,alphabet)
    print(f"Final nodes: {finalNodes}")
    with open(dfaTestfile) as dfaTest:
        for line in dfaTest:
            print(f"{testVal(dfa,finalNodes,line.strip())} {line.strip()}")
else:
    dfa1={
        0:{
            "a":1
        },
        1:{
            "a":2
        },
        2:{
            "b":3
        },
        3:{}
    }
    final1=[3]

    dfa2={
        0:{
            "0":0,
            "1":1,
            "2":0
        },
        1:{
            "0":0,
            "1":1,
            "2":0
        }
        
    }
    final2=[1]

    dfa3={
        0:{
            "a":0,
            "b":1,
            "c":0
        },
        1:{
            "a":1,
            "b":1,
            "c":1
        }
    }
    final3=[1]

    dfa4={
        0:{
            "0":1,
            "1":0
        },
        1:{
            "0":0,
            "1":1
        }
    }
    final4=[0]

    dfa5={
        0:{
            "0":1,
            "1":2,
        },
        1:{
            "0":0,
            "1":3,
        },
        2:{
            "0":3,
            "1":0,
        },
        3:{
            "0":2,
            "1":1,
        }

    }
    final5=[0]

    dfa6={
        0:{
            "a":1,
            "b":0,
            "c":0
        },
        1:{
            "a":0,
            "b":2,
            "c":0
        },
        2:{
            "a":0,
            "b":0,
            "c":3
        },
        3:{
            "a":3,
            "b":3,
            "c":3
        }
    }
    final6=[0,1,2]

    dfa7={
        0:{
            "0":0,
            "1":1,
        },
        1:{
            "0":2,
            "1":1,
        },
        2:{
            "0":2,
            "1":3,
        },
        3:{
            "0":2,
            "1":4,
        },
        4:{
            "0":4,
            "1":4,
        }
    }
    final7=[4]

    if arg1=="1":
        dfa=dfa1
        finalNodes=final1
        alphabet="ab"
    elif arg1=="2":
        dfa=dfa2
        finalNodes=final2
        alphabet="012"
    elif arg1=="3":
        dfa=dfa3
        finalNodes=final3
        alphabet="abc"
    elif arg1=="4":
        dfa=dfa4
        finalNodes=final4
        alphabet="01"
    elif arg1=="5":
        dfa=dfa5
        finalNodes=final5
        alphabet="01"
    elif arg1=="6":
        dfa=dfa6
        finalNodes=final6
        alphabet="abc"
    elif arg1=="7":
        dfa=dfa7
        finalNodes=final7
        alphabet="01"
    else:
        print("Invalid argument")
        quit()
    displaydfa(dfa,alphabet)
    print(f"Final nodes: {finalNodes}")
    with open(arg2) as dfaTest:
        for line in dfaTest:
            print(f"{testVal(dfa,finalNodes,line.strip())} {line.strip()}") 