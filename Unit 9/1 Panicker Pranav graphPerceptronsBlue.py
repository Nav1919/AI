from matplotlib import pyplot as plt
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
    return tuple(table[::-1])
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
def check(n, w, b):
    table=truth_table(len(w),n)
    totalCorrect=0
    for i in table:
        estimate=perceptron(step,w,b,i[0])
        if estimate==i[1]:
            totalCorrect+=1
    return totalCorrect/len(table)
def vector_equals(vec1,vec2):
    for i in range(len(vec1)):
        if vec1[i]!=vec2[i]:
            return False
    return True
def generate_perceptron(bits, n, learning_rate):
    table=truth_table(bits,n)
    w=(0,)*bits
    b=0
    prev_w=(-1,)*bits
    prev_b=0
    first=True
    count=0
    while True:
        for x, result in table:
            estimate=perceptron(step, w, b, x)
            error=result-estimate
            w=tuple([w[i]+error*learning_rate*x[i] for i in range(bits)])
            b=b+error*learning_rate
        if not first:
            if vector_equals(prev_w,w) and prev_b==b:
                return table,w,b
        count+=1
        if count==100:
            return w,b
        else: first=False
        prev_w=w
        prev_b=b

bits=2
total=16
fig,axis=plt.subplots(4,4)
for n in range(total):
    table,w,b=generate_perceptron(bits,n,0.1)
    y=n//4
    x=n%4
    axis[y,x].title.set_text(f"#{n}")
    for i,j in table:
        x1,x2=i
        if j==0:
            axis[y,x].plot(x1,x2,marker="o", markersize=2, color='red')

        else:
            axis[y,x].plot(x1,x2,marker="o", markersize=2, color='green')

        
    for i in range(-20,21):
        for j in range(-20,21):
            x1=i/10
            x2=j/10
            if not((x1==0 or x1==1) and (x2==0 or x2==1)):
                if perceptron(step,w,b,(x1,x2))==1:
                    axis[y,x].plot(x1,x2,marker="o", markersize=.1, color='green')

                else:
                    axis[y,x].plot(x1,x2,marker="o", markersize=.1, color='red')


plt.show()