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
        """vector """
        self.vector = np.array(vector)
    def simpson(self):
        """https://en.wikipedia.org/wiki/Diversity_index#Shannon_index"""
        freqs = self.vector / self.vector.sum()
        return sum(freqs**2)
    def simpson_inverse(self):
        """https://en.wikipedia.org/wiki/Diversity_index#Shannon_index"""
        return 1 / self.simpson()
    def simpson_gini(self):
        """https://en.wikipedia.org/wiki/Diversity_index#Shannon_index"""
        return 1 - self.simpson()
    def shannon(self):
        """https://en.wikipedia.org/wiki/Diversity_index#Shannon_index"""
        freqs = self.vector / self.vector.sum()
        nonzero_freqs = freqs[freqs.nonzero()]
        return -(sum(nonzero_freqs * np.log(nonzero_freqs)))
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
    def singles(self,size=1):
        """Calculate number of single occurrences (singletons)."""
        return (self.vector == size).sum()
    def doubles(self):
        """Calculate number of double occurrences (doubletons)."""
        return (self.vector == 2).sum()
    def osd(self):
        """Calculate observed OTUs, singles, and doubles."""
        return self.observed_otus(), self.singles(), self.doubles()
    def robbins(self):
        """Calculate Robbins' estimator for the probability of unobserved outcomes."""
        return self.singles(self.vector) / self.vector.sum()
    def observed_otus(self):
        """Calculate the number of distinct OTUs."""
        return (self.vector != 0).sum()
    def pielou_e(self):
        """Calculate Pielou's Evenness index J'."""
        return self.shannon() / np.log(self.observed_otus())
    def berger_parker_d(self):
        """Calculate Berger-Parker dominance.Berger-Parker dominance is defined as the fraction of the sample that belongs to the most abundant OTU."""
        return self.vector.max() / self.vector.sum()
    def goods_coverage(self):
        """Calculate Good's coverage of counts."""
        f1 = self.singles()
        N = self.vector.sum()
        return 1 - (f1 / N)
    def chao1(self, bias_corrected=True):
        """Calculate chao1 richness estimator. Uses the bias-corrected version unless `bias_corrected` is ``False`` *and* there are both singletons and doubletons.

        bias_corrected : bool, optional Indicates whether or not to use the bias-corrected version of the equation. If False` *and* there are both singletons and doubletons, the uncorrected version will be used. The biased-corrected version will be used otherwise."""
        o, s, d = self.osd()
        if not bias_corrected and s and d:
            return o + s ** 2 / (d * 2)
        else:
            return o + s * (s - 1) / (2 * (d + 1))
    
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
