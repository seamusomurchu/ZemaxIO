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
import matplotlib.pyplot as plt

def DataLoad():
    #import pixel matrix as 'data'
    filename = 'detviewdata.txt'
    data = np.loadtxt(filename, skiprows=24)
    data = data[:,1:101]
    
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
            elif i == 15:
                ycen = line
                ycen = ycen.split()
                ycen = ycen[3]
            elif i == 16:
                zcen = line
                zcen = zcen.split()
                zcen = zcen[3]
            elif i > 23:
                break
            
    return data, fileinfo, lineinfo, detwidth, detheight, pixwidth, pixheight, \
        hitnum, xcen, ycen, zcen

def XYcalc(data, xcen, ycen, zcen, detwidth, detheight, pixwidth, pixheight):
    #calculate array or matrix with xy positions of zemax detector
    #in its reference frame
    xmax = float(xcen) + 0.5*float(detwidth)
    xmin = float(xcen) - 0.5*float(detwidth)
    ymax = float(ycen) + 0.5*float(detheight)
    ymin = float(ycen) - 0.5*float(detheight)

    xcoords = np.linspace(xmin,xmax)
    ycoords = np.linspace(ymin,ymax)
    
    shapenum = float(detwidth) * float(detheight) / 2
    #print shapenum, type(shapenum)
    #reform data
    datamod = np.reshape(data, (int(shapenum),2))
    #print datamod.shape
    
    return xcoords, ycoords, xmin, xmax, ymin, ymax

def SpotPlot(data, xcoords, ycoords, xmin, xmax, ymin, ymax):
  
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.imshow(data, extent=[xmin, xmax, ymin, ymax])
    ax.set_aspect('equal')

#    for row in data[row,:]:
#        print "row", row
#        for col in row[col]:
#            print "col", col

    return    

def MainFunc():
    #Call data load params
    data, fileinfo, lineinfo, detwidth, detheight, pixwidth, pixheight, \
        hitnum, xcen, ycen, zcen = DataLoad()
        
    #print fileinfo, lineinfo, detwidth, detheight, pixwidth, pixheight, \
     #   hitnum, xcen, ycen, zcen       
    #print "data shape", data.shape
    
    #calculate coordinate array from pixel info
    #still need to assign data value to coordinates
    xcoords, ycoords, xmin, xmax, ymin, ymax = XYcalc(
            data, xcen, ycen, zcen, detwidth, detheight, pixwidth, pixheight)
    #print xcoords, ycoords   
    
    SpotPlot(data, xcoords, ycoords, xmin, xmax, ymin, ymax)
    
    
    return

# NEED TO THINK MORE ABOUT THIS DATA SHAPE AND PLOTTING METHOD
