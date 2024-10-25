from colorama import init, Back, Fore
import re
import sys
init()
exparg=sys.argv[1].split("/")

flags=list()
if('i' in exparg[2]):
    flags.append(re.I)
if('m' in exparg[2]):
    flags.append(re.M)
if('s' in exparg[2]):
    flags.append(re.S)

if(len(flags)==3):
    exp=re.compile(rf"{exparg[1]}", flags[0] | flags[1] | flags[2])
if(len(flags)==2):
    exp=re.compile(rf"{exparg[1]}", flags[0] | flags[1])
if(len(flags)==1):
    exp=re.compile(rf"{exparg[1]}", flags[0])
if(len(flags)==0):
    exp=re.compile(rf"{exparg[1]}")

s="While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?"
prevEnd=0
ret=""
prevFlipped=False
for result in exp.finditer(s):

    indices=result.span()
    if(prevEnd!=indices[0]):
        ret+=s[prevEnd:indices[0]]
        ret+=(Back.LIGHTYELLOW_EX+s[indices[0]:indices[1]]+Back.RESET)
        prevFlipped=False
    elif not prevFlipped:
        ret+=(Back.LIGHTCYAN_EX+s[indices[0]:indices[1]]+Back.RESET)
        prevFlipped=True
    else:
        ret+=(Back.LIGHTYELLOW_EX+s[indices[0]:indices[1]]+Back.RESET)
        prevFlipped=False
    
    prevEnd=indices[1]
ret+=(Back.RESET+s[prevEnd:])
print(ret)
