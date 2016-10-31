#!/usr/bin/python
# -*- coding=utf-8 -*-
import sys
import os
import re
from collections import defaultdict

indir = sys.argv[1]
sample = ["P001","P002","P003","P004","P005"]
for term in sample:
	indir_tmp = indir + "/" + "term" + "/check/check_snv/"
	indir_fold = os.listdir(indir_tmp)
	sample_merge_dic = defaultdict(list)
	out_file = term + "_merge.txt"
	fw = open(out_file,"w")
	dic_all = defaultdict(list)
	total_col = 0
	gene_id = []
	dic_uniq = {}
	total_file = 0
	for infile in indir_fold:
		fr = safe_open(infile,"r")
		total_file += 1
		every_col = 0
		for line in fr:
			arr_line = line.strip().split("\t")
			dic_id = "_".join(arr_line[0:5])
			if every_col == 0:
				every_col = len(arr_line) - 5
				total_col += every_col
			if not dic_uniq.get(dic_id,False):
				gene_id.append(dic_id)
				dic_uniq[arr_line[0]] = 1
			if total_file == 1:
				dic_all[arr_line[0]].extend(arr_line[5:])
			elif dic_all.get(arr_line[0],False):
				dic_all[arr_line[0]].extend(arr_line[5:])
			else:
				dic_all[arr_line[0]].extend([0] * total_col)
				dic_all[arr_line[0]].extend(arr_line[5:])

		fr.close()
	for term in gene_id:
		term_col_num = len(dic_all[term])
		if term_col_num < total_col:
			continue
		fw.write(term + "\t" + "\t".join([str(x) for x in dic_all[term]]),"\n")
	fw.close()
