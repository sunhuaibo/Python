#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import xlrd
if len(sys.argv) < 2:
    print """
    This script extract sheet from Excel form file\n
    Usage: python %s <in.xlsx> <sheet_name> > out.txt
    """ %sys.argv[0]
    exit()
data = xlrd.open_workbook(sys.argv[1])
table = data.sheet_by_name(sys.argv[2])
nrows = table.nrows
for i in xrange(nrows):
    line = table.row_values(i)
    line = map(str,line)
    print "\t".join(line)
