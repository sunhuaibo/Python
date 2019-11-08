#!/usr/bin/env python
#-*- coding=utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np
from collections import Counter

def sampling(vector,size,replace=True):
    """This function is to normalization of vector
    -size   The upper limit of depths"""
    vector_range = []
    vector_return = []
    for ix,term in enumerate(vector):
        tmp = [ix] * int(term)
        vector_range.extend(tmp)
    np.random.shuffle(vector_range)
    choice = np.random.choice(vector_range, size, replace=replace)
    del vector_range
    count = Counter(choice)
    vector_return = [count.get(x, 0) for x in range(len(vector))]
    return vector_return
def main():
    '''This is test'''
    a = [10,5,3,1,1]
    b = sampling(a, 10)
    print(a)
    print(b)
if __name__ == "__main__":
    main()
