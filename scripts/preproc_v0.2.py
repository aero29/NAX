#!/usr/bin/env python

# NAX v0.2 Aero-Design systems
# Python v2.7 Pre-processing script
# Calculates the FFT of distortion profile &
# creates the input file for further process

# ----------------------------------------------------
# Sandeep Kumar , GTSL , UC Aerospace
#------------------------------------------------------
# ------------------------------------------------------

# Library Imports

import os
import numpy as np
from numpy import genfromtxt
from scipy.fftpack import fft
import pandas , csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
import string


# Check for validity of Run 'distortion profile files should exist'

# Read from naxinfo.dat file 
# user input for non-axisymmetric rows in array , (naxrow)


os.chdir("./inputs")  

print " "
print "     Checking Inputs validity - "
print " "
def file_len(fname):
    with open(fname) as f:
        for i,l in enumerate(f):
            pass 
    return

if any(File.startswith("naxinfo") for File in os.listdir(".")):
    print ( "     Nax-info file Exist ")
else:
    print( "    ERROR : nax-info files not found")
    print( "    Execution Terminated ! ")
    exit(1)

with open("naxinfo.dat") as info:
    length=file_len("naxinfo.dat")
    f = open("naxinfo.dat","r")
    lineread = f.readlines()

for num,line in enumerate(lineread,1):
    linelist = line.split()

    if num == 15:
        axirow = (linelist[1])
    if num == 16:
        naxrow = (linelist[1])


totalnaxrows = len(naxrow.split(','))
print "     "
print "     Total non-axisymmetric rows :" , totalnaxrows
totalaxirows = len(axirow.split(','))
print "     Total axisymmetric rows     :" , totalaxirows
print "     -----   #   ----------   #   -----"

for j in range(totalnaxrows):

    currentrow = naxrow.split(',')[j]
    curr_dist_file = "distortion.row"+str(currentrow) +".csv"
    curr_3dbgb_file = "3dbgbinput."+str(currentrow) +".dat"
    #print "     Current Row :", currentrow
    #print "     Distortion File :" , curr_dist_file
    #print "     3dbgb input File :", curr_3dbgb_file 

    if any(File.startswith("distortion.row"+str(currentrow)) for File in os.listdir(".")):
        print ( "     Distortion profile  for  row " +str(currentrow)+"  Exist ")
        #print ("    ")
    else:
        print( "      ERROR : Distortion profile files not found")
        print( "      Execution Terminated ! ")
        exit(1)

    if any(File.startswith("3dbgbinput."+str(currentrow)) for File in os.listdir(".")):
        print ( "     3dbgb Input files for  row " +str(currentrow)+"  Exist ")
        print ("    ")
    else:
        print( "       ERROR : 3dbgb Input files not found")
        print( "       Execution Terminated ! ")
        exit(1)


    zero = [0.0]*11

# # read the distortion file
    # colnames = ['location', 'inlet_angle']
    # data = pandas.read_csv(curr_dist_file, names=colnames)   #should be distortion.row1.csv
    # theta = data.location.tolist()
    # alpha = data.inlet_angle.tolist()
    data = genfromtxt(curr_dist_file,delimiter=',')
    theta = data[:,0]
    alpha = data[:,1]
    n= len(alpha)

#    print "n:" , n

# #Calculate FFT
    a = fft(alpha)
    amp = np.abs(a)/(n/2)
    phase = np.angle(a)
    #print ' Amplitude', amp[0]
    #print ' Phase', phase[0]
    #print amp


# # Plot the values
# # Figure1 : Data for Amplitude and Phase values
    fig,ax = plt.subplots()
    ax.plot(phase[0:11],'o-',label='Phase')
    ax.plot(amp[0:11],'r-^',label='Amplitude')
    ax.plot(zero[0:11],'k--')
    legend = ax.legend(loc='upper right')
    plt.xlabel('Mode')
    plt.ylabel('Magnitude')
    ax.set_xlim([1,10])
    ax.set_ylim([-4,4])
    fig.savefig('Amp_Phase_data.row'+str(currentrow)+'.jpg')

    print " >>   Fourier Amplitude - Phase Data for row  " + str(currentrow)+ "   saved "
    print " "


# #show(block=False)
# #plt.show()                                        # Uncomment if User want to Manually close Figures and then continue


# # Read no of blades from 3dbgbinput.2.dat file
    filename= curr_3dbgb_file        
    f = open(filename, "r")
    lineread = f.readlines()
    for num, line in enumerate(lineread, 1):
        linelist = line.split()
        if num == 6:
            nblades = int(linelist[0])
    f.close





# # >>>>>>>>>>>>
    fmodes = input(' >   Enter no. of Fourier Modes for in_Beta (inlet angle):    ')
    block=[]
    if fmodes == 0 :
        block = [0.0000000000000000]*6 
    else:
        for i in range(1,fmodes+1):
            a=[amp[i],phase[i]]
            block.append(a)

    block1 = str(block).translate(string.maketrans('', ''), '[]\'') #strip the [] to print

# # use these user inputs for making new array like 'block' >>

    delta_theta_fmodes = input(' >   Enter no. of Fourier Modes for delta_theta          :    ')
    block_dt = []
    if delta_theta_fmodes == 0:
        block_dt = [0.0000000000000000]*6 
    else:
        for i in range(1,delta_theta_fmodes+1):
            a2=[amp[i],phase[i]]
            block_dt.append(a2)
    block1_dt = str(block_dt).translate(string.maketrans('', ''), '[]\'') #strip the [] to print


    true_lean_fmodes = input(' >   Enter no. of Fourier Modes for true lean            :    ')
    block_tl =[]
    if true_lean_fmodes == 0 :
        block_tl = [0.0000000000000000]*6 
    else:
        for i in range(1,true_lean_fmodes+1):
            a3=[amp[i],phase[i]]
            block_tl.append(a3)
    block1_tl = str(block_tl).translate(string.maketrans('', ''), '[]\'')



    true_sweep_fmodes = input(' >   Enter no. of Fourier Modes for true sweep           :    ')
    block_ts = []
    if true_sweep_fmodes == 0:
        block_ts = [0.0000000000000000]*6
    else:
        for i in range(1,true_sweep_fmodes+1):
            a4=[amp[i],phase[i]]
            block_ts.append(a4)
    block1_ts = str(block_ts).translate(string.maketrans('', ''), '[]\'')
# #


# #>>>>>>>>>>>>>>
# # Write the naxinput file
    spanpoints =3           #except hub
    f1 = open("naxinput."+str(currentrow)+".dat", "w")
    f1.write("NAX v0.2 - input file"+"\n")
    f1.write("Casename: "+"\n")
    f1.write("nasafan "+"\n")
    f1.write("Bladerow:"+"\n")
    f1.write(str(currentrow)+"\n")
    f1.write("  "+"\n")
    f1.write("  "+"\n")

# # in-Beta
    f1.write("in_Beta Span Control Points"+"     "+ "Fourier Modes (Magnitude , Phase)"+"\n")
    f1.write((" "+('%.f'%(spanpoints+1))  + "                                     "+('%.f'%fmodes))+"\n")   #fmodes
    for row in range(spanpoints+1):
        f1.write(('%.4f'%(row*(1.0/spanpoints)))+"    "+(block1)+"\n")

    f1.write("  "+"\n")

    # for delta_theta
    f1.write("delta_theta Span Control Points"+"     "+ "Fourier Modes(Magnitude , Phase)"+"\n")
    f1.write((" "+('%.f'%(spanpoints+1))  + "                                   "+('%.f'%delta_theta_fmodes))+"\n")      #delta_theta_modes
    for row in range(spanpoints+1):
        f1.write(('%.4f'%(row*(1.0/spanpoints)))+"    "+(block1_dt)+"\n")

# # for true_lean
    f1.write("  "+"\n")
    f1.write("true_lean Span Control Points"+"     "+ "Fourier Modes(Magnitude , Phase)"+"\n")
    f1.write((" "+('%.f'%(spanpoints+1))  + "                                    "+('%.f'%true_lean_fmodes))+"\n") #true_lean_modes
    for row in range(spanpoints+1):
        f1.write(('%.4f'%(row*(1.0/spanpoints)))+"    "+(block1_tl)+"\n")

# # for true_sweep
    f1.write("  "+"\n")
    f1.write("true_sweep Span Control Points"+"     "+ "Fourier Modes(Magnitude , Phase)"+"\n")
    f1.write((" "+('%.f'%(spanpoints+1))  + "                                     "+('%.f'%true_sweep_fmodes))+"\n")  #true_sweep_modes
    for row in range(spanpoints+1):
        f1.write(('%.4f'%(row*(1.0/spanpoints)))+"    "+(block1_ts)+"\n")

    f1.close

    print " >>   Input file for row  "+str(currentrow)+" Written "
    #print " Pre-processing Complete"
    print "     -----   #   ----------   #   -----"
    
exit(0)


# used to work up with 'inputs' directory ! delete if used all inputs in same directory 
os.chdir("../")