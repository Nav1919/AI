from math import pi , acos , sin , cos
import sys
from time import perf_counter
from heapq import heappush, heappop, heapify

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
def dijkstra(start,goal,edges):
    closed=set()
    startNode=(0,start)
    fringe=[]
    heappush(fringe, startNode)
    while fringe:
        (dist, state)=heappop(fringe)
        if state==goal:
            return dist
        if state not in closed:
            closed.add(state)
            for edgedist, child in edges[state]:
                if child not in closed:
                    temp=(dist+edgedist,child)
                    heappush(fringe,temp)
    return None
def astar(start,goal,edges,nodes):
    closed=set()
    startNode=(calcd(nodes[start],nodes[goal]),0,start)
    fringe=[]
    heappush(fringe, startNode)
    while fringe:
        (_, dist, state)=heappop(fringe)
        if state==goal:
            return dist
        if state not in closed:
            closed.add(state)
            for edgedist, child in edges[state]:
                if child not in closed:
                    temp=(calcd(nodes[child], nodes[goal])+dist+edgedist,dist+edgedist,child)
                    heappush(fringe,temp)
    return None
start=perf_counter()
nodesFile="rrNodes.txt"
nodes=dict()
with open(nodesFile) as words_file:
    for line in words_file:
        vals=line.split(" ")
        nodes[vals[0]]=(float(vals[1]), float(vals[2]))
edgesFile="rrEdges.txt"
edges=dict()
with open(edgesFile) as words_file:
    for line in words_file:
        line=line[:-1]
        vals=line.split(" ")
        if(vals[0] not in edges):
            edges[vals[0]]=set()
        if(vals[1] not in edges):
            edges[vals[1]]=set()
        dist=calcd(nodes[vals[0]],nodes[vals[1]])
        edges[vals[0]].add((dist, vals[1]))
        edges[vals[1]].add((dist, vals[0]))
cityFile="rrNodeCity.txt"
cityToNode=dict()
with open(cityFile) as words_file:
    for line in words_file:
        vals=line.split(" ",1)
        cityToNode[vals[1].strip()]=vals[0]
print(f"Time to create data structure: {perf_counter()-start}")
city1=sys.argv[1]
city2=sys.argv[2]
start=perf_counter()
print(f"{city1} to {city2} with Dijkstra: {dijkstra(cityToNode[city1],cityToNode[city2],edges)} in {perf_counter()-start} seconds.")
start=perf_counter()
print(f"{city1} to {city2} with A*: {astar(cityToNode[city1],cityToNode[city2],edges, nodes)} in {perf_counter()-start} seconds.")