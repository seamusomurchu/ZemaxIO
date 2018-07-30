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
import re
import os
import matplotlib.pyplot as plt

def RDBrmHeader():
    #uses bash from OS to remove header, NB +13 is hardcoded
    script = """
            tail -n +13 "RDB_64.txt" > "RDBdata_noheaderTMP.txt" && mv "RDBdata_noheaderTMP.txt" "RDBdata64noheader_64.txt"
            """
    os.system ("bash -c '%s'" % script)
    
    return 

def RDBLoad():
    
    filename = '/home/james/ZemaxIO/RDBdata64noheader_64.txt'
    with open(filename, "r") as ins:
        #setup arrays
        arrayrow = np.zeros([27]) #need to keep array correct length/comments from data
        raynum = np.array([])
        
        for line in ins:
            
            if re.match(r'^\s*$', line): #Skip blank lines in file
                continue
            
            elif line[0] is 'R': #Capture RDB ray-number from this logic
                raysplit = line.split()
                raysplit = np.asarray(raysplit)
                raynum = np.append(raynum, raysplit[1])
                #print raysplit, raysplit[1]
                continue
                
            elif line[0] is 'S': #If line begins with R or S, skip
                continue
            
            lsplit = line.split()
            lsplit = np.asarray(lsplit)

            """here 4 refers to segment 4, the Dichroic from the zemax model
            """
            if int(lsplit[0]) == 5: 
                #print lsplit, type(lsplit), len(lsplit), type(lsplit[0])
                lsplit = lsplit[0:27]
                arrayrow = np.vstack((arrayrow, lsplit))


        #test RDB ray num logic here
        arrayrow = arrayrow[1:129,:] # delete first row zeros
        #print raynum.shape, arrayrow.shape
        arrayrow = np.c_[raynum, arrayrow]
        #print arrayrow.shape
        #drop duplicate rows, NB returns sorted numpy array
        #print arrayrow.shape, arrayrow[0]
        arrayrow = np.unique(arrayrow, axis=0)
        return arrayrow

def AngleOfIncidence(sarr):
    #see zemax documentation for this calculation
    #make histograms of angles of incidence in Nx, Ny, & Nz
    thetas = np.array([])
    for row in sarr:
        L = float(row[13])
        M = float(row[14])
        N = float(row[15])
        Nx = float(row[16])
        Ny = float(row[17])
        Nz = float(row[18])
#        i = L*Nx + M*Ny + N*Nz
#        j = np.sqrt(L**2 + M**2 + N**2)
#        k = np.sqrt(Nx**2 + Ny**2 + Nz**2)
        theta = np.arccos( L*Nx + M*Ny + N*Nz / (np.sqrt(L**2 + M**2 + N**2) * np.sqrt(Nx**2 + Ny**2 + Nz**2)))
        theta = np.rad2deg(theta)
        thetas = np.append(thetas, theta)
        print Nx, Ny, Nz, theta
        
        #this value of theta should be check, was expecting 20degish
        #add angle to seg array

    return thetas

def AngleHist(thetas):
    #need to fix this as I was expecting 45deg. (90+45=135, could be fault)
    plt.figure()
    plt.hist(thetas - 180, bins=16)
    plt.xlabel('Angle of Incidence')
    plt.ylabel('Number of rays per Bin')
    plt.title('Dichroic AoI Histogram')
    plt.show
    
    return

def RDBMain():
    #remove header from RDB file
    RDBrmHeader()
    #return array of segment/dichroic
    #could pass in segment number here for generalisation
    segmentarray = RDBLoad()
    #print segmentarray.shape, segmentarray[0]
    
    #calculate angle of incidence from RDB data
    thetas = AngleOfIncidence(segmentarray)
    
    #plot histogram
    AngleHist(thetas)
    
    return

RDBMain()


