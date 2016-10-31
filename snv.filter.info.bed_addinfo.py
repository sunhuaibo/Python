#!/usr/bin/python
import sys
if len(sys.argv) < 2:
    print "usage: python %s <som_var.txt> <snv.filter.info.bed> > snv.filter.info.add.bed" %sys.argv[0]
    exit()
fr = open(sys.argv[1],'r')
def pos(head):
    head_pos = {}
    i = 0
    for term in head:
        head_pos[term] = i
        i += 1
    return head_pos
#[Chr,Start,Case_var_freq,Cosmic]
dic_info = {}
i = 1
for line in fr:
    if i == 1:
        head = line.strip().split("\t")
        head_pos = pos(head)
    else:
        line_arr = line.strip().split("\t")
        chr_hsa = line_arr[head_pos["Chr"]]
        start = line_arr[head_pos["Start"]]
        Case_var_freq = line_arr[head_pos["Case_var_freq"]]
        Cosmic = line_arr[head_pos["Cosmic"]]
        dic_id = chr_hsa + "_" + start
        dic_info[dic_id] = [Case_var_freq,Cosmic]
    i += 1
fr.close()
fr = open(sys.argv[2],'r')
i = 1
for line in fr:
    line_arr = line.strip().split("\t")
    if i == 1:
        line_arr = line_arr[0:-1]
        line_arr.extend(["Gene","cHGVS","pHGVS","Function","Case_var_freq","Cosmic"])
        print "\t".join(line_arr)
    else:
        dic_id = line_arr[0] + "_" + line_arr[1]
        if dic_info.get(dic_id,False):
            line_arr.extend(dic_info[dic_id])
        else:
            line_arr.extend(["-","-"])
        print "\t".join(line_arr)
    i += 1
fr.close()
