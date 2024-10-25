import sys
import numpy as np
def step(num):
    return int(num>0)
def dot(v1,v2):
    sum=0
    for i in range(len(v1)):
        sum+=v1[i]*v2[i]
    return sum
def perceptron(A, w, b, x):
    return A(dot(w,x)+b)


def step_vec(x):
    return np.heaviside(x,0)
def sigmoid(x):
   return 1/(1+np.exp(-x))

def p_net(A_vec, weights, biases, input):
    a=[input]
    n=len(weights)
    for i in range(1,n):
        a.append(A_vec(np.add(np.matmul(weights[i],a[i-1]),biases[i])))
    return a[n-1]

if len(sys.argv)==2:
    arg=sys.argv[1][1:-1].split(", ")
    input=np.array([[int(arg[0])],[int(arg[1])]])
    weights=[None,np.array([[1,1],[-1,-2]]),np.array([[1,2]])]
    biases=[None,np.array([[0],[3]]),np.array([[-2]])]
    # XOR HAPPENS HERE
    print(int(p_net(step_vec,weights, biases, input)))

elif len(sys.argv)==3:
    
    x=float(sys.argv[1])
    y=float(sys.argv[2])
    input=np.array([[x],[y]])
    weights=[None,np.array([[-1,-1],[-1,1],[1,-1],[1,1]]),np.array([[1,1,1,1]])]
    biases=[None,np.array([[1],[1],[1],[1]]),np.array([[-3.5]])]
    result=int(p_net(step_vec,weights, biases, input))
    if result==1: print("inside")
    else: print("outside")

elif len(sys.argv)==1:
    
    points=2 * np.random.rand(500, 2) - 1
    misclassified=list()
    weights=[None,np.array([[-1,-1],[-1,1],[1,-1],[1,1]]),np.array([[1,1,1,1]])]
    i=-.9035
    j=-1.3
    biases=[None,np.array([[i],[i],[i],[i]]),np.array([[j]])]
    correct=0
    for val in points:
        result=p_net(sigmoid,weights, biases, np.array([val]).transpose())
        result=int(result<0.5)
        actual=int(np.linalg.norm(val)<1)
        if actual==result:
            correct+=1
        else:
            print(val)
    print(correct/500)