#!/usr/bin/python
import os,sys
if len(sys.argv) < 2:
	exit("Usage: python %s <path> <sample> > out.txt" %sys.argv[0])
dir_all = os.listdir(sys.argv[1].strip())

fr = open(sys.argv[2],'r')
i = 1
out_dic = {}
for line in fr:
	if i > 2:
		line = line.strip().split("\t")
		out_dic[line[3]] = line[0]
	i += 1
for term in dir_all:
	term = term.strip()
	term = sys.argv[1] + "/" + term
	path = os.popen("readlink %s" %term).read().strip()
	sam_name = path.split("_")[-1]
	if out_dic.get(sam_name,False):
		print "\t".join([out_dic[sam_name],path])


