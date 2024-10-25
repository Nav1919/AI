from math import log
from math import sqrt
from random import sample
from PIL import Image
STARS=list()
with open("star_data.csv") as f:
    first=True
    for line in f:
        if first:
            first=False
            continue
        else:
            a=line.strip().split(',')
            STARS.append(((log(float(a[0])),log(float(a[1])),log(float(a[2])),float(a[3])),int(a[4])))
def kmeans(k):
    centers=sample(range(0,len(STARS)),k)
    subgroups={STARS[center][0]:list() for center in centers}
    # print(subgroups)
    find_groups(subgroups)
    stable,nextsubgroups=check_stable(subgroups)
    # print(nextsubgroups)
    while not stable:
        subgroups=nextsubgroups
        find_groups(subgroups)
        stable,nextsubgroups=check_stable(subgroups)
    for mean in subgroups:
        print(mean)
        for val in subgroups[mean]:
            print(STARS[val][0], STARS[val][1])
        print("")



def find_groups(subgroups):
    pos=0
    for vector, _ in STARS:
        mindist=0
        keyvector=None
        for mean in subgroups:
            if keyvector==None:
                keyvector=mean
                mindist=dist(keyvector,vector)
            else:
                testdist=dist(mean,vector)
                if(testdist<mindist):
                    mindist=testdist
                    keyvector=mean
        subgroups[keyvector].append(pos)
        pos+=1

def check_stable(subgroups):
    stable=True
    nextsubgroups=dict()
    for key in subgroups:
        newcenter=average_group(subgroups[key],STARS)
        nextsubgroups[newcenter]=list()
        if newcenter!=key:
            stable=False
    return stable,nextsubgroups

def dist(v1,v2):
    return ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2+(v1[3]-v2[3])**2)
def average_group(group,STARS):
    sum1=sum2=sum3=sum4=0
    count=0
    for val in group:

        count+=1
        sum1+=STARS[val][0][0]
        sum2+=STARS[val][0][1]
        sum3+=STARS[val][0][2]
        sum4+=STARS[val][0][3]
    return (sum1/count,sum2/count,sum3/count,sum4/count)
kmeans(6)
