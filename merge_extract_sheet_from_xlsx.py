#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import xlrd
from collections import defaultdict
if len(sys.argv) < 2:
	print """
	This script extract sheet from Excel form file\n
	Usage: python %s <sample.list> <sheet_name> > out.txt
	""" %sys.argv[0]
	exit()
samplelist = sys.argv[1]
#data = xlrd.open_workbook(sys.argv[1])
out_dic = defaultdict(list)
fr = open(samplelist,'r')
head = []
uniq_dic = {}
for line in fr:
	line = line.strip()
	data = xlrd.open_workbook(line)
	table = data.sheet_by_name(sys.argv[2])
	nrows = table.nrows
	basename = os.path.basename(line)
	name,extend = os.path.splitext(basename)
	for i in xrange(nrows):
#		line = table.row_values(i)
		cell_1 = table.cell(i,0).value
		cell_2 = table.cell(i,1).value
		if i == 0:
			name = cell_2 + "(" + name + ")"
			out_dic[cell_1].append(name)
		else:
			out_dic[cell_1].append(cell_2)
		if not uniq_dic.get(cell_1,False):
			uniq_dic[cell_1] = 1
			head.append(cell_1)

for key in head:
	out_dic[key] = map(str,out_dic[key])
	print key + "\t" + "\t".join(out_dic[key])
