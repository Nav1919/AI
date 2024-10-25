from math import pi , acos , sin , cos
import sys
from time import perf_counter
from heapq import heappush, heappop
import tkinter as tk
from collections import deque

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
    elif((node2,node1) in edgeToLine):
        return edgeToLine[(node2, node1)]
    else:
        return -1
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
                    c.itemconfig(getLine(edgeToLine, state, child), fill="red")
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
    return minDist

def dfs(start,goal,edges,r,c,edgeToLine):
    fringe=deque()
    visited=set()
    fringe.append((start,0))
    visited.add(start)
    prev=dict()
    count=0
    while fringe:
        state=fringe.pop()
        visited.add(state[0])
        if(state[0]==goal):
            break
        for edgedist, child in edges[state[0]]:
            if child not in visited:
                fringe.append((child,state[1]+edgedist))
                count+=1
                c.itemconfig(getLine(edgeToLine, state[0], child), fill="red")
                prev[child]=state[0]
                if(count%10==0):
                    r.update()
    r.update()
    node1=goal
    while node1!=start:
        node2=prev[node1]
        c.itemconfig(getLine(edgeToLine, node1, node2), fill="green", width=2)
        r.update()
        node1=node2
    r.update()
    return state[1]

def kdfs(k, start, goal, edges, r,c,edgeToLine):
    count = 0
    fringe = []
    visited = {start: (0, [start])}
    path = dict()
    heappush(fringe, (0, start, [start]))
    while len(fringe) > 0:
        v_depth, v_node, v_path = heappop(fringe)
        if v_node == goal:
            temp = goal
            while (temp != start):
                c.itemconfig(getLine(edgeToLine, temp, path[temp]), fill="green", width=2)
                temp = path[temp]
                r.update()

            return v_depth
        if v_depth < k:
            for i in edges[v_node]:
                newdepth = v_depth + i[0]
                if i[1] not in visited.keys():
                    if i[1] not in path.values():
                        path[i[1]] = v_node
                    heappush(fringe, (newdepth, i[1], v_path + [i[1]]))
                    visited[i[1]] = (newdepth, v_path + [i[1]])
                    count += 1
                    c.itemconfig(getLine(edgeToLine, i[1], v_node), fill="red")
                    if(count%1000==0):
                        r.update()
    return None

def iddfs(start, goal, edges,nodes, r,c,edgeToLine):
    ipp_value = calcd(nodes[start], nodes[goal]) #this would be maximum depth
    k = ipp_value//8
    result = None
    first=True
    while result == None:
        if not first:
            resetGraph(r,c,edgeToLine)
        result = kdfs(k, start, goal, edges, r,c,edgeToLine)
        k += ipp_value
        r.update()
        first=False
        
    r.update()
    return result
def bidijkstra(start,goal,edges,r,c,edgeToLine):
    startNode=(0,start)
    goalNode=(0,goal)
    qf=[]
    qb=[]
    heappush(qf, startNode)
    heappush(qb, goalNode)
    prev=dict()
    next=dict()
    df=dict()
    db=dict()
    df[start]=0
    db[goal]=0
    sf=set()
    sb=set()
    mu=float('inf')
    leftEnd=""
    rightEnd=""
    updateCount=0
    while qf and qb:
        (du, u)=heappop(qf)
        (dv, v)=heappop(qb)
        sf.add(u)
        sb.add(v)
        
        for dist, x in edges[u]:
            if x not in prev:
                prev[x]=(u,dist+du)
            else:
                curr=prev[x]
                if(dist+du<curr[1]):
                    prev[x]=(u,dist+du)
            if x not in sf and (x not in df or df[x]>df[u]+dist):
                df[x]=du+dist
                heappush(qf,(df[x],x))
                c.itemconfig(getLine(edgeToLine, x, u), fill="red")
                updateCount+=1
                if(updateCount%1500==0):
                    r.update()
            if x in sb and u in df and x in db and df[u]+dist+db[x]<mu:
                mu=df[u]+dist+db[x]
                leftEnd=u
                rightEnd=x
        for dist, x in edges[v]:
            if x not in next:
                next[x]=(v,dist+dv)
            else:
                curr=next[x]
                if(dist+dv<curr[1]):
                    next[x]=(v,dist+dv)
            if x not in sb and (x not in db or db[x]>db[v]+dist):
                db[x]=dv+dist
                heappush(qb,(db[x],x))
                c.itemconfig(getLine(edgeToLine, x, v), fill="red")
                updateCount+=1
                if(updateCount%1500==0):
                    r.update()
            if x in sf and v in db and x in df and db[v]+dist+df[x]<mu:
                mu=db[v]+dist+df[x]
                leftEnd=x
                rightEnd=v
        if(df[u]+db[v]>=mu):
            break
    node2=rightEnd
    while(node2!=goal):        
        node1=next[node2][0]
        c.itemconfig(getLine(edgeToLine, node1, node2), fill="green",width=2)
        r.update()
        node2=node1
    node2=leftEnd
    c.itemconfig(getLine(edgeToLine, leftEnd, rightEnd), fill="green",width=2)
    while(node2!=start):
        node1=prev[node2][0]
        c.itemconfig(getLine(edgeToLine, node1, node2), fill="green",width=2)        
        r.update()
        node2=node1
    return mu

def reverseastar(start,goal,edges,nodes,r,c,edgeToLine):
    closed=set()
    startNode=(-calcd(nodes[start],nodes[goal]),0,start)
    fringe=[]
    heappush(fringe, startNode)
    prev=dict()
    maxDist=0
    count=0
    while fringe:
        (_, dist, state)=heappop(fringe)
        if state==goal:
            maxDist=dist
            break
        if state not in closed:
            closed.add(state)
            for edgedist, child in edges[state]:
                if child not in closed:
                    prev[child]=state
                    c.itemconfig(getLine(edgeToLine, state, child), fill="red")
                    count+=1
                    temp=(-(calcd(nodes[child], nodes[goal])+dist+edgedist),dist+edgedist,child)
                    heappush(fringe,temp)
                    if count%1500==0:
                        r.update()
    node2=goal
    while(node2!=start):
        node1=prev[node2]
        c.itemconfig(getLine(edgeToLine, node1, node2), fill="green", width=2)
        r.update()
        node2=node1
    return maxDist

def biastar(start,goal,edges,nodes,r,c,edgeToLine):
    sep=calcd(nodes[start],nodes[goal])
    startNode=(sep,0,start)
    goalNode=(sep,0,goal)
    qf=[]
    qb=[]
    heappush(qf, startNode)
    heappush(qb, goalNode)
    prev=dict()
    next=dict()
    df=dict()
    db=dict()
    df[start]=0
    db[goal]=0
    sf=set()
    sb=set()
    mu=float('inf')
    leftEnd=""
    rightEnd=""
    updateCount=0
    while qf and qb:
        (_, du, u)=heappop(qf)
        (_, dv, v)=heappop(qb)
        sf.add(u)
        sb.add(v)
        
        for dist, x in edges[u]:
            if x not in sf and (x not in df or df[x]>df[u]+dist):
                df[x]=du+dist
                heappush(qf,(df[x]+calcd(nodes[x],nodes[goal]),df[x],x))
                prev[x]=u
                c.itemconfig(getLine(edgeToLine, x, u), fill="red")
                updateCount+=1
                if(updateCount%1000==0):
                    r.update()
            if x in sb and u in df and x in db and df[u]+dist+db[x]<mu:
                mu=df[u]+dist+db[x]
                leftEnd=u
                rightEnd=x
        for dist, x in edges[v]:
            if x not in sb and (x not in db or db[x]>db[v]+dist):
                db[x]=dv+dist
                heappush(qb,(db[x]+calcd(nodes[x],nodes[start]),db[x],x))
                next[x]=v
                c.itemconfig(getLine(edgeToLine, x, v), fill="red")
                updateCount+=1
                if(updateCount%1000==0):
                    r.update()
            if x in sf and v in db and x in df and db[v]+dist+df[x]<mu:
                mu=db[v]+dist+df[x]
                leftEnd=x
                rightEnd=v
        if(df[u]+db[v]>=mu+30):
            break
    node2=rightEnd
    while(node2!=goal):
        node1=next[node2]
        c.itemconfig(getLine(edgeToLine, node1, node2), fill="green",width=2)
        r.update()
        node2=node1
    node2=leftEnd
    c.itemconfig(getLine(edgeToLine, leftEnd, rightEnd), fill="green",width=2)
    while(node2!=start):
        node1=prev[node2]
        c.itemconfig(getLine(edgeToLine, node1, node2), fill="green",width=2)
        r.update()
        node2=node1
    return mu

start=perf_counter()
nodesFile="Unit 4/rrNodes.txt"
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
edgesFile="Unit 4/rrEdges.txt"
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

        line=canvas.create_line([(x1,y1),(x2,y2)],tags="edge")

        edgeToLine[(vals[0],vals[1])]=line
        edges[vals[0]].add((dist, vals[1]))
        edges[vals[1]].add((dist, vals[0]))
root.update()

cityFile="Unit 4/rrNodeCity.txt"
cityToNode=dict()
with open(cityFile) as words_file: 
    for line in words_file:
        vals=line.split(" ",1)
        cityToNode[vals[1].strip()]=vals[0]
print(f"Time to create data structure: {perf_counter()-start}")
city1=sys.argv[1]
city2=sys.argv[2]
option=""
while(option!="-1"):
    print("Which algorithm? (Type in number of desired algorithm or -1 to exit)")
    option=input("1. Dijkstra, 2. A*, 3. DFS, 4. ID-DFS, 5. Bidirectional dijkstra, 6. Reverse A*, 7. Bidirectional A*\n")
    if(option=="-1"):
        break
    resetGraph(root,canvas,edgeToLine)
    start=perf_counter()
    if(option=="1"):
        print(f"{city1} to {city2} with Dijkstra: {dijkstra(cityToNode[city1],cityToNode[city2],edges,root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")
    elif(option=="2"):
        print(f"{city1} to {city2} with A*: {astar(cityToNode[city1],cityToNode[city2],edges, nodes,root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")
    elif(option=="3"):
        print(f"{city1} to {city2} with DFS: {dfs(cityToNode[city1],cityToNode[city2],edges, root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")
    elif(option=="4"):
        print(f"{city1} to {city2} with ID-DFS: {iddfs(cityToNode[city1],cityToNode[city2],edges,nodes,root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")
    elif(option=="5"):
        print(f"{city1} to {city2} with Bidirectional Dijkstra: {bidijkstra(cityToNode[city1],cityToNode[city2],edges, root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")

    elif(option=="6"):
        print(f"{city1} to {city2} with Reverse A*: {reverseastar(cityToNode[city1],cityToNode[city2],edges,nodes,root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")
    elif(option=="7"):
        print(f"{city1} to {city2} with Bidirectional A*: {biastar(cityToNode[city1],cityToNode[city2],edges, nodes,root,canvas,edgeToLine)} in {perf_counter()-start} seconds.")
    else:
        print("Invalid input")
    print("")
    