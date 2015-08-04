#!/usr/bin/env python
__author__ = "Huaibo Sun"
__email__ = "sunhuaibo@novogene.com"
__version__ = "V1.0"
__data__ = "2015-08-04"
import sys
import os
import argparse
from collections import defaultdict
#from gzip import open as gz_open
def usage():
    print 'Usage: python %s <infile.fna> > derep.fana' %(sys.argv[0])


def read_fasta(fa):
    ''' This function is read fasta format file.
        Argument is a filehandle of fasta.
        Return value is (name,seq).
    '''
    name , seq = '' , []
    name = fa.readline().rstrip()[1:]
    while True:
        line = fa.readline().rstrip()
        if not line:
            break
        elif line.startswith('>'):
            yield (name, ''.join(seq))
            name, seq = line[1:], []
        else:
            seq.append(line)
    if name:
        yield (name, ''.join(seq))

def main():
    if (len(sys.argv) < 2): 
        usage()
        sys.exit()
    sequence_read_f = open(sys.argv[1],'r')
    seq_repnum = defaultdict(lambda:0)
    seq_id = {}
    for seq_name, seq_base in read_fasta(sequence_read_f):
        seq_repnum[seq_base]+=1
        if seq_id.get(seq_base,0):
            continue
        else:
            seq_id[seq_base] = seq_name
#    for i in sorted(seq_repnum.iteritems(),key=lambda x:x[1],reverse=True):
#    for i in sorted(seq_repnum.iteritems(),key=lambda x:len(x[0]),reverse=True):
#            print ">%s;size=%d;\n%s" %(seq_id[i[0]],i[1],i[0])
    seq_sort = sorted(seq_repnum.keys(),key=len,reverse=True)
    for i in range(1,len(seq_sort)-1):
        for j in range(0,i-1):
            if len(seq_sort[i]) == len(seq_sort[j]):
                break
            elif seq_sort[i] in seq_sort[j]:
                seq_repnum[seq_sort[j]]=seq_repnum[seq_sort[i]]+seq_repnum[seq_sort[j]]
                del seq_repnum[seq_sort[i]]
                del seq_id[seq_sort[i]]
                break
    for i in sorted(seq_repnum.iteritems(),key=lambda x:x[1],reverse=True):
        print ">%s;size=%d;\n%s" %(seq_id[i[0]],i[1],i[0])

if __name__ == '__main__' :
    main()
