import sys
def main():
    arg=sys.argv[1]

    if arg=="A":
        print(sum([int(i[0]) for i in sys.argv[2:5]]))

    elif arg=="B":
        print(sum([int(i[0]) for i in sys.argv[2:]]))
    elif arg=="C":
        print([value for value in sys.argv[2:] if int(value) % 3 == 0])
    elif arg=="D":
        fibList=[]
        for value in range(int(sys.argv[2])):
            if(value<=1):
                fibList.append(1)
            else:
                fibList.append(fibList[value-1]+fibList[value-2])
        print(fibList)
    elif arg=="E":
        print([value**2-3*value+2 for value in range(int(sys.argv[2]),int(sys.argv[3])+1)])
        
    elif arg=="F":
        if sum([float(i) for i in sys.argv[2:4]])>float(sys.argv[4]) and sum([float(i) for i in sys.argv[3:5]])>float(sys.argv[2]) and float(sys.argv[2])+float(sys.argv[4])>float(sys.argv[3]):
            s=sum([float(i) for i in sys.argv[2:5]])/2
            print((s*(s-float(sys.argv[2]))*(s-float(sys.argv[3]))*(s-float(sys.argv[4])))**(1/2))
        else:
            print("Error: invalid side lengths")
    elif arg=="G":
        vowCount = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
        for letter in sys.argv[2]:
            if letter.lower() in 'aeiou':
                vowCount[letter.lower()]=vowCount.get(letter.lower())+1
        print(vowCount)
    else:
        print("Error: letter must be between A-G inclusive")

if __name__=="__main__":
    main()
