"""
An implementation of:
Improving Translation Quality by Discarding Most of the Phrasetable (Johnson, Martin, Foster, Kuhn 2007)

Usage: 
    -d debug symbols
"""
# Copyright (C) 2009 
# Author: Gabriel Synnaeve
# License: http://www.opensource.org/licenses/PythonSoftFoundation.php

import sys 

#f = open('/Volumes/BLACKDATA/apertium/phrase-table')
file = open('tiny.sample')
i = 0

count_s = {}
count_t = {}
count_st = {}

def count(line):
    table = line.strip().replace('#','').replace('[','').replace(']','')\
            .split('|||') # seems to be faster than with the RE '$\[\]'
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

map(count, file)

for k in count_s.iterkeys():
    tmp = 0
    for (s, v) in count_s.iteritems():
        if k in s and k != s:
            tmp += v
    count_s[k] += tmp

for k in count_t.iterkeys():
    tmp = 0
    for (t, v) in count_t.iteritems():
        if k in t and k != t:
            tmp += v
    count_t[k] += tmp

for (ks, kt) in count_st.iterkeys():
    tmp = 0
    for ((s, t), v) in count_st.iteritems():
        if ks in s and ks != s and kt in t and kt != t:
            tmp += v
    count_st[(ks, kt)] += tmp


if '-d' in sys.argv:
    print '============================'
    print count_s
    print '============================'
    print count_t
    print '============================'
    print count_st
