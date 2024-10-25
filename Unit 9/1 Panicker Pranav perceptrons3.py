import sys
def get_binary(val,bits):
    ret="{0:b}".format(val)
    if len(ret)<bits:
        ret="0"*(bits-len(ret))+ret
    return ret
def truth_table(bits,n):
    binary=get_binary(n,pow(2,bits))
    table=list()
    index=0
    for i in range(pow(2,bits)-1,-1,-1):
        val=get_binary(i,bits)
        curr=list()
        for j in val:
            curr.append(int(j))
        table.append((tuple(curr),int(binary[index])))
        index+=1
    return tuple(table)
def pretty_print_tt(table):
    dim=len(table[0][0])
    for i in range(dim):
        print(f"In{i+1}",end="\t")
    print(f"|Out")
    for i in table:
        for j in i[0]:
            print(j,end='\t')
        print(f"|{i[1]}")
def step(num):
    return int(num>0)
def dot(v1,v2):
    sum=0
    for i in range(len(v1)):
        sum+=v1[i]*v2[i]
    return sum
def perceptron(A, w, b, x):
    return A(dot(w,x)+b)

input=sys.argv[1][1:-1].split(", ")
# XOR HAPPENS HERE
def xor(x):
    h1=perceptron(step,(1,1),0,x)
    h2=perceptron(step,(-1,-2),3,x)
    return perceptron(step,(1,2),-2,(h1,h2))

print(xor((int(input[0]),int(input[1]))))