#!/opt/local/bin/python2.5
"""
An implementation of:
Improving Translation Quality by Discarding Most of the Phrasetable (Johnson, Martin, Foster, Kuhn 2007)

Usage: 
    -d debug symbols
"""
# Copyright (C) 2009 
# Author: Gabriel Synnaeve
# License: http://www.opensource.org/licenses/PythonSoftFoundation.php

import sys, getopt, math #, guppy
#h = guppy.hpy()

from fisher import FisherExactTest
fish = FisherExactTest()

i = 0

count_s = {}
count_t = {}
count_st = {}
debug = 0

def Usage():
    print "./pruning.py phrase-table [-d][-h][-o outputfile]"
    sys.exit(0)

try:
    optlist, list = getopt.getopt(sys.argv[1:],':doh')
except getopt.GetoptError:
    Usage()
    sys.exit(1)
for opt in optlist:
    print opt[0]
    if opt[0] == '-h':
        Usage()
    if opt[0] == '-d':
        debug = 1
    if opt[0] == '-o':
        outputname = list[0]

file = open(sys.argv[1])

def count(line):
    table = line.replace('#','').replace('[','').replace(']','')\
            .replace('?','').replace('!','').strip().split('|||') 
            # seems to be faster than with the RE '#\[\]?!'
    source = table[0]
    target = table[1]
    if source in count_s:
        count_s[source] +=  1
    else: 
        count_s[source] =  1
    if target in count_t:
        count_t[target] +=  1
    else:
        count_t[target] =  1
    st = (source, target)
    if st in count_st:
        count_st[st] +=  1
    else:
        count_st[st] =  1

#map(count, file)
N = 0
for line in file:
    count(line)
    N += 1

#sdic = {}
#tdic = {}

for k in count_s.iterkeys():
    tmp = 0
    for (s, v) in count_s.iteritems():
        if k in s and k != s:
            tmp += v
#            sdic[(k,s)] = True
    count_s[k] += tmp

for k in count_t.iterkeys():
    tmp = 0
    for (t, v) in count_t.iteritems():
        if k in t and k != t:
            tmp += v
#            tdic[(k,t)] = True
    count_t[k] += tmp


for (ks, kt) in count_st.iterkeys():
    tmp = 0
    for ((s, t), v) in count_st.iteritems():
        if ks in s and ks != s and kt in t and kt != t:
#        if (ks,s) in sdic and (kt,t) in tdic:
            tmp += v
    count_st[(ks, kt)] += tmp

if debug:
    #print h.heap()
    print '===========count_s============='
    print count_s
    print '===========count_t============='
    print count_t
    print '===========count_st============='
    print count_st
    print '============================'

delete = []
threshold = math.log(N) - 0.01
print threshold
for k in count_st.iterkeys():
    try:
        if -math.log( fish.pvalue(count_st[k], count_s[k[0]], \
                count_t[k[1]], N) [2] ) > threshold:
            delete.append(k)
    except OverflowError:
        # The value is so low that even your mother can't ... oh sh** 
        # Discard this entry
        delete.append(k)

print file[3]

print delete
