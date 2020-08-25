#!/usr/local/bin/python3

# NAX v0.3 Aero-Design systems
# Python v3.5 Pre-processing script
# Python v2.7 was used till NAX v0.2 
# Calculates the FFT of distortion profile &
# creates the input file for further process

# ----------------------------------------------------
# Sandeep Kumar , DEC 2K18
# GTSL , Dept of Aerospace Engg, University of Cincinnati
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


# Check for validity of Run -'distortion profile' file(s) should exist
# Read from naxinfo.dat file 
# user input for non-axisymmetric rows in array , (naxrow)


os.chdir("./inputs")  

print (" ")
print ("     Checking Inputs validity - ")
print (" ")
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



# Independent if condition - for definiting any blade row(s) as 0 - see naxinfo 
if naxrow =="0":
    totalnaxrows = 0 
else:
    totalnaxrows = len(naxrow.split(','))

if axirow =="0":
    totalaxirows = 0
else:
    totalaxirows = len(axirow.split(','))


#print ("     ")
print ("     Total non-axisymmetric rows :" , totalnaxrows)

print ("     Total axisymmetric rows     :" , totalaxirows)
print ("     --------------------------------------------")

for j in range(totalnaxrows):

    currentrow = naxrow.split(',')[j]
    curr_dist_file = "distortion.row"+str(currentrow) +".csv"
    curr_3dbgb_file = "3dbgbinput."+str(currentrow) +".dat"

    if any(File.startswith("distortion.row"+str(currentrow)) for File in os.listdir(".")):
        print ( "     Distortion profile  for  row " +str(currentrow)+"  Exist ")
    else:
        print( "      ERROR : Distortion profile files not found")
        print( "      Execution Terminated ! ")
        exit(1)

    if any(File.startswith("3dbgbinput."+str(currentrow)) for File in os.listdir(".")):
        print ( "     tblade3/3dbgb Input files for  row " +str(currentrow)+"  Exist ")
        print ("    ")
    else:
        print( "       ERROR : tblade3/3dbgb Input files not found")
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

# #Calculate FFT
    a = fft(alpha)
    amp = np.abs(a)/(n/2)
    phase = np.angle(a)


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
#    fig.savefig('Amp_Phase_data.row'+str(currentrow)+'.jpg')

    print (" >>   Fourier Amplitude - Phase Data for row  " + str(currentrow)+ "   saved ")
    print (" ")


# #show(block=False)
# #plt.show()                               # Uncomment if User want to Manually close Figures and then continue


# # Read no of blades from 3dbgbinput.#.dat file
    filename= curr_3dbgb_file        
    f = open(filename, "r")
    lineread = f.readlines()
    for num, line in enumerate(lineread, 1):
        linelist = line.split()
        if num == 6:
            nblades = int(linelist[0])
    f.close

# >>>>>>>>>>>>
# Variables for naxinput files -
# SWEEP
    cp_sweep =     int(input(' >   Enter no. of Span-Control points for Sweep (min=4)           :   '))
    fmodes_sweep = int(input(' >   Enter no. of Fourier Modes for Sweep                         :   '))
    block_sw=[]
    if fmodes_sweep == 0 :
        block_sw = [0.0000000000000000]*6 
    else:
        for i in range(1,fmodes_sweep+1):
            a1=(', '.join(map(str, [amp[i],phase[i]])))
            block_sw.append(a1)

    block_sw=(', '.join(map(str, block_sw)))

# LEAN
    cp_lean =     int(input(' >   Enter no. of Span-Control points for Lean (min=4)            :   '))
    fmodes_lean = int(input(' >   Enter no. of Fourier Modes for Lean                          :   '))
    block_ln=[]
    if fmodes_lean == 0 :
        block_ln = [0.0000000000000000]*6 
    else:
        for i in range(1,fmodes_lean+1):
            a2=(', '.join(map(str, [amp[i],phase[i]])))
            block_ln.append(a2)

    block_ln=(', '.join(map(str, block_ln)))

# IN_BETA
    cp_inbeta =     int(input(' >   Enter no. of Span-Control points for InBeta (min=4)          :   '))
    fmodes_inbeta = int(input(' >   Enter no. of Fourier Modes for In_beta                       :   '))
    block_ib=[]
    if fmodes_inbeta == 0 :
        block_ib = [0.0000000000000000]*6 
    else:
        for i in range(1,fmodes_inbeta+1):
            a3=(', '.join(map(str, [amp[i],phase[i]])))
            block_ib.append(a3)

    block_ib=(', '.join(map(str, block_ib)))
    
# OUT_BETA
    cp_outbeta =     int(input(' >   Enter no. of Span-Control points for OutBeta (min=4)         :   '))
    fmodes_outbeta = int(input(' >   Enter no. of Fourier Modes for Out_beta                      :   '))
    block_ob=[]
    if fmodes_outbeta == 0 :
        block_ob = [0.0000000000000000]*6 
    else:
        for i in range(1,fmodes_outbeta+1):
            a4=(', '.join(map(str, [amp[i],phase[i]])))
            block_ob.append(a4)

    block_ob=(', '.join(map(str, block_ob)))

# CHORD_MULTIPLIER
    cp_cm =     int(input(' >   Enter no. of Span-Control points for chord_multiplier (min=4):   '))
    fmodes_cm = int(input(' >   Enter no. of Fourier Modes for chord_multiplier              :   '))
    block_cm=[]
    if fmodes_cm == 0 :
        block_cm = [0.0000000000000000]*6 
    else:
        for i in range(1,fmodes_cm+1):
            a5=(', '.join(map(str, [amp[i],phase[i]])))
            block_cm.append(a5)

    block_cm=(', '.join(map(str, block_cm)))
 
# TM/C
    cp_tmc =     int(input(' >   Enter no. of Span-Control points for tm/c (min=4)            :   '))
    fmodes_tmc = int(input(' >   Enter no. of Fourier Modes for tm/c                          :   '))
    block_tmc=[]
    if fmodes_tmc == 0 :
        block_tmc = [0.0000000000000000]*6 
    else:
        for i in range(1,fmodes_tmc+1):
            a6=(', '.join(map(str, [amp[i],phase[i]])))
            block_tmc.append(a6)

    block_tmc=(', '.join(map(str, block_tmc)))

    print (" --------------------------------------------------- ")

# # Write the naxinput file
    f1 = open("naxinput."+str(currentrow)+".dat", "w")
    f1.write("NAX v0.3 - input file"+"\n")
    f1.write("Casename: "+"\n")
    f1.write("nax_case "+"\n")
    f1.write("Bladerow:"+"\n")
    f1.write(str(currentrow)+"\n")
    f1.write("  "+"\n")
    f1.write("  "+"\n")

	# for Sweep
    f1.write("Sweep Span Control Points"+"     "+ "Fourier Modes (Magnitude , Phase)"+"\n")
    f1.write(("    "+('%.f'%(cp_sweep))  + "                         "+('%.f'%fmodes_sweep))+"\n")   #fmodes
    for row in range(cp_sweep):
        f1.write(('%.4f'%(row*(1.0/(cp_sweep-1))))+"    "+(block_sw)+"\n")

    f1.write("  "+"\n")

	# for Lean
    f1.write("Lean Span Control Points"+"     "+ "Fourier Modes (Magnitude , Phase)"+"\n")
    f1.write(("    "+('%.f'%(cp_lean))  + "                         "+('%.f'%fmodes_lean))+"\n")   #fmodes
    for row in range(cp_lean):
        f1.write(('%.4f'%(row*(1.0/(cp_lean-1))))+"    "+(block_ln)+"\n")

    f1.write("  "+"\n")
 
 	# for in_beta
    f1.write("In_beta Span Control Points"+"     "+ "Fourier Modes (Magnitude , Phase)"+"\n")
    f1.write(("    "+('%.f'%(cp_inbeta))  + "                         "+('%.f'%fmodes_inbeta))+"\n")   #fmodes
    for row in range(cp_inbeta):
        f1.write(('%.4f'%(row*(1.0/(cp_inbeta-1))))+"    "+(block_ib)+"\n")

    f1.write("  "+"\n")   
    
 	# for out_beta
    f1.write("Out_beta Span Control Points"+"     "+ "Fourier Modes (Magnitude , Phase)"+"\n")
    f1.write(("    "+('%.f'%(cp_outbeta))  + "                         "+('%.f'%fmodes_outbeta))+"\n")   #fmodes
    for row in range(cp_outbeta):
        f1.write(('%.4f'%(row*(1.0/(cp_outbeta-1))))+"    "+(block_ob)+"\n")

    f1.write("  "+"\n") 

 	# for chord_multiplier
    f1.write("Chord_multiplier Span Control Points"+"     "+ "Fourier Modes (Magnitude , Phase)"+"\n")
    f1.write(("    "+('%.f'%(cp_cm))  + "                             "+('%.f'%fmodes_cm))+"\n")   #fmodes
    for row in range(cp_cm):
        f1.write(('%.4f'%(row*(1.0/(cp_cm-1))))+"    "+(block_cm)+"\n")

    f1.write("  "+"\n") 

 	# for tm/c
    f1.write("tm/c Span Control Points"+"     "+ "Fourier Modes (Magnitude , Phase)"+"\n")
    f1.write(("    "+('%.f'%(cp_tmc))  + "                             "+('%.f'%fmodes_tmc))+"\n")   #fmodes
    for row in range(cp_tmc):
        f1.write(('%.4f'%(row*(1.0/(cp_tmc-1))))+"    "+(block_tmc)+"\n")

    f1.write("  "+"\n") 

    f1.close

    print (" >>   Input file for row  "+str(currentrow)+" Written ")

    print ("---------------------------------------------------")
    
exit(0)

# used to work up when 'inputs' directory exist ! delete ( change dir) in case all inputs are in same directory 
os.chdir("../")
