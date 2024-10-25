import sys
import numpy as np

input=sys.argv[1]
point=np.array([[0], [0]])
min=pow(10,-8)
learning_rate=0.1
if input=='A':
    while True:
        x=float(point[0][0])
        y=float(point[1][0])
        
        partialx=8*x-3*y+24
        partialy=4*(y-5)-3*x
        print(f"Location: ({x}, {y}); Gradient: <{partialx}, {partialy}>")
        gradient=np.array([[partialx],[partialy]])
        mag=np.sum(np.square(gradient)) ** 0.5
        if mag<min:
            break
        point=np.array([[x-learning_rate*partialx],[y-learning_rate*partialy]])

elif input=='B':
    while True:
        x=float(point[0][0])
        y=float(point[1][0])
        
        partialx=2*(x-pow(y,2))
        partialy=2*(-2*x*y+2*pow(y,3)+y-1)
        print(f"Location: ({x}, {y}); Gradient: <{partialx}, {partialy}>")
        gradient=np.array([[partialx],[partialy]])
        mag=np.sum(np.square(gradient)) ** 0.5
        if mag<min:
            break
        point=np.array([[x-learning_rate*partialx],[y-learning_rate*partialy]])
