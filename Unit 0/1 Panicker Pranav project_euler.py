from time import perf_counter
start = perf_counter()
def is_prime(x):
    if x%2==0:
        return False
    for i in range(3, int(x**0.5)+1, 2):
        if x%i==0:
            return False
    return True
    
#Problem 1
print("#1:", (sum([i for i in range(3, 1000, 3)])+sum([j for j in range(5,1000,5) if j%3!=0])))

#Problem 2
fibEvenSum=0
prev=1
curr=2
while(curr<4000000):
    if curr%2==0:
        fibEvenSum+=curr
    curr+=prev
    prev=curr-prev

print("#2:", fibEvenSum)

#Problem 3
num=600851475143
divisor=3
while num>1:
    if(num%divisor==0):
        num=num/divisor
    else:
        divisor=divisor+2

print("#3:", int(divisor))

#Problem 4
maxPal=0
for i in range(999, 99, -1):


    for j in range(i, 99, -1):
        product=i*j
        if(product<=maxPal):
            break
        val=product
        reverse=0
        while(val>0):
            reverse=reverse*10+val%10
            val=val//10
        if(reverse==product):
            maxPal=product

print("#4", maxPal)

#Problem 5
def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b, a%b)

n=20 #works for any value n
product=n
for i in range(n-1, 0, -1):
    product=product*i/gcd(product, i)
        

print("#5:", int(product))

#Problem 6
print("#6:", int((100*101/2)**2-(100 * 101) *(100 + 101)/6))

#Problem 7
def nthPrime(n):
    if n==1:
        return 2
    count=1
    val=1
    while(count<n):
        val+=2
        if(is_prime(val)):
            count+=1
    return val

print("#7:", nthPrime(10001))

#Problem 8
num_string = "731671765313306249192251196744265747423553491949349698352031277450632623957831801698480186947885184385" +\
            "861560789112949495459501737958331952853208805511125406987471585238630507156932909632952274430435576689" +\
            "664895044524452316173185640309871112172238311362229893423380308135336276614282806444486645238749303589" +\
            "072962904915604407723907138105158593079608667017242712188399879790879227492190169972088809377665727333" +\
            "001053367881220235421809751254540594752243525849077116705560136048395864467063244157221553975369781797" +\
            "784617406495514929086256932197846862248283972241375657056057490261407972968652414535100474821663704844" +\
            "031998900088952434506585412275886668811642717147992444292823086346567481391912316282458617866458359124" +\
            "566529476545682848912883142607690042242190226710556263211111093705442175069416589604080719840385096245" +\
            "544436298123098787992724428490918884580156166097919133875499200524063689912560717606058861164671094050" +\
            "7754100225698315520005593572972571636269561882670428252483600823257530420752963450"

adj13products=[1 for i in range(1000-13+1)]
for i in range(1000-13):
    for j in num_string[i:i+13]:
        adj13products[i]*=int(j)
        if(int(j)==0):
            break

print("#8:", max(adj13products))

#Problem 9
prodTri=0
for a in range(1000//3, 2, -1):
    b=(500000-1000*a)//(1000-a) #Expression found by solving for b in terms of a when plugging in c=1000-(a+b) to a^2+b^2=c^2
    c=1000-a-b
    if(a<c and a*a+b*b==c*c):
        prodTri=a*b*c
        break

print("#9", prodTri)
#Problem 11
data = [[ 8,  2, 22, 97, 38, 15,  0, 40,  0, 75,  4,  5,  7, 78, 52, 12, 50, 77, 91,  8],
       [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48,  4, 56, 62,  0],
       [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30,  3, 49, 13, 36, 65],
       [52, 70, 95, 23,  4, 60, 11, 42, 69, 24, 68, 56,  1, 32, 56, 71, 37,  2, 36, 91],
       [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
       [24, 47, 32, 60, 99,  3, 45,  2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
       [32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
       [67, 26, 20, 68,  2, 62, 12, 20, 95, 63, 94, 39, 63,  8, 40, 91, 66, 49, 94, 21],
       [24, 55, 58,  5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
       [21, 36, 23,  9, 75,  0, 76, 44, 20, 45, 35, 14,  0, 61, 33, 97, 34, 31, 33, 95],
       [78, 17, 53, 28, 22, 75, 31, 67, 15, 94,  3, 80,  4, 62, 16, 14,  9, 53, 56, 92],
       [16, 39,  5, 42, 96, 35, 31, 47, 55, 58, 88, 24,  0, 17, 54, 24, 36, 29, 85, 57],
       [86, 56,  0, 48, 35, 71, 89,  7,  5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
       [19, 80, 81, 68,  5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77,  4, 89, 55, 40],
       [ 4, 52,  8, 83, 97, 35, 99, 16,  7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
       [88, 36, 68, 87, 57, 62, 20, 72,  3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
       [ 4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18,  8, 46, 29, 32, 40, 62, 76, 36],
       [20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74,  4, 36, 16],
       [20, 73, 35, 29, 78, 31, 90,  1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57,  5, 54],
       [ 1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52,  1, 89, 19, 67, 48]]

prodGrid=0
for i in range(20):
    for j in range(20):
        if(i<17):
            prodGrid=max(prodGrid,data[i][j]*data[i+1][j]*data[i+2][j]*data[i+3][j])
        if(j<17):
            prodGrid=max(prodGrid, data[i][j]*data[i][j+1]*data[i][j+2]*data[i][j+3])
        if(i<17 and j<17):
            prodGrid=max(prodGrid,data[i][j]*data[i+1][j+1]*data[i+2][j+2]*data[i+3][j+3])
        if(i>=3 and j<17):
            prodGrid=max(prodGrid,data[i][j]*data[i-1][j+1]*data[i-2][j+2]*data[i-3][j+3])

print("#11", prodGrid)

#Problem 14
finished={2:2}

longest=2
longestVal=2
for i in range(3, 1000000):
    pos=i
    steps=0
    while(pos>1):
        if(pos in finished):
            finished[i]=steps+finished[pos]
            break
        if pos%2==0:
            pos=pos/2
        else:
            pos=3*pos+1
        steps+=1
    if(finished[i]>longest):
        longest=finished[i]
        longestVal=i
print("#14:",longestVal)

#Problem 18
data = [[75],
       [95, 64],
       [17, 47, 82],
       [18, 35, 87, 10],
       [20,  4, 82, 47, 65],
       [19,  1, 23, 75,  3, 34],
       [88,  2, 77, 73,  7, 63, 67],
       [99, 65,  4, 28,  6, 16, 70, 92],
       [41, 41, 26, 56, 83, 40, 80, 70, 33],
       [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
       [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
       [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
       [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
       [63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
       [ 4, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23]]

for i in range(len(data)-2, -1, -1):
    for j in range(0, i+1):
        data[i][j]+=max(data[i+1][j], data[i+1][j+1])
print("#18:",data[0][0])

#Problem 28
count=0
increment=1
prevTerm=1
sum=1
while(prevTerm<1001*1001):
    if(count==4):
        count=0
        increment+=1
    prevTerm+=increment*2
    sum+=prevTerm
    count+=1

print("#28:", sum)

#Problem 29
print("#29:", len({a**b for a in range(2, 101) for b in range(2, 101)}))


end=perf_counter()
print("Total time:",end-start)