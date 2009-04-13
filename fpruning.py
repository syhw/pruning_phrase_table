#!/opt/local/bin/python2.5
"""
An implementation of:
Improving Translation Quality by Discarding Most of the Phrasetable (Johnson, Martin, Foster, Kuhn 2007)

Usage: 
    -d debug symbols
"""
# Copyright (C) 2009 
# Authors: Gabriel Synnaeve & Nicolas Dumazet
# License: http://www.opensource.org/licenses/PythonSoftFoundation.php

import sys
#import guppy
#h = guppy.hpy()

#f = open('/Volumes/BLACKDATA/apertium/phrase-table')
file = open('test.sample')
i = 0

count_s = {}
count_t = {}

dict_st = {}

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

    if source in dict_st:
        d = dict_st[source]
        if target in d:
            d[target] += 1
        else:
            d[target] = 1
    else:
        dict_st[source] = {target:1}

map(count, file)

included_in_s = {}
included_in_t = {}
sets = {}

for k in count_s.iterkeys():
    tmp = 0
    dico = {}
    for (s, v) in count_s.iteritems():
        if k in s and k != s:
            tmp += v
            dico[s] = True
            if not s in sets:
                sets[s] = set(dict_st[s].keys())
    included_in_s[k] = dico
    count_s[k] += tmp

for k in count_t.iterkeys():
    tmp = 0
    dico = {}
    for (t, v) in count_t.iteritems():
        if k in t and k != t:
            tmp += v
            dico[t] = True
    included_in_t[k] = dico
    count_t[k] += tmp

for ks, kdic in dict_st.iteritems():
    ks_lesser_than = included_in_s[ks]
    for kt in kdic.iterkeys():
        # kt is in every element of kt_lesser_than
        kt_lesser_than = included_in_t[kt]
        kt_lesser_than = set(kt_lesser_than.keys())
        for s in ks_lesser_than.iterkeys():
            # we know that 'ks in s'
            intersect = kt_lesser_than & sets[s]
            tmp = 0
            for e in intersect:
                tmp += dict_st[s][e]
            kdic[kt] += tmp

if '-d' in sys.argv:
    print '============================'
    print count_s
    print '============================'
    print count_t
    print '============================'
    print dict_st
