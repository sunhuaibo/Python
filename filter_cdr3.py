#!/usr/bin/python
# -*- coding=utf-8 -*-
import sys,os
from argparse import ArgumentParser

parse = ArgumentParser()
parse.add_argument("-indir",help="Input project dir",required=True)
parse.add_argument("-sample",help="Input sample.list",required=True)
parse.add_argument("-freq",help="Filter frequence",default=0.001)
parse.add_argument("-outdir",help="Out file dir",default="./")
opt=vars(parse.parse_args())

def pos(head):
	head = head.split("\t")
	head_d = {}
	for i in xrange(len(head)):
		head_d[head[i]] = i
	return head_d

#def filter_tsv(infile,outdir,sampleid,freq):
def filter_tsv(infile,outfile,freq):
#	outdir_sam = outdir + "/" + sampleid
#	if not os.path.isdir(outdir_sam):
#		os.mkdir(outdir_sam)
#	infile_basename,extend_name = os.path.splitext(os.path.basename(infile))

#	outfile = outdir_sam + "/" + infile_basename + "_filter" + extend_name
	fr = open(infile,'r')
	fw = open(outfile,'w')
	i = 1
	filter_col = ["cloneFraction","aaSeqCDR3"]
	for line in fr:
		line = line.strip()
		if i == 1:
			head_pos_d = pos(line)
			fw.write(line + "\n")
		else:
			line_l = line.split("\t")
			if "*" in line_l[head_pos_d[filter_col[1]]] or "_" in line_l[head_pos_d[filter_col[1]]]:
				continue
			if float(freq) < float(line_l[head_pos_d[filter_col[0]]]):
				 fw.write("\t".join(line_l) + "\n")
		i += 1
	fr.close()
	fw.close()
def main():
	indir = opt["indir"].strip()
	indir = os.path.abspath(indir)
	freq = opt["freq"]
	sample_list = opt["sample"]
	outdir = opt["outdir"].strip()
	outdir = os.path.abspath(outdir)
	outdir += "/result_filter"
	if not os.path.isdir(outdir):
		os.mkdir(outdir)
	fr = open(sample_list,'r')
	i = 1
	out_path_list = outdir + "/out_path.list"
	fw = open(out_path_list,'w')

	for line in fr:
		line = line.strip()
		if i == 1:
			pass
		else:
			line_l = line.split("\t")
			sampleid = line_l[3]
			if "PD" in line_l[5]:
				freq = 0.001
			elif "TD" in line_l[5]:
				freq = 0.0001
			elif "CD" in line_l[5]:
				freq = 0.00001
			else:
				print sampleid + " is not in PD/CD/TD"
				
			infile = indir + "/" + sampleid + "/" + sampleid + ".tsv"
			outfile = outdir + "/" + sampleid
			if not os.path.isdir(outfile):
				os.mkdir(outfile)
			infile_basename,extend_name = os.path.splitext(os.path.basename(infile))
			outfile += "/" + infile_basename + "_filter" + extend_name
			fw.write(sampleid + "\t" + outfile + "\n")
			filter_tsv(infile,outfile,freq)
		i += 1
	fr.close()
	fw.close()
if __name__ == "__main__":
	main()
