#!/usr/bin/python
# -*- coding=utf-8 -*-
import sys
import os
import re
from collections import defaultdict

indir = sys.argv[1]
#sample = ["P001","P002","P003","P004","P005"]
sample = ["P001"]
for term in sample:
	indir_tmp = indir + "/" + term + "/check/check_snv/"
	indir_fold = os.listdir(indir_tmp)
	sample_merge_dic = defaultdict(list)
	out_file = term + "_merge_checkSNV.txt"
	fw = open(out_file,"w")
	dic_all = defaultdict(list)
	total_col = 0
	gene_id = []
	dic_uniq = {}
	total_file = 0
	for infile in indir_fold:
		sample = infile
		infile = indir_tmp + infile + "/snv.filter.info.add.bed"
		print infile
		fr = open(infile,"r")
		total_file += 1
		every_col = 0
		i = 1
		for line in fr:
			arr_line = line.strip().split("\t")
			dic_id = "_".join(arr_line[0:5])
			if i == 1:
				for j in xrange(5,len(arr_line)):
					arr_line[j] += "(%s)" %sample
			i += 1
			if every_col == 0:
				every_col = len(arr_line) - 5
				total_col += every_col
			if not dic_uniq.get(dic_id,False):
				gene_id.append(dic_id)
				dic_uniq[dic_id] = 1
			if total_file == 1:
				dic_all[dic_id].extend(arr_line[5:])
			elif dic_all.get(dic_id,False) and (total_col-every_col) == len(dic_all[dic_id]):
				dic_all[dic_id].extend(arr_line[5:])
			elif dic_all.get(dic_id,False) and (total_col-every_col) != len(dic_all[dic_id]):
				term_col_num = len(dic_all[dic_id])
				less_col = total_col - term_col_num - every_col
				dic_all[dic_id].extend([0] * less_col)
				dic_all[dic_id].extend(arr_line[5:])
			else:
				dic_all[dic_id].extend([0] * (total_col - every_col))
				dic_all[dic_id].extend(arr_line[5:])

		fr.close()
	for term in gene_id:
		for i in xrange(total_col):
			term_col_num = len(dic_all[term])
			if term_col_num < total_col:
				less_col = total_col - term_col_num
				dic_all[term].extend([0] * less_col)
		term_col_num = len(dic_all[term])
		line_out = term.split("_")
		line_out.extend(dic_all[term])
#		fw.write(term + "\t" + "\t".join([str(x) for x in dic_all[term]])+"\n")
		fw.write("\t".join([str(x) for x in line_out])+"\n")
	fw.close()
