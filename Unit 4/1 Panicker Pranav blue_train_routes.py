from math import pi , acos , sin , cos
import sys
from time import perf_counter
from time import sleep
from heapq import heappush, heappop, heapify
import tkinter as tk

def calcd(node1, node2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   y1, x1 = node1
   y2, x2 = node2

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R
def getLine(edgeToLine, node1, node2):
    if((node1, node2) in edgeToLine):
        return edgeToLine[(node1,node2)]
    else:
        return edgeToLine[(node2, node1)]
def resetGraph(r,c,edgeToLine):
    for line in edgeToLine.values():
        c.itemconfig(line, fill="black",width=1)
    r.update()
def dijkstra(start,goal,edges,r,c,edgeToLine):
    closed=set()
    startNode=(0,start)
    fringe=[]
    heappush(fringe, startNode)
    prev=dict()
    minDist=0
    total=0
    while fringe:
        (dist, state)=heappop(fringe)
        if state==goal:
            minDist=dist
            break
        if state not in closed:
            closed.add(state)
            for edgedist, child in edges[state]:
                if child not in closed:
                    if child not in prev:
                        prev[child]=(state,dist+edgedist)
                    else:
                        other=prev[child]
                        if(other[1]>dist+edgedist):
                            prev[child]=(state,dist+edgedist)
                    c.itemconfig(getLine(edgeToLine, state, child), fill="red")
                    
                    total+=1
                    temp=(dist+edgedist,child)
                    heappush(fringe,temp)
                    if(total%1000==0):
                        r.update()
    node2=goal
    while(node2!=start):
        node1=prev[node2][0]
        c.itemconfig(getLine(edgeToLine, node1, node2), fill="green",width=2)
        r.update()
        node2=node1
    sleep(3)  
    return minDist

def astar(start,goal,edges,nodes,r,c,edgeToLine):
    closed=set()
    startNode=(calcd(nodes[start],nodes[goal]),0,start)
    fringe=[]
    heappush(fringe, startNode)
    prev=dict()
    minDist=0
    total=0
    while fringe:
        (_, dist, state)=heappop(fringe)
        if state==goal:
            minDist=dist
            break
        if state not in closed:
            closed.add(state)
            for edgedist, child in edges[state]:
                if child not in closed:
                    if child not in prev:
                        prev[child]=(state,dist+edgedist)
                    else:
                        other=prev[child]
                        if(other[1]>dist+edgedist):
                            prev[child]=(state,dist+edgedist)
                    c.itemconfig(getLine(edgeToLine, state, child), fill="blue")
                    total+=1
                    if(total%1000==0):
                        r.update()
                    temp=(calcd(nodes[child], nodes[goal])+dist+edgedist,dist+edgedist,child)
                    heappush(fringe,temp)
            
    node2=goal
    while(node2!=start):
        node1=prev[node2][0]
        c.itemconfig(getLine(edgeToLine, node1, node2), fill="green",width=2)
        r.update()
        node2=node1
    sleep(3)
    return minDist
start=perf_counter()
nodesFile="rrNodes.txt"
nodes=dict()
minLat=float('inf')
maxLat=float('-inf')
minLong=float('inf')
maxLong=float('-inf')
with open(nodesFile) as words_file:
    for line in words_file:
        vals=line.split(" ")
        lat=float(vals[1])
        long=float(vals[2])
        if(lat<minLat):
            minLat=lat
        if(lat>maxLat):
            maxLat=lat
        if(long<minLong):
            minLong=long
        if(long>maxLong):
            maxLong=long
        nodes[vals[0]]=(lat, long)
latRange=maxLat-minLat
longRange=maxLong-minLong
latShift=(50-latRange)/2
longShift=(75-longRange)/2
edgesFile="rrEdges.txt"
edges=dict()
edgeToLine=dict()
root = tk.Tk() #creates the frame
canvas = tk.Canvas(root, height=600, width=800, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
canvas.pack(expand=True)
with open(edgesFile) as words_file:
    for line in words_file:
        line=line[:-1]
        vals=line.split(" ")
        if(vals[0] not in edges):
            edges[vals[0]]=set()
        if(vals[1] not in edges):
            edges[vals[1]]=set()
        dist=calcd(nodes[vals[0]],nodes[vals[1]])
        (lat1, long1)=nodes[vals[0]]
        (lat2, long2)=nodes[vals[1]]
        y1=500-10*(lat1-minLat+latShift)+50
        y2=500-10*(lat2-minLat+latShift)+50
        x1=10*(long1-minLong+longShift)+25
        x2=10*(long2-minLong+longShift)+25

        #print(x1,y1,x2,y2)
        line=canvas.create_line([(x1,y1),(x2,y2)],tags="edge")
        #root.update()
        edgeToLine[(vals[0],vals[1])]=line
        edges[vals[0]].add((dist, vals[1]))
        edges[vals[1]].add((dist, vals[0]))

root.update()

cityFile="rrNodeCity.txt"
cityToNode=dict()
with open(cityFile) as words_file: 
    for line in words_file:
        vals=line.split(" ",1)
        cityToNode[vals[1].strip()]=vals[0]
print(f"Time to create data structure: {perf_counter()-start}")

# city1="Ciudad Juarez"
# city2="Montreal"
city1=sys.argv[1]
city2=sys.argv[2]

start=perf_counter()
print(f"{city1} to {city2} with Dijkstra: {dijkstra(cityToNode[city1],cityToNode[city2],edges,root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")
resetGraph(root, canvas, edgeToLine)
start=perf_counter()
print(f"{city1} to {city2} with A*: {astar(cityToNode[city1],cityToNode[city2],edges, nodes,root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")
root.mainloop()