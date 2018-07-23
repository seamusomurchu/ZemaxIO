#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 15:27:35 2018

@author: james

This file should load a ray database viewer text file from Zemax Non-Sequential mode.
Should read file and load it.
In particular, find incident ray angles on the detector viewer file

To use this program you will have to make certain your ray database viewer file
is set up correctly and exported from zemax. Refer to zemax documentation for RDB

For now, I'm including all '7' options ticked... except processed data?
"""

import numpy as np
import matplotlib.pyplot as plt

def RDBLoad():
    
    filename = 'RDBdata.txt'
    with open(filename, "r") as ins:
        array = []
        for line in ins:
            lsplit = line.split()
            lsplit = np.asarray(lsplit)
            print lsplit, type(lsplit), len(lsplit)
#            if len(lsplit) > 0 and lsplit[0] is '4':
#                print lsplit
#            else:
#                return

            #print line, line[3]
#            if line[3] is '0':
#                print line
#                array.append(line)
#            else:
#                return
     
        return

def RDBMain():
    
    RDBLoad()
    
    return




