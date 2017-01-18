#!/usr/bin/env python
#-*- coding=utf-8 -*-
"""This script is to calculate alpha diversity index
Usage: python %prog <infile> > outfile"""
import os
import sys
import pandas as pd
import numpy as np
def Usage():
    exit(__doc__)
class alpha_diversity():
    def __init__(self,vector):
        self.vector = np.array(vector)
    def simpson(self):
        """https://en.wikipedia.org/wiki/Diversity_index#Shannon_index"""
        return sum(self.vector**2)
    def simpson_inverse(self):
        """https://en.wikipedia.org/wiki/Diversity_index#Shannon_index"""
        return 1 / self.simpson()
    def simpson_gini(self):
        """https://en.wikipedia.org/wiki/Diversity_index#Shannon_index"""
        return 1 - self.simpson()
    def shannon(self):
        """https://en.wikipedia.org/wiki/Diversity_index#Shannon_index"""
        return -(sum(self.vector * np.log(self.vector)))
    def evenness(self):
        """S = H(obs)/H(max)
        Where H(obs) is the number derived from the Shannon diversity index and H(max) is the maximum possible value of H(obs) (if every species was equally likely)
        https://en.wikipedia.org/wiki/Species_evenness"""
        obs = self.shannon()
        count = self.vector.shape[0]
        max_freq = 1.0 / count
        max_vector = np.repeat(max_freq,count)
        pre = -(sum(max_vector * np.log(max_vector)))
        return obs / pre
    def clonality(self):
        """ S = 1 − H(obs)/H(max)  ref: DOI: 10.1126/scitranslmed.3010760 """
        return 1 - self.evenness()
class beta_diversity():
    def __init__(self,vector1,vector2):
        self.vector1 = np.array(vector1)
        self.vector2 = np.array(vector2)
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
        sum_v1 = sum(self.vector1)
        sum_v2 = sum(self.vector2)
        bc_dis = diff_vector / (sum_v1 + sum_v2)
        return dc_dis
    def euclidean(self):
        euclidean_dis = np.sqrt((sum((self.vector1 - self.vector2)**2))
        return euclidean_dis
    def manhattan(self):
        manhattan_dis = sum((vector1 - vector2))
        return manhattan_dis
def main():
    a = np.random.rand(10)
    b = alpha_diversity(a)
    print "simpson:" + str(b.simpson())
    print "simpson_inverse:" + str(b.simpson_inverse())
    print "simpson_gini:" + str(b.simpson_gini())
    print "shannon:" + str(b.shannon())
    print "evenness:" + str(b.evenness())
    print "clonality:" + str(b.clonality())
if __name__ == "__main__":
    main()
