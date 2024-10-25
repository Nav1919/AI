from PIL import Image
from random import randint
import sys
from time import perf_counter
imagefile=sys.argv[1]
K=int(sys.argv[2])
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
#https://www.geeksforgeeks.org/ml-k-means-algorithm/#
def genCentersKMeansPlusPlus(pix):
    centers=dict()
    x=randint(0,w-1)
    y=randint(0,h-1)
    lastCenter=pix[x,y]
    centers[lastCenter]=[lastCenter]
    colorMinDist=dict()
    colorMinDist[lastCenter]=0

    count=1
    while count<K:
        maxColor=(0,0,0)
        maxDist=0
        for color in pixelColors:
            if color not in colorMinDist:
                colorMinDist[color]=dist(color,lastCenter)
            elif colorMinDist[color]!=0:
                colorMinDist[color]=min(colorMinDist[color],dist(color,lastCenter))
                    
            if colorMinDist[color]>maxDist:
                    maxDist=colorMinDist[color]
                    maxColor=color
        centers[maxColor]=[maxColor]
        lastCenter=maxColor
        count+=1
    return centers
def guaranteeRange(threshold):
    if threshold>255:
        return 255
    elif threshold<0:
        return 0
    else: return threshold
def roundRGB(color):
    r=(round(color[0]))
    g=(round(color[1]))
    b=(round(color[2]))
    return (r,g,b)
def find_closest_palette_color(oldpixel,colorspace):
    oldpixel=(guaranteeRange(oldpixel[0]),guaranteeRange(oldpixel[1]),guaranteeRange(oldpixel[2]))
    mindist=dist(oldpixel,colorspace[0])
    minpos=0
    for i in range(1,K):
        tempdist=dist(oldpixel,colorspace[i])
        if(tempdist<mindist):
            mindist=tempdist
            minpos=i
    return colorspace[minpos]
def addMultTuple(tup1, tup2, mult: float):
    return (tup1[0]+mult*tup2[0],tup1[1]+mult*tup2[1],tup1[2]+mult*tup2[2])
def dither(subgroups,pix):
    colorspace=list()
    for color in subgroups:
        colorspace.append(roundRGB(color))
    for y in range(h):
        for x in range(w):
            oldpixel=pix[x,y]
            newpixel=find_closest_palette_color(oldpixel,colorspace)
            pix[x,y]=newpixel
            quant_error=addMultTuple(oldpixel,newpixel,-1)
            if(quant_error!=(0,0,0)):
                a=1
            if x<w-1:
                pix[x+1,y]=roundRGB(addMultTuple(pix[x+1,y],quant_error,7/16))
            if y+1<h:
                if x>0: pix[x-1,y+1]=roundRGB(addMultTuple(pix[x-1,y+1],quant_error,3/16))
                pix[x,y+1]=roundRGB(addMultTuple(pix[x,y+1],quant_error,5/16))
                if x<w-1: pix[x+1,y+1]=roundRGB(addMultTuple(pix[x+1,y+1],quant_error,1/16))
    #From wiki: https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering        
    # for each y from top to bottom do
    #     for each x from left to right do
    #         oldpixel := pixels[x][y]
    #         newpixel := find_closest_palette_color(oldpixel)
    #         pixels[x][y] := newpixel
    #         quant_error := oldpixel - newpixel
    #         pixels[x + 1][y    ] := pixels[x + 1][y    ] + quant_error × 7 / 16
    #         pixels[x - 1][y + 1] := pixels[x - 1][y + 1] + quant_error × 3 / 16
    #         pixels[x    ][y + 1] := pixels[x    ][y + 1] + quant_error × 5 / 16
    #         pixels[x + 1][y + 1] := pixels[x + 1][y + 1] + quant_error × 1 / 16

def kmeans(pix,ditherbool):
    start=perf_counter()
    subgroups=genCentersKMeansPlusPlus(pix)
    find_groups(subgroups)
    stable,nextsubgroups=check_stable(subgroups)
    while not stable:
        subgroups=nextsubgroups
        find_groups(subgroups)
        stable,nextsubgroups=check_stable(subgroups)
    if ditherbool: dither(subgroups,pix)
    else: display(subgroups,pix)
    print(perf_counter()-start)
    boxsize=w/K
    output=Image.new("RGB",(w,maxh:=(h+round(boxsize))),0)
    pixout=output.load()
    for x in range(w):
        for y in range(h):
            pixout[x,y]=pix[x,y]
    x=0
    right=1
    for color in subgroups.keys():
        color=(round(color[0]),round(color[1]),round(color[2]))
        while x<=round(boxsize*right) and x<w:
            for y in range(h,maxh):
                pixout[x,y]=color
            x+=1
        right+=1
    return output
original = Image.open(imagefile)
img=original.copy()
w,h=img.size
pix=img.load()

pixelColors=dict()
for x in range(w):
    for y in range(h):
        if pix[x,y] in pixelColors:
            pixelColors[pix[x,y]].append((x,y))
        else:
            pixelColors[pix[x,y]]=[(x,y)]

output=kmeans(pix,True)
output.save("kmeansout.png")
output.show()
