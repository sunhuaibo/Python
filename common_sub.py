#!/usr/bin/python
# -*- coding=utf-8 -*-
import sys,os

def pos(array):
	""" This function return array index """
	pos_dic = {}
	for i in xrange(len(array)):
		pos_dic[array[i]] = i
	return pos_dic
