#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import numpy as np
import pandas as pd
from collections import defaultdict

if len(sys.argv) < 2:
	usage = """
	Split infile.txt[csv] according to group.list
	Usge: python %s <infile.txt> <group.list>""" %sys.argv[0]
	exit(usage)
infile = sys.argv[1]
group = sys.argv[2]
fr = open(group,'r')
group_sam = defaultdict(list)
i = 1
for line in fr:
	line = line.strip().split("\t")
	if i == 1:
		pass
	else:
		group_sam[line[1]].append(line[0])
	i += 1
fr.close()
if (infile.endswith(".csv")):
	dat = pd.read_csv(infile,index_col=0)
else:
	dat = pd.read_table(infile,index_col=0)
for key in group_sam:
	sub_dat = dat[group_sam[key]]
	columns = sub_dat.columns
#	sub_dat=sub_dat.sort_values(columns[0],ascending=False)
	outname = key + ".csv"
	fr = open(outname,'w')
	sub_dat.to_csv(outname)
	fr.close()
