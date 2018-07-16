#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 16:41:24 2018

@author: james

program takes zemax text input and computues / calculates xy coordinates
for later analysis/program in this same folder. TBD.

Currently is specific to zemax non sequential mode detector viewer text file
but potentially could be generalised to all zemax
"""
import numpy as np

#import pixel matrix as 'data'
filename = 'detviewdata.txt'
data = np.loadtxt(filename, skiprows=24)

#load zemax params from file header
with open("detviewdata.txt") as fp:
    for i, line in enumerate(fp):
        if i == 8:
            fileinfo = line
            lineinfo = fileinfo.split()
            detwidth = lineinfo[1]
            detheight = lineinfo[4]
            pixwidth = lineinfo[8]
            pixheight = lineinfo[11]
            hitnum = lineinfo[16]
        elif i == 14:
            xcen = line          
            xcen = xcen.split()
            xcen = xcen[3]
        elif i > 23:
            break


