#!/opt/local/bin/python2.5
"""
An implementation of:
Improving Translation Quality by Discarding Most of the Phrasetable (Johnson, Martin, Foster, Kuhn 2007)

Usage: 
    -d debug symbols
    -i input file
    -o ouput file
"""
# Copyright (C) 2009 
# Authors: Gabriel Synnaeve (& Nicolas Dumazet)
# License: http://www.opensource.org/licenses/PythonSoftFoundation.php

import sys, getopt, math #, guppy
#h = guppy.hpy()

import enrichment 

def Usage():
    print "./pruning.py phrase-table [-d][-h][-o outputfile]"
    sys.exit(0)

try:
    opts, args = getopt.getopt(sys.argv[1:],'di:o:h')
except getopt.GetoptError:
    Usage()
    sys.exit(2)
debug = 0
for o, a in opts:
    if o == '-h':
        Usage()
    elif o == '-d':
        debug = 1
    elif o == '-i':
        inputname = a
    elif o == '-o':
        outputname = a
    else:
        assert False, "unhandled option"

#file = open(sys.argv[1])
file = open(inputname)

count_s = {}
count_t = {}
dict_st = {}
lines = {}

def count(line):
    table = line.replace('#','').replace('[','').replace(']','')\
            .replace('?','').replace('!','').replace(',','')\
            .replace("'",'').replace('&quo','').replace(';','')\
            .replace('--','')\
            .replace('  ',' ').strip().split('|||') 
            # seems to be faster than with the RE '#\[\]?!'
    table[0] = ' '+table[0]+' '
    table[1] = ' '+table[1]+' '
    source = table[0]
    target = table[1]
    if not source == '' and not target == '':
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
        if (source, target) in lines:
            lines[(source, target)].append(N)
        else:
            lines[(source, target)] = [N]

#map(count, file)
N = 0
for line in file:
    N += 1
    count(line)

included_in_s = {}
included_in_t = {}
sets = {}

for k in count_s.iterkeys():
    tmp = 0
    dico = {}
    for (s, v) in count_s.iteritems():
        if ' '+k+' ' in s and k != s:
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
        if ' '+k+' ' in t and k != t:
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

file.close()

if debug:
    #print h.heap()
    print '===========count_s============='
    print count_s
    print '===========count_t============='
    print count_t
    print '===========dict_st============='
    print dict_st
    print '============================'

delete = []
threshold = math.log(N) - 0.01
if debug:
    print ">>> Threshold :", 
    print threshold
##################################
for ks, kdic in dict_st.iteritems():
    for kt in kdic.iterkeys():
        try:
            if debug:
                print "dict_st[ks][kt] ", 
                print dict_st[ks][kt]
                print "count_s[ks] ", 
                print count_s[ks]
                print 'debut|'+ks+'|fin'
                print "count_t[kt] ", 
                print count_t[kt]
                print 'debut|'+kt+'|fin'
                print "N ", 
                print N
            if -math.log( enrichment.fisher_exact_test(dict_st[ks][kt], \
                    count_s[ks], count_t[kt], N)[1] ) > threshold:
                for l in lines[(ks, kt)]:
                    delete.append(l)
        except OverflowError:
            # The value is so low that even your mo****
            # Discard this entry
            for l in lines[(ks, kt)]:
                delete.append(l)

delete.sort() 

if debug:
    print ">>> Lines to delete:",
    print delete

file = open(inputname)
outputfile = open(outputname, 'w')
i = 0
for line in file:
    i += 1
    if not i in delete:
        outputfile.write(line)
outputfile.close()

