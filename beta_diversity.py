#!/usr/bin/env python
#-*- coding=utf-8 -*-
"""This script is to calculate Morisita–Horn overlap index
Usage: python %prog <infile> > outfile"""
import os
import sys
import pandas as pd
def Usage():
    exit(__doc__)
class betadiversity():
    def __init__(self,vector1,vector2):
        self.vector1 = vector1
        self.vector2 = vector2
    def morisita(self):
        """This function is to calculate Morisita–Horn overlap index
        Ref:  http://dx.doi.org/10.1016/j.it.2015.09.006"""
        diff_vector = sum(self.vector1 * self.vector2)
        v1 = sum(self.vector1 ** 2)
        v2 = sum(self.vector2 ** 2)
        morisita_dis = 2 * diff_vector / (v1 + v2)
        return morisita_dis
    def bray_curtis(self):
        """This function is to calculate bray_curtis distance"""
        diff_vector = sum(self.vector1 - self.vector2)
        sum_v1 = self.vector1.sum()
        sum_v2 = self.vector2.sum()
        bc_dis = diff_vector / (sum_v1 + sum_v2)
        return bc_dis
    def euclidean(self):
        euclidean_dis = np.sqrt((self.vector1 - self.vector2).pow(2).sum())
        return euclidean_dis
    def manhattan(self):
        manhattan_dis = (self.vector1 - self.vector2).sum()
        return manhattan_dis

def main():
    if len(sys.argv) < 3:
        Usage()
    infile = sys.argv[1]
    sampleid = sys.argv[2]
    if infile.endswith(".csv"):
        df = pd.read_csv(infile,header=0,index_col=0)
    else:
        df = pd.read_csv(infile,header=0,index_col=0,sep="\t")
    df = df.fillna(0)
    df = df.filter(regex="^T",axis=1)
    total = df.sum()
    df = df / total
    df_colname = df.columns
    out_result = {}
    out = pd.Series()
    for i in range(len(df_colname)-1):
        for j in range(i + 1,len(df_colname)):
            vector1 = df[df_colname[i]]
            vector2 = df[df_colname[j]]
            key1 = "_".join([df_colname[i],df_colname[j]])
            key2 = "_".join([df_colname[j],df_colname[i]])
            if out_result.get(key1,False) or out_result.get(key2,False):
                pass
            else:
                morisita_index = morisita(vector1,vector2)
                out_result[key1] = morisita_index
                out[key1] = morisita_index
    for key in out_result:
        print "\t".join([key,str(out_result[key])])
    mean = out.mean()
    sys.stderr.write("\t".join([sampleid,str(mean)]) + "\n")
if __name__ == "__main__":
    main()
