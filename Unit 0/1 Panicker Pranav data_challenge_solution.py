from time import perf_counter
from heapq import heappop, heappush, heapify
import sys
start = perf_counter()
#f1, f2, f3 = "10mfile1.txt", "10mfile2.txt", "10mfile3.txt"
f1, f2, f3 = sys.argv[1], sys.argv[2], sys.argv[3]
with open(f1) as r1, open(f2) as r2, open(f3) as r3:
  (fList1, fList2, fList3)=([int(line.strip()) for line in r1],[int(line.strip()) for line in r2],[int(line.strip()) for line in r3])
s3=set(fList3)
distinctValCount, sum100Unique = 0, 0
d1 = dict()
d2 =dict()
for val in fList2:
  if val not in d2:
    d2[val]=1
  else:
    d2[val]=d2.get(val)+1

for val in fList1:
  if val not in d1:
    d1[val]=1
    if val in d2:
      distinctValCount+=1
    if(len(d1)%100==0):
      sum100Unique+=val
  else:
    d1[val]=d1.get(val)+1
    


f3count=0
for val in s3:
  if val in d1:
    f3count=f3count+d1[val]
  if val in d2:
    f3count=f3count+d2[val]

h1=list(d1)
heapify(h1)
min10=list()
for i in range(10):
  min10.append(heappop(h1))

h2=[-1*i for i in d2]
heapify(h2)
max10occur2=list()
i=0
while i<10 and h2:
  val=-1*heappop(h2)
  if d2[val]>1:
    max10occur2.append(val)
    i=i+1

sumMinsBfrMult53=0
sumSet=set()
h3=list()
for val in fList1:   
  if val not in sumSet:
    heappush(h3, val)
  if val%53==0:
    next=heappop(h3)
    while next in sumSet:
      next=heappop(h3)  
    sumSet.add(next)
    sumMinsBfrMult53+=next

  

print("#1: %s" % distinctValCount)
print("#2: %s" % sum100Unique)
print("#3: %s" % f3count)
print("#4: %s" % min10)
print("#5: %s" % max10occur2)
print("#6: %s" % sumMinsBfrMult53)
end = perf_counter()
print("Total time:", end - start)