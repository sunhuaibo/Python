#!/usr/bin/env python
import sys,os
import re
import argparse

__author__ = "Huaibo Sun"
__email__ = "sunhuaibo@novogene.com"
__version__ = "V1.0"
__data__ = "2015-08-07"

parser = argparse.ArgumentParser(description = "Find taxonomy via the gi number of ncbi")
parser.add_argument('-i','--input_gi',help = " input gi number ",required = True)
parser.add_argument('--nodes',help = "input nodes.dmp file",required = True)
parser.add_argument('--names',help = "input names.dmp file",required = True)
parser.add_argument('-o','--output',help = "outputfile name",required = True)
opt = vars(parser.parse_args())

def usage():
	print "python %s <gi.list> <nodes.dmp> <names.dmp> > out.txt" % sys.argv[0]
def nodes(handle):
	gi_lever = {}
	fr = open(handle,'r')
	for line in fr:
		array = re.split("\s+\|\s+",line)
		gi_lever[array[0]] = array[1:3]
	fr.close()
	return gi_lever
def names(handle):
    gi_name = {}
    fr = open(handle,'r')
    for line in fr:
        if re.search(r'scientific name',line):
            array = re.split(r'\s+\|\s+',line)
            gi_name[array[0]] = array[1]
    fr.close()
    return gi_name
def find_gi(gi):
    if not gi_lever.get(gi,0):
        return None
    elif (gi_lever[gi][1] == "superkingdom"):
        return gi
    else:
        return (gi+";"+find_gi(gi_lever[gi][0]))
def find_tax(gi):
    tax=[]
    for i in range(len(gi)):
        xx = lever_abbr[i]+gi_name[gi[i]]
        tax.append(xx)
    return tax
if __name__ == '__main__':
#   if len(sys.argv) < 2:
#        usage()
#        sys.exit()
#    gi_list,nodes_in,names_in = sys.argv[1:]
    nodes_in = opt["nodes"]
    names_in = opt["names"]
    gi_list = opt["input_gi"]
    fw = open(opt["output"],'w')


    gi_lever = nodes(nodes_in)
    gi_name = names(names_in)
    fr = open(gi_list,'r')
    lever_abbr = ["k__","p__","c__","o__","f__","g__","s__"]
    lever = ["superkingdom","phylum","class","order","family","genus","species"]
    for line in fr:
        gi = line.strip()
        return_gi = find_gi(gi)
        return_gi = return_gi.split(";")[::-1]
        return_gi_del = []
        for i in return_gi:
            if gi_lever[i][1] in lever:
                return_gi_del.append(i)
        return_tax = find_tax(return_gi_del)
#        print ";".join(return_tax)
        fw.write(";".join(return_tax)+"\n") 
    fr.close()
    fw.close()
