# !/usr/bin/python
import random
import pdb

# def rush_basic(capacity,key):
#     j = capacity
#     mapped = False
#     loc = False
#     while not mapped :
#         random.seed(key)
#         random.jumpahead(j)
#         if j == 0 :
#             mapped = True
#             loc = random.randint(0,j - 1)
#         z = random.randint(0,j - 1)
# 
#         if z >= 1 :
#             j = j - 1
#         else :
#             mapped = True
#             loc = (j - 1) + (z % 1)
#     return loc
# 
# capacity = 10
# 
# for i in range(0,20):
#     print rush_basic(capacity,i)


meight = []
night  = None

def do_n(meight):
    n = [0]
    for i in range(1,len(meight)):
        s = 0
        for j in range(0,i):
            s = s + meight[j]
        n.append(s)
    return n

def rush(n,m,key):
    j = len(m) - 1
    while True:
        random.seed(key)
        random.jumpahead(j)
        if j == 0:
            return random.randint(0,m[j] - 1)
        z = random.randint(0,n[j] + m[j] - 1)
        if z >= m[j]:
            j = j - 1
        else:
            #print "zz " + str(z) + " j " + str(j)
            return n[j] + (z % m[j])
## init

count = []
for i in range(0,10):
    meight.append(1)
    count.append(0)

#print meight
night = do_n(meight)

for key in range(0,1000):
    loc = rush(night,meight,key)
    count[loc] = count[loc] + 1
    #print "key " + str(key) + " loc " + str(loc)

print count
