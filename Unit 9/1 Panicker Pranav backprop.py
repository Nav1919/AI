import numpy as np
import sys

def sigmoid(x):
   return 1/(1+np.exp(-x))
def sigmoid_prime(x):
    a=sigmoid(x)
    return a-a*a


def train_function( train, expected, weights, bias, lamda, N ):
    a = []
    dot = [None]
    delta = [None]*(N+1)
    
    avg_error = 0

    for index in range( len(train) ):
        x = train[index]
        y = expected[index]
        
        a.append( x )       
        for layer in range(1, N+1):
            dot.append( weights[layer] @ a[layer-1] + bias[layer] )
            a.append( sigmoid(dot[layer]) )   
        avg_error += 0.5 * sum([ (y[i] - a[N][i])**2 for i in range(len(y)) ])
        delta[N] = sigmoid_prime(dot[N])*(y-a[N])       
        for layer in range(N-1, 0, -1):
            delta[layer] = sigmoid_prime(dot[layer]) * (weights[layer+1].transpose() @ delta[layer+1])
        for layer in range(1, N+1):
            bias[layer] = bias[layer] + (lamda * delta[layer])
            weights[layer] = weights[layer] + lamda * (delta[layer] @ (a[layer-1]).transpose())
    
        a = []
        dot = [None]
        delta = [None]*(N+1)
            
    return weights, bias, (avg_error / len(train))

def test_function( data, weights, bias, N ):
    outputs = []
    a = []
    for data_point in data:
        a.append(data_point)
        for layer in range(1, N+1):
            a.append( sigmoid(weights[layer] @ a[layer-1] + bias[layer]) )
        final_output = a[N]
        
        outputs.append((final_output))
        a.clear()
        
    return outputs

if sys.argv[1] == "S":
    
    training_input = [ np.array([[0], [0]]), np.array([[0], [1]]), np.array([[1], [0]]), np.array([[1], [1]]) ]
    expected_output = [ np.array([[0], [0]]), np.array([[0], [1]]),  np.array([[0], [1]]), np.array([[1], [0]]) ]

    N = 2

    weights = [ 2 * np.random.rand(2, 2) - 1 for i in range(N) ]
    weights.insert(0, None)
    bias = [ 2 * np.random.rand(2, 1) - 1 for i in range(N) ]
    bias.insert(0, None)

    lamda = 0.5
    
    for epoch in range(10000):
        weights, bias = train_function( training_input, expected_output, weights, bias, lamda, N )[0:2]
    
    data_points = [np.array([[0], [0]]), np.array([[0], [1]]), np.array([[1], [0]]), np.array([[1], [1]])]
    outputs = test_function( data_points, weights, bias, N )
    
    for output in outputs:
        print(f"{output[0,0]}, {output[1,0]}")
    
if sys.argv[1] == "C":
    
    training_input = []
    expected_output = []
    with open("10000_pairs.txt") as file:
        data = [line.strip().split() for line in file]
        for x, y in data:
            training_input.append(np.array([[float(x)], [float(y)]]))
            if float(x)**2 + float(y)**2 < 1:
                expected_output.append(np.array([[1]]))
            else:
                expected_output.append(np.array([[0]]))
    
    N = 3
    
    weights = [ 2 * np.random.rand(12, 2) - 1, 2 * np.random.rand(4, 12) - 1, 2 * np.random.rand(1, 4) - 1 ]
    weights.insert(0, None)
    bias = [ 2 * np.random.rand(12, 1) - 1, 2 * np.random.rand(4, 1) - 1, 2 * np.random.rand(1, 1) - 1 ]
    bias.insert(0, None)
    
    lamda = 0.6
    previous_error = None
    
    for epoch in range(250):
        weights, bias, curr_error = train_function( training_input, expected_output, weights, bias, lamda, N )
        
        if previous_error is None:
            previous_error = curr_error
        else:
            lamda = lamda * (curr_error / previous_error)
            previous_error = curr_error

        misclassified = 0
        outputs = test_function( training_input, weights, bias, N )
        
        for index in range(len(outputs)):
            if outputs[index][0, 0] > 0.5:
                if expected_output[index][0, 0] == 0:
                    misclassified += 1
            else:
                if expected_output[index][0, 0] == 1:
                    misclassified += 1
        
        print(f"Epoch {epoch+1}: misclassified {misclassified} points.")        
        