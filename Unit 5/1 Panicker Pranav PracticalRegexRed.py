import re
import sys
# filename=sys.argv[1]
filename="Unit 5\wordlist.txt"
myRegexLst = [
  r"(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)\w+", #1
  r"(?!(\w*[aeiou]){6,})(?=(\w*[aeiou]){5})\w+", #2
  r"(\w)(?!\w*\1\w*.$)\w*\1", #3
  r"(\w)(\w)(\w)\w*(?<=\3\2\1)", #4
  r"[ac-su-z]*(bt|tb)[ac-su-z]*", #5
  r"\w*(\w)\1{1}\w*", #6
  r"\w*(\w)(\w*\1){1}\w*", #7
  r"\w*(\w\w)(\w*\1){1}\w*", #8
  r"([aeiou]*[b-df-hj-np-tv-z]){1,}[aeiou]*", #9
  r"(?!\w*(\w)(\w*\1){2})\w*" #10
  ]
with open(filename) as words_file:
    words_list=[line.strip() for line in words_file]
matches=list()
regexes=list()
for i in range(10):
    matches.append(list())
for word in words_list:
    for i in range(10):
        curr=re.fullmatch(myRegexLst[i],word,re.I)
        if curr!=None:
            matches[i].append(curr.group(0))
final1=list()
minlength=0
for val in matches[0]:
    if minlength==0:
        minlength=len(val)
    if len(val)==minlength:
        final1.append(val)
    elif len(val)<minlength:
        final1.clear()
        final1.append(val)
        minlength=len(val)
matches[0]=final1
final2=list()
maxlength=0
for val in matches[1]:
    if maxlength==0:
        maxlength=len(val)
    if len(val)==maxlength:
        final2.append(val)
    elif len(val)>maxlength:
        final2.clear()
        final2.append(val)
        maxlength=len(val)
matches[1]=final2
final3=list()
maxlength=0
for val in matches[2]:
    if maxlength==0:
        maxlength=len(val)
    if len(val)==maxlength:
        final3.append(val)
    elif len(val)>maxlength:
        final3.clear()
        final3.append(val)
        maxlength=len(val)
matches[2]=final3

currList=words_list
nextList=matches[5]
currRegex=r"\w*(\w)\1{0}\w*"
nextRegex=r"\w*(\w)\1{1}\w*"
n=1
while nextList:
    currList=nextList.copy()
    currRegex=nextRegex
    nextList.clear()
    n+=1
    nextRegex=r"\w*(\w)\1{"+f"{n}"+r"}\w*"
    for val in currList:
        curr=re.fullmatch(nextRegex,val,re.I)
        if curr!=None:
            nextList.append(curr.group(0))
myRegexLst[5]=currRegex
matches[5]=currList

currList=words_list
nextList=matches[6]
currRegex=r"\w*(\w)(\w*\1){0}\w*"
nextRegex=r"\w*(\w)(\w*\1){1}\w*"
n=1
while nextList:
    currList=nextList.copy()
    currRegex=nextRegex
    nextList.clear()
    n+=1
    nextRegex=r"\w*(\w)(\w*\1){"+f"{n}"+r"}\w*"
    for val in currList:
        curr=re.fullmatch(nextRegex,val,re.I)
        if curr!=None:
            nextList.append(curr.group(0))
myRegexLst[6]=currRegex
matches[6]=currList

currList=words_list
nextList=matches[7]
currRegex=r"\w*(\w\w)(\w*\1){0}\w*"
nextRegex=r"\w*(\w\w)(\w*\1){1}\w*"
n=1
while nextList:
    currList=nextList.copy()
    currRegex=nextRegex
    nextList.clear()
    n+=1
    nextRegex=r"\w*(\w\w)(\w*\1){"+f"{n}"+r"}\w*"
    
    for val in currList:
        curr=re.fullmatch(nextRegex,val,re.I)
        if curr!=None:
            nextList.append(curr.group(0))
myRegexLst[7]=currRegex
matches[7]=currList

currList=words_list
nextList=matches[8]
currRegex=r"([aeiou]*[b-df-hj-np-tv-z]){0}[aeiou]*"
nextRegex=r"([aeiou]*[b-df-hj-np-tv-z]){1,}[aeiou]*"
n=1
while nextList:
    currList=nextList.copy()
    currRegex=nextRegex
    nextList.clear()
    n+=1
    nextRegex=r"([aeiou]*[b-df-hj-np-tv-z]){"+f"{n}"+r",}[aeiou]*"
    
    for val in currList:
        curr=re.fullmatch(nextRegex,val,re.I)
        if curr!=None:
            nextList.append(curr.group(0))
myRegexLst[8]=currRegex
matches[8]=currList

final10=list()
maxlength=0
for val in matches[9]:
    if maxlength==0:
        maxlength=len(val)
    if len(val)==maxlength:
        final10.append(val)
    elif len(val)>maxlength:
        final10.clear()
        final10.append(val)
        maxlength=len(val)
matches[9]=final10

for i in range(10):
    print(f"#{i+1}: /^{myRegexLst[i]}$/i")
    print(f"{len(matches[i])} total matches")
    min=5
    if(len(matches[i])<5):
        min=len(matches[i])
    for j in range(min):
        print(matches[i][j])
    print("")
# for val in matches[9]:
#     print(val)