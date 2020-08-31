#!/usr/local/bin/python2

# Python script v2.7 for plot m-theta plot around annulus
# Sandeep Kumar , GTSL
# UC Aerospace Engg

# IMPORTANT : 
# This script is to supplement NAX - for details see gtsl.ase.uc.edu
# Keep this script in same dir as other NAX files

# Change the path ,files ,filedata : and it can used to read & plot any file
# 

import os
import numpy as np
import matplotlib.pyplot as plt

print ""
print " Post-processing : m'theta plots - section 10"
print " (NOTE: script not suitable for 'dtheta' change during NAX operations)"
print ""
#row = str(input("   Enter the row no:   "))
row =str(1)
#tot_blades= str(input("   Enter no of blades in row:   "))
tot_blades =str(20)
case_name="Case6_2"
#section = str(input("   Enter section no :   "))
section = str(2) 
print ""


delta_theta =  2*np.pi/int(tot_blades)
#
fig = plt.figure(figsize=(10,6))
ax = plt.subplot(1,1,1)
plt.xlabel('theta ( radians)')
plt.ylabel("m'")
   
ax.set_ylim([-0.4,0.8])
ax.set_xlim([0.0,6.6])
#    
os.chdir("./row"+row)    
for i in range(1,int(tot_blades)+1):
    path= str(row +".nax"+str(i))
    #print "path :",path , i, tot_blades
    os.chdir(path)
    
    plotfile = "blade."+str(section)+"."+str(row)+"."+case_name
    #print "reading file:",plotfile
    
    filedata = np.genfromtxt(plotfile, skip_header=2)
    m = filedata[:,][:,0]
    #theta =  float(delta_theta)*int(i) +filedata[:,][:,1]
    theta =  filedata[:,][:,1] 
    #print "m,theta:", m , theta
    
    plt.plot(theta,m,color='k')
    ax.text(float(delta_theta)*int(i),0.6,str(i),fontsize=7)

    os.chdir("../")
    
plt.axes().set_aspect('equal','datalim')
plt.axes().set_aspect('equal','box')

#    
       
os.chdir("../")
#plt.text(0.1,0.8,"blade#",fontsize=7)
plt.savefig("m_theta_row"+str(row)+"_"+"section"+str(section)+".png",dpi=300)
plt.show(block=False)
print "   Figure saved ... "
print ""

