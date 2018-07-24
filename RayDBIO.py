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
import pandas as pd
import re
import os

def RDBrmHeader():
    #uses bash from OS to remove header, NB +13 is hardcoded
    script = """
            bash -c 'tail -n +13 "RDBdata64.txt" > "RDBdata_noheaderTMP.txt" && mv "RDBdata_noheaderTMP.txt" "RDBdata64noheader.txt"'
            """
    os.system ("bash -c '%s'" % script)
    
    return 

def RDBLoad():
    
    filename = '/home/james/ZemaxIO/RDBdata_noheader64.txt'
    with open(filename, "r") as ins:
        arrayrow = np.zeros([27]) #need to keep array correct length/comments from data
        for line in ins:
            
            if re.match(r'^\s*$', line): #Skip blank lines in file
                continue
            elif line[0] is 'R' or line[0] is 'S': #If line begins with R or S, skip
                continue
            
            lsplit = line.split()
            lsplit = np.asarray(lsplit)

            """here 4 refers to segment 4, the Dichroic from the zemax model
            """
            if int(lsplit[0]) == 4: 
                #print lsplit, type(lsplit), len(lsplit), type(lsplit[0])
                lsplit = lsplit[0:27]
                arrayrow = np.vstack((arrayrow, lsplit))

        arrayrow = arrayrow[1:127,:] # delete first row zeros
        #drop duplicate rows, NB returns sorted numpy array
        print arrayrow.shape, arrayrow[0]
        arrayrow = np.unique(arrayrow, axis=0)
        print arrayrow.shape, arrayrow[0]
        return arrayrow

def RDBMain():
    #remove header from RDB file
    RDBrmHeader()
    #return array of segment/dichroic
    #could pass in segment number here for generalisation
    segmentarray = RDBLoad()
    print segmentarray.shape, segmentarray[0]
    
    return




