import sys
from time import perf_counter
from time import sleep
from heapq import heappush, heappop, heapify
import tkinter as tk
from math import pi , acos , sin , cos

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

def resetter(root, canvas, connector):
    for x in connector.values():
        canvas.itemconfig(line, fill="black")
    root.update()

def Astar(start, finish, canvas, dictionary_tag_to_coordinates, root, continous, connectors):
    closed = set()
    starter = (calcd(dictionary_tag_to_coordinates[start], dictionary_tag_to_coordinates[goal]), 0, start)
    fringe = list()
    heapify(fringe)
    heappush(fringe, starter)
    backchildren = {}
    counter = 0
    temptravel = 0
    while len(fringe) > 0:
        v = heappop(fringe)
        print(v)
        if v[2] == goal:
            temptravel = v[1]
            break
        if v[2] not in closed:
            closed.add(v[2])
            for x, a in continous[v[2]]:
                if a not in closed:
                    if a not in backchildren:
                        # print(backchildren, v, "hi")
                        backchildren[a] = (v[2], v[1] + x)
                    else:
                        temp = backchildren[a]
                        if(temp[1] > v[1] + a):
                            backchildren[a] = (v[2], v[1] + x)
                    if(v[1], a) in connectors:
                        canvas.itemconfig(connectors[(v[2], a)], fill="yellow")
                    else:
                        canvas.itemconfig(connectors[a, v[2]], fill ="yellow")
                    counter+=1
                    heappush(fringe, (v[1] + x, a))
                    if(counter%1000 == 0):
                        root.update()
                    adding = (calcd(dictionary_tag_to_coordinates[a], dictionary_tag_to_coordinates[goal]) + v[2] + x, v[2] + x, a)
                    print(adding, "/",adding[2])
                    heappush(fringe, adding)
    temper = finish  
    while(temper!=start):
        temp = backchildren[temper][0]
        if(temp, temper) in connectors:
            canvas.itemconfig(connectors[(temp, temper)], fill="green")
        else:
            canvas.itemconfig(connectors[temper, temp], fill ="green")
        root.update()
        temper = temp
    return temptravel

def Dijkstra(start, finish, canvas, root, continous, connectors):
    global datastructure
    goal = finish
    closed = set()
    starter = (0, start)
    fringe = list()
    heapify(fringe)
    heappush(fringe, starter)
    backchildren = {}
    counter = 0
    temptravel = 0
    while len(fringe) > 0:
        v = heappop(fringe)
        if v[1] == goal:
            temptravel = v[0]
            break
        if v[1] not in closed:
            closed.add(v[1])
            for x, a in continous[v[1]]:
                if a not in closed:
                    if a not in backchildren:
                        backchildren[a] = [v[1], v[0] + x]
                    else:
                        temp = backchildren[a]
                        if(temp[1] > v[0] + a):
                            backchildren[a] = (v[1], v[0] + x)
                    if(v[1], a) in connectors:
                        canvas.itemconfig(connectors[(v[1], a)], fill="red", width = 1)
                    else:
                        canvas.itemconfig(connectors[a, v[1]], fill ="red", width = 1)
                    counter+=1
                    heappush(fringe, (v[0] + x, a))
                    if(counter%1000 == 0):
                        root.update()
    temper = finish
    while(temper!=start):
        temp = backchildren[temper][0]
        if(temp, temper) in connectors:
            canvas.itemconfig(connectors[(temp, temper)], fill="green", width = 3)
        else:
            canvas.itemconfig(connectors[temper, temp], fill ="green", width = 3)
        root.update()
        temper = temp
    return temptravel

start = perf_counter()
pathways = []
junctions = set()
with open("Unit 4/rrEdges.txt") as f:
    for line in f:
            x = line.strip()
            first, second = x.split(" ")
            junctions.add(int(first))
            junctions.add(int(second))
            pathways.append((int(second), int(first)))
            pathways.append((int(first), int(second)))
dictionary_tag_to_coordinate = {}
with open("Unit 4/rrNodes.txt") as f:
    for line in f:
            x = line.strip()
            temp = x.split(" ")
            dictionary_tag_to_coordinate[int(temp[0])] = (float(temp[1]), float(temp[2]))
dictionary_name_to_id = {}
with open("Unit 4/rrNodeCity.txt") as f:
    for line in f:
            x = line.strip()
            y = x.split(" ")
            name = ' '.join(y[1:len(y)])
            id = y[0]
            dictionary_name_to_id[name] = int(id)
datastructure = {}
for x in junctions:
    datastructure[int(x)] = set()
for x in pathways:
    starting = x[0]
    goal = x[1]
    datastructure[int(starting)].add((calcd(dictionary_tag_to_coordinate[int(starting)], dictionary_tag_to_coordinate[int(goal)]), goal))
end = perf_counter()
print("Time to create data structure in seconds: " + str(float(end) - float(start)))
root = tk.Tk() #creates the frame
canvas = tk.Canvas(root, height=800, width=1500, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
canvas.pack(expand=True)

dictionary = {}
continuous = {}
connectors = {}
for x in pathways:
    if(x[0] not in continuous):
        continuous[x[0]] = set()
    if(x[1] not in continuous):
        continuous[x[1]] = set()
    tup1 = dictionary_tag_to_coordinate[x[0]]
        #print(tup1)
    tup2 = dictionary_tag_to_coordinate[x[1]]
    distance = calcd(tup1, tup2)
        #horiz, verti = findmxmn(pathways)
    y1 = 800 - tup1[0]*12
    x1 = 1800 - tup1[1]*-1*12
    y2 = 800 - tup2[0]*12
    x2 = 1800 - tup2[1]*-1*12
        #print(id1y, id1x, id2y, id2x, "HI")
    line = canvas.create_line([(x1, y1), (x2, y2)], activewidth = 1)
    connectors[x[0], x[1]] = line
    continuous[x[0]].add((distance, x[1]))
    continuous[x[1]].add((distance, x[0]))

root.update()

# city1=sys.argv[1]
# city2=sys.argv[2]
city1="Miami"
city2="Leon"

start=perf_counter()
# print(f"{city1} to {city2} with Dijkstra: {Dijkstra(dictionary_name_to_id[city1],dictionary_name_to_id[city2],canvas,root, continuous, connectors)} in {perf_counter()-start} seconds.")
# resetter(root, canvas, connectors)
start=perf_counter()
print(f"{city1} to {city2} with A*: {Astar(dictionary_name_to_id[city1],dictionary_name_to_id[city2],canvas, dictionary_tag_to_coordinate, root,continuous,connectors)} in {perf_counter()-start} seconds.")
root.mainloop()