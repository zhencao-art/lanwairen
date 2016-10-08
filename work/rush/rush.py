# !/usr/bin/python
# -*- coding: utf-8 unicode -*

import random

cluster_map = [1,1,1,1,1,1,1]
n_map = [1,2,3,4,5,6,7]

def select(oid):
    j = len(cluster_map) - 1
    while True:
        random.seed(oid)
        random.jumpahead(j)
    
        if j==0:
            return random.randint(0,n_map[j]);

        #z = random.randint(0,n_map[j])
        z = random.random()

        print "oid=" + str(oid) + "jump=" + str(j) + "random=" + str(z)

        if z >= cluster_map[j]:
            j = j - 1
        else:
            return n_map[j-1] + (z % cluster_map[j])

result = []

for i in range(0,10):
    result.append(select(i))

tongji = {}

for i in range(0,len(result)):
    if tongji.has_key(result[i]):
        tongji[result[i]].append(i)
    else:
        tongji[result[i]] = [i]

for i in tongji:
    print "Bucket " + str(i) + " len " + str(len(tongji[i]))
