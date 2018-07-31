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

def RDBLoad(segnum):
    
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
                raysplit = raysplit[1].split(',')
                raynum = np.append(raynum, raysplit[0])
                #print raysplit, raysplit[1]
                continue
                
            elif line[0] is 'S': #If line begins with R or S, skip
                continue
            
            lsplit = line.split()
            lsplit = np.asarray(lsplit)

            """here 4 refers to segment 4, the Dichroic from the zemax model
            """
            if int(lsplit[0]) == segnum:  #segnum is passed in from main for multiple segments to be loaded
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
        #print Nx, Ny, Nz, theta
        
        #this value of theta should be check, was expecting 20degish
        #add angle to seg array

    return thetas

def AngleHist(thetas):
    #need to fix this as I was expecting 45deg. (90+45=135, could be fault)
    plt.figure(0)
    plt.hist(abs(thetas - 180), bins=16)
    plt.xlabel('Angle of Incidence')
    plt.ylabel('Number of rays per Bin')
    plt.title('Dichroic AoI Histogram')
    plt.show
    
    return

def DetPlotter(sarr1, sarr2, thetas):
    #plot ray number on detector surfaces, multiplot
    x1 = np.asarray(sarr1[:,10], dtype=np.float32)
    y1 = np.asarray(sarr1[:,11], dtype=np.float32)
    x2 = np.asarray(sarr2[:,10], dtype=np.float32)
    y2 = np.asarray(sarr2[:,11], dtype=np.float32)
    raytxt1 = np.asarray(sarr1[:,0], dtype=np.int)
    raytxt2 = np.asarray(sarr2[:,0], dtype=np.int)
    thetas = np.around(abs(thetas - 180), decimals=1)
    
    plt.figure(1)
    plt.subplot(121)
    plt.scatter(x1, y1)
    plt.axis([-75, 75, -75, 75])
    plt.axis('equal')
    plt.xlabel('X axis QUBIC GRF [mm]')
    plt.ylabel('Y axis QUBIC GRF [mm]')
    plt.title('Rays from Horns')
    
    for i, txt in enumerate(raytxt1):
        plt.annotate(txt, (x1[i], y1[i]))
    
    plt.subplot(122)
    plt.scatter(x2, y2)
    plt.axis('equal')
    plt.xlabel('X axis PG RF [mm]')
    plt.ylabel('Y axis PG RF [mm]')
    plt.title('Rays in Dichroic Plane')
    
    for i, txt in enumerate(raytxt2):
        plt.annotate(txt, (x2[i], y2[i]))
    
    plt.show()
    
    plt.figure(2)
    plt.scatter(x2, y2)
    plt.axis('equal')
    plt.xlabel('X axis PG RF [mm]')
    plt.ylabel('Y axis PG RF [mm]')
    plt.title('Ray Angles in Dichroic Plane')
    
    for i, txt in enumerate(thetas):
        plt.annotate(txt, (x2[i], y2[i]))
    
    plt.show()
    
    return
    

def RDBMain():
    plt.close('all') # close all open figures
    
    #remove header from RDB file
    RDBrmHeader()
    #return array of segment/dichroic
    #could pass in segment number here for generalisation
    #return segment array for specific segment
    #first test segment
    segment_number1 = 1
    segmentarray1 = RDBLoad(segment_number1)
    #Dichroic segment
    segment_number5 = 5
    segmentarray5 = RDBLoad(segment_number5)
    
    #calculate angle of incidence from RDB data
    thetas = AngleOfIncidence(segmentarray5)
    
    #plot histogram
    AngleHist(thetas)
    
    #plot rays on detectors
    DetPlotter(segmentarray1, segmentarray5, thetas)
    
    return

RDBMain()


