import sys
import numpy as np
def p_net(A_vec, weights, biases, input):
    a=[input]
    n=len(weights)
    for i in range(1,n):
        a.append(A_vec(np.add(np.matmul(weights[i],a[i-1]),biases[i])))
    return a[n-1]
def sigmoid(x):
   return 1/(1+np.exp(-x))
def sigmoid_prime(x):
    a=sigmoid(x)
    return a-a*a
def genRandomMatrix(min,max,rows,cols):
    return (max-min) * np.random.rand(rows, cols) - min
def calc_error(actual,expected):
    return pow(np.linalg.norm(actual-expected),2)/2
def round_result(x, threshold):
    return np.heaviside(x-threshold,0)
if(len(sys.argv)>=2 and sys.argv[1]=='S'):
    inputs=[np.array([[0],[0]]),np.array([[0],[1]]),np.array([[1],[0]]),np.array([[1],[1]])]
    outputs=[np.array([[0],[0]]),np.array([[0],[1]]),np.array([[0],[1]]),np.array([[1],[0]])]
    weights=[None,genRandomMatrix(-1,1,2,2),genRandomMatrix(-1,1,2,2)]
    biases=[None,genRandomMatrix(-1,1,2,1),genRandomMatrix(-1,1,2,1)]

    for epoch in range(10000):
        for i in range(len(inputs)):
            x=inputs[i]
            y=outputs[i]
            a=[x]
            dot=[None]
            n=len(weights)
            for i in range(1,n):
                dot.append(weights[i]@a[i-1]+biases[i])
                a.append(sigmoid(dot[i]))
            delta=[None]*n
            delta[n-1]=sigmoid_prime(dot[n-1])*(y-a[n-1])
            for L in range(n-2,0,-1):
                delta[L]=sigmoid_prime(dot[L])* ((weights[L+1].transpose())@delta[L+1])
            for L in range(1,n):
                biases[L]=biases[L]+0.1*delta[L]
                weights[L]=weights[L]+0.1*(delta[L]@a[L-1].transpose())
    for i in range(len(inputs)):
        x=inputs[i]
        print(f"{x.transpose()}->{p_net(sigmoid,weights,biases,x).transpose()}")
else:#elif(sys.argv[1]=='C'):
    weights=[None, genRandomMatrix(-1,1,12,2),genRandomMatrix(-1,1,4,12),genRandomMatrix(-1,1,1,4)]
    biases=[None,genRandomMatrix(-1,1,12,1),genRandomMatrix(-1,1,4,1),genRandomMatrix(-1,1,1,1)]
    for i in range(1,len(weights)):
        print(weights[i])
        print(biases[i])
        print()
    points=list()
    results=list()
    with open("10000_pairs.txt") as f:
        for line in f:
            temp=line.strip().split()
            val=np.array([[float(temp[0])],[float(temp[1])]])
            points.append(val)
            results.append(int(np.linalg.norm(val)<1))
    learning_rate=2
    for epoch in range(100):
        for i in range(len(points)):
            x=points[i]
            y=results[i]
            a=[x]
            dot=[None]
            n=len(weights)
            for i in range(1,n):
                dot.append(weights[i]@a[i-1]+biases[i])
                a.append(sigmoid(dot[i]))
            delta=[None]*n
            delta[n-1]=sigmoid_prime(dot[n-1])*(y-a[n-1])
            for L in range(n-2,0,-1):
                delta[L]=sigmoid_prime(dot[L])*((weights[L+1].transpose())@delta[L+1])
            for L in range(1,n):
                biases[L]=biases[L]+learning_rate*delta[L]
                weights[L]=weights[L]+learning_rate*(delta[L]@a[L-1].transpose())
        misclassified=0
        for i in range(len(points)):
            x=points[i]
            y=results[i]
            val=int(p_net(sigmoid,weights,biases,x)>0.5)
            if val!=y:
                misclassified+=1
        print(f"Epoch {epoch}: {misclassified} misclassified")
    for i in range(len(points)):
        x=points[i]
        y=results[i]
        print(f"{x.transpose()}->{p_net(sigmoid,weights,biases,x).transpose()}")