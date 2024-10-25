from PIL import Image
from random import randint
import sys
imagefile="puppy.jpg"#sys.argv[1]
K=8#int(sys.argv[2])
def naive2(val):
    if(val<128):
        return 0
    else: 
        return 255
def naive3(val):
    if(val<255//3):
        return 0
    if(val>(255*2)//3):
        return 255
    else:
        return 127
def rep8Colors(pix):
    for x in range(w):
        for y in range(h):
            r,g,b=pix[x,y]
            r=naive2(r)
            g=naive2(g)
            b=naive2(b)
            pix[x,y]=(r,g,b)
def rep27Colors(pix):
    for x in range(w):
        for y in range(h):
            r,g,b=pix[x,y]
            r=naive3(r)
            g=naive3(g)
            b=naive3(b)
            pix[x,y]=(r,g,b)
def genCenters():
    centers=dict()
    count=0
    while count<K:
        x=randint(0,w-1)
        y=randint(0,h-1)
        if (x,y) not in centers:
            centers[(x,y)]=[(x,y)]
            count+=1
    return centers

def display(subgroups,pix):
    for newcolor in subgroups:
        replacement=(round(newcolor[0]),round(newcolor[1]),round(newcolor[2]))
        for oldcolor in subgroups[newcolor]:
            for cord in pixelColors[oldcolor]:
                pix[cord]=replacement

def find_groups(subgroups):
    pos=0
    for color in pixelColors:
        mindist=0
        keyvector=None
        for mean in subgroups:
            if keyvector==None:
                keyvector=mean
                mindist=dist(keyvector,color)
            else:
                testdist=dist(mean,color)
                if(testdist<mindist):
                    mindist=testdist
                    keyvector=mean
        subgroups[keyvector].append(color)
        # for cords in pixelColors[color]:
        #     if cords not in subgroups:
        #         subgroups[keyvector].append(cords)
        pos+=1

def check_stable(subgroups):
    stable=True
    nextsubgroups=dict()
    for key in subgroups:
        newcenter=average_group(subgroups[key])
        nextsubgroups[newcenter]=list()

        if newcenter!=key:
            stable=False
    return stable,nextsubgroups

def dist(v1,v2):
    return ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2)
def average_group(group):
    sumR=sumG=sumB=0
    count=0
    for color in group:
        pixColorCount=len(pixelColors[color])
        count+=pixColorCount
        sumR+=color[0]*pixColorCount
        sumG+=color[1]*pixColorCount
        sumB+=color[2]*pixColorCount
    return (sumR/count,sumG/count,sumB/count)

def kmeans(pix):
    subgroups=genCenters()
    # print(subgroups)
    pos=0
    for color in pixelColors:
        mindist=0
        keyvector=None
        for mean in subgroups:
            if keyvector==None:
                keyvector=mean
                mindist=dist(pix[keyvector],color)
            else:
                testdist=dist(pix[mean],color)
                if(testdist<mindist):
                    mindist=testdist
                    keyvector=mean
        
        for cords in pixelColors[color]:
            if cords not in subgroups:
                subgroups[keyvector].append(cords)
            #this dict has a rgb tuple point to the list of colors that is closest to it
        pos+=1
    # stable, nextsubgroups=check_stable(subgroups)
    stable=False
    nextsubgroups=dict()
    for key in subgroups:
        sumR=sumG=sumB=0
        count=0
        for val in subgroups[key]:

            count+=1
            sumR+=pix[val][0]
            sumG+=pix[val][1]
            sumB+=pix[val][2]
        newcenter= (sumR/count,sumG/count,sumB/count)

        # newcenter=average_group(subgroups[key])
        nextsubgroups[newcenter]=list()

    # print(nextsubgroups)
    while not stable:
        subgroups=nextsubgroups
        find_groups(subgroups)
        stable,nextsubgroups=check_stable(subgroups)
    display(subgroups,pix)
    # for mean in subgroups:
    #     print(mean)
    #     for val in subgroups[mean]:
    #         print(STARS[val][0], STARS[val][1])
    #     print("")

original = Image.open(imagefile)
img=original.copy()
w,h=img.size
pix=img.load()
# rep8Colors(pix)
# img.show()
# img.save("tiger8naive.png")
# img = original.copy()
# pix=img.load()
# rep27Colors(pix)
# img.show()
# img.save("tiger27naive.png")

# img=original.copy()
# pix=img.load()
pixelColors=dict()
for x in range(w):
    for y in range(h):
        if pix[x,y] in pixelColors:
            pixelColors[pix[x,y]].append((x,y))
        else:
            pixelColors[pix[x,y]]=[(x,y)]

#i made a dict with each color pointing to a list of the pixels w that color
kmeans(pix)
img.save("kmeansout.png")
img.show()
# img.show()
# img.save("tiger8means.png")
# img = original.copy()
# pix=img.load()

# K=27
# kmeans(pix)
# img.show()
# img.save("tiger27means.png")