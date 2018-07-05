#!/usr/bin/env python

# NAX v0.2 Aero-Design Systems
# Python script (v2.7)to produce Non-Axisymmetric designs
# Support script that reads 3dbgbinput files genearted from TAXI
# Reads input data from naxinput.<row#>.dat for process
# Produces Individual blade files for each row
# makes directory for all the blades separately
# This script may contain few specific values for NASA BLI fan case
# Change the parsing property as per design requirements
# here only incidence and deviation angles are changed
# Fourier coeff used to induce perturbations in blades
# Other properties can also be parsed and used
# >> -------------------------------------------------------------
# Running from terminal " python nonaxisym_v0.2.py
# spancontrol input file can be downloaded from GTSL ( T-Blade3) website
# >> --------------------------------------------------------------
# Sandeep Kumar , Nov 2K17
# GTSL , Dept of Aerospace Engg, University of Cincinnati
# --------------------------------------------------------
# ------------------------------------------------------------


# Library Imports
import os , math
import glob
import shutil

# ------------------------------------------------------------

os.chdir("./inputs")  

# ------------------------------------------------------------
# check if 3dbgbinput files are present in current directory
# else exit the script 
# check if required files are present in current directory
# else exit the script


print " "
print "     Checking Inputs Validity -"

if any(File.startswith("naxinfo") for File in os.listdir(".")):
    print (" ")
    print ( "     Nax-info file Exist ")
else:
    print( "    ERROR : nax-info files not found")
    print( "    Execution Terminated ! ")
    exit(1)
if any(File.startswith("naxinput") for File in os.listdir(".")):
    print ( "     nax-input files Exist ")
else:
    print( "    ERROR : nax-input files not found")
    print( "    Execution Terminated ! ")
    exit(1)

if any(File.startswith("3dbgbinput") for File in os.listdir(".")):
    print ( "     3dbgb input files Exist ")
else:
    print( "    ERROR : 3dbgbinput files not found")
    print( "    Execution Terminated ! ")
    exit(1)

if any(File.startswith("spancontrolinputs") for File in os.listdir(".")):
    print ( "     spancontrol input files Exist ")
else:
    print( "    ERROR : spancontrol input files not found")
    print( "    Execution Terminated ! ")
    exit(1)


#Function definition to calculate file length
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1



#-------------------------------------------------------------
# Declare axi and non-axi blade rows
# Can also be user inputs for Axi / Non-Axi rows and store in array
with open("naxinfo.dat") as info:
    length=file_len("naxinfo.dat")
    f3 = open("naxinfo.dat","r")
    lineread3 = f3.readlines()

for num,line in enumerate(lineread3,1):
    linelist3 = line.split()

    if num == 15:
        a_row = (linelist3[1])
    if num == 16:
        n_row = (linelist3[1])

if n_row == "NONE":
    n_row = []

totalaxirows = len(a_row.split(','))
totalnaxrows = len(n_row.split(','))

all_rows = a_row + ',' + n_row

# counter for number of files
axicount = 0
nonaxicount = 0


# ------------------------------------------------------------
# No of input file , reads max 50 blade rows
#total = len(glob.glob("3dbgbinput.[0-50].dat"))
#naxtotal = len(glob.glob("naxinput.[0-50].dat"))

#or 
total = totalaxirows + totalnaxrows

print '     Total nax-input files :', totalnaxrows
print '     Total 3dbgb input files :', total

# ------------------------------------------------------------
# ------------------------------------------------------------

for row in range(total):                        

    current_row = all_rows.split(',')[row]
    os.makedirs('row'+current_row)

    curr_3dbgbfile = "3dbgbinput." + current_row +".dat"
    curr_spanfile  = "spancontrolinputs."+ current_row + ".dat"

    # print " Curr Row :" , current_row
    # print " Curr 3dbgb :", curr_3dbgbfile
    # print " Curr span :", curr_spanfile 

    with open(curr_3dbgbfile) as f3dbgb:
        file_length = file_len(curr_3dbgbfile)
        f = open(curr_3dbgbfile, "r")
        lineread = f.readlines()
    
    with open(curr_spanfile) as fspanc:
        file_length1 = file_len(curr_spanfile)
        fspan = open(curr_spanfile, "r")
        lineread2 = fspan.readlines()

    #

    for num, line in enumerate(lineread, 1):    # reading default values
        linelist = line.split()

        if num == 6:
            blades = int(linelist[0])     # no of blades in row

        if num == 8:
            bsf = float(linelist[0]) # Blade Scaling Factor

        # if num == 8:
        #     blade_position = float(linelist[1]) # the postion of blade around the annulus in Degree
        
        if num == 97:
            span1_sweep = (linelist[2])         # True sweep values
        if num == 98:
            span2_sweep = (linelist[2])
        if num == 99:
            span3_sweep = (linelist[2])
        if num == 100:
            span4_sweep = (linelist[2])

        # Offest of blades/ positions - Tangential/Axisymmetric Lean - Local lean of blade 

        if num == 105:
            theta1 = (linelist[1])
        if num == 106:
            theta2 = (linelist[1])
        if num == 107:
            theta3 = (linelist[1])
        if num == 108:
            theta4 = (linelist[1])

        # for true lean
        if num == 105:
            span1_lean = (linelist[2])
        if num == 106:
            span2_lean = (linelist[2])
        if num == 107:
            span3_lean = (linelist[2])
        if num == 108:
            span4_lean = (linelist[2])

        # Incidence / In_beta angles
        if num == 113:
            span1_in_beta = (linelist[1])
        if num == 114:
            span2_in_beta = (linelist[1])
        if num == 115:
            span3_in_beta = (linelist[1])
        if num == 116:
            span4_in_beta = (linelist[1])

        # Deviation / Out_beta angles
        if num == 121:
            span1_out_beta = (linelist[1])
        if num == 122:
            span2_out_beta = (linelist[1])
        if num == 123:
            span3_out_beta = (linelist[1])
        if num == 124:
            span4_out_beta = (linelist[1])
            
            

        # FOR AXI SYM ROW
            if current_row in a_row[:]:

                os.chdir("./"'row'+ current_row)
                for naxdir in range(1,2):
                    os.makedirs(current_row +'.'+'axi1')
                
                blade_position = 0.0            # Blade position in Degree around annulus
                
                span1_dtheta_Perturbation = 0.0     # Perturbation Offsets ( like a Local Lean of blade)
                span2_dtheta_Perturbation = 0.0
                span3_dtheta_Perturbation = 0.0
                span4_dtheta_Perturbation = 0.0
                
                span1_inbeta_Perturbation = 0.0      #InBeta Angles
                span2_inbeta_Perturbation = 0.0
                span3_inbeta_Perturbation = 0.0
                span4_inbeta_Perturbation = 0.0

                span1_outbeta_Perturbation = 0.0      #OutBeta Angles
                span2_outbeta_Perturbation = 0.0
                span3_outbeta_Perturbation = 0.0
                span4_outbeta_Perturbation = 0.0
                
                span1_lean_Perturbation = 0.0       #True Lean
                span2_lean_Perturbation = 0.0
                span3_lean_Perturbation = 0.0
                span4_lean_Perturbation = 0.0
                
                span1_sweep_Perturbation = 0.0      #True Sweep
                span2_sweep_Perturbation = 0.0
                span3_sweep_Perturbation = 0.0
                span4_sweep_Perturbation = 0.0
                
                nax_tsweep1 = float(span1_sweep) + float(span1_sweep_Perturbation)
                nax_tsweep2 = float(span2_sweep) + float(span2_sweep_Perturbation)
                nax_tsweep3 = float(span3_sweep) + float(span3_sweep_Perturbation)
                nax_tsweep4 = float(span4_sweep) + float(span4_sweep_Perturbation)
                
                nax_theta_offset1 = float(theta1) + float(span1_dtheta_Perturbation)
                nax_theta_offset2 = float(theta2) + float(span2_dtheta_Perturbation)
                nax_theta_offset3 = float(theta3) + float(span3_dtheta_Perturbation)
                nax_theta_offset4 = float(theta4) + float(span4_dtheta_Perturbation)
                
                nax_tlean1 = float(span1_lean) + float(span1_lean_Perturbation)
                nax_tlean2 = float(span2_lean) + float(span2_lean_Perturbation)
                nax_tlean3 = float(span3_lean) + float(span3_lean_Perturbation)
                nax_tlean4 = float(span4_lean) + float(span4_lean_Perturbation)
                
                naxspan1_in_beta = float(span1_in_beta) + float(span1_inbeta_Perturbation)
                naxspan2_in_beta = float(span2_in_beta) + float(span2_inbeta_Perturbation)
                naxspan3_in_beta = float(span3_in_beta) + float(span3_inbeta_Perturbation)
                naxspan4_in_beta = float(span4_in_beta) + float(span4_inbeta_Perturbation)
                
                # following #Commented for 0 out angles
                naxspan1_out_beta = float(span1_out_beta) + float(span1_outbeta_Perturbation)
                naxspan2_out_beta = float(span2_out_beta) + float(span2_outbeta_Perturbation)
                naxspan3_out_beta = float(span3_out_beta) + float(span3_outbeta_Perturbation)
                naxspan4_out_beta = float(span4_out_beta) + float(span4_outbeta_Perturbation)
                
                os.chdir(current_row +'.'+'axi1')
                
#           Write new 3dbgb input file

                axicount = axicount + 1

                #filename_nax = "3dbgbinput."+ current_row + ".axi1" + ".dat"
                filename_nax = "3dbgbinput."+ current_row + "axi1" + ".dat"
                
                f3 = open(str(filename_nax), "w")
        
                for i in range(0,2):
                    f3.write(lineread[i])
            #   change the blade row # as bladerow#.blade num e.g. 1.2 in the file
            #
                m=3
                f3.write(('NAX Design Systems : Blade row#  -  Blade #')  + "\n")
                #
                l=4
                f3.write("          ")
                f3.write(( '%d'%int(current_row) + '       ' + '%d'%int(naxdir))+ "\n")
                #
                m=5
                f3.write(('Number of blades in this row:')  + "\n")
                #
                l=6
                f3.write("          ")
                f3.write(( '%d'%int(blades) )+ "\n")
                #
                m=7
                f3.write((' Blade Scaling factor (mm):      Blade Postion (Degree)')  + "\n")
                #
                l=8
                f3.write("          ")
                f3.write(( '%6f'%float(bsf) + '       ' + '%6f'%float(blade_position) )+ "\n")
                #


                for i in range(8,96):
                    f3.write(lineread[i])
                    #
                d1=96
                f3.write("  ")
                f3.write(lineread[d1].split()[0] + "            ")
                f3.write(lineread[d1].split()[1]  + "           ")
                f3.write(('%.6f'%nax_tsweep1) + " \n")
                d2=97
                f3.write("  ")
                f3.write(lineread[d2].split()[0] + "         ")
                f3.write(lineread[d2].split()[1]  + "       ")
                f3.write(('%.6f'%nax_tsweep2) + " \n")
                d3=98
                f3.write("  ")
                f3.write(lineread[d3].split()[0] + "            ")
                f3.write(lineread[d3].split()[1]  + "       ")
                f3.write(('%.6f'%nax_tsweep3) + " \n")
                d4=99
                f3.write("  ")
                f3.write(lineread[d4].split()[0] + "            ")
                f3.write(lineread[d4].split()[1]  + "       ")
                f3.write(('%.6f'%nax_tsweep4) + " \n")
                    #
                for i in range(100,104):
                    f3.write(lineread[i])
                    
                t1=104
                f3.write("  ")
                f3.write(lineread[t1].split()[0] + "            ")
                f3.write(('%.6f'%nax_theta_offset1)  + "               ")
                f3.write(('%.6f'%nax_tlean1) + " \n")
                t2=105
                f3.write(" ")
                f3.write(lineread[t2].split()[0] + "            ")
                f3.write(('%.6f'%nax_theta_offset2)  + "               ")
                f3.write(('%.6f'%nax_tlean2) + " \n")
                t3=106
                f3.write(" ")
                f3.write(lineread[t3].split()[0] + "            ")
                f3.write(('%.6f'%nax_theta_offset3)  +  "               ")
                f3.write(('%.6f'%nax_tlean3) + " \n")
                t4=107
                f3.write("  ")
                f3.write(lineread[t4].split()[0] + "            ")
                f3.write(('%.6f'%nax_theta_offset4) +  "               ")
                f3.write(('%.6f'%nax_tlean4) + " \n")
                #
                for i in range(108,112):
                    f3.write(lineread[i])
                #
                p1=112
                f3.write("  ")
                f3.write(lineread[p1].split()[0] + "            ")
                f3.write(('%.6f'%naxspan1_in_beta)  + "\n")
                p2=113
                f3.write(" ")
                f3.write(lineread[p2].split()[0] + "            ")
                f3.write(('%.6f'%naxspan2_in_beta)  + "\n")
                p3=114
                f3.write(" ")
                f3.write(lineread[p3].split()[0] + "            ")
                f3.write(('%.6f'%naxspan3_in_beta)  +  "\n")
                p4=115
                f3.write("  ")
                f3.write(lineread[p4].split()[0] + "            ")
                f3.write(('%.6f'%naxspan4_in_beta) +  "\n")
                    #
                for i in range(116,120):
                    f3.write(lineread[i])
                    #
                q1=120
                f3.write("  ")
                f3.write(lineread[q1].split()[0] + "            ")
                f3.write(('%.6f'%naxspan1_out_beta)  + "\n")
                q2=121
                f3.write(" ")
                f3.write(lineread[q2].split()[0] + "            ")
                f3.write(('%.6f'%naxspan2_out_beta)  + "\n")
                q3=122
                f3.write(" ")
                f3.write(lineread[q3].split()[0] + "            ")
                f3.write(('%.6f'%naxspan3_out_beta)  +  "\n")
                q4=123
                f3.write("  ")
                f3.write(lineread[q4].split()[0] + "            ")
                f3.write(('%.6f'%naxspan4_out_beta) +  "\n")
                    #
                for i in range(124,file_length):
                    f3.write(lineread[i])
                f3.close
                
                
                ## Write spancontrol file
                # filename_span = "spancontrolinputs."+ current_row + ".axi1" + ".dat"
                filename_span = "spancontrolinputs."+ current_row + "axi1" + ".dat"
                f4 = open(str(filename_span), "w")
                for s1 in range(0,file_length1):
                    f4.write(lineread2[s1])

                os.chdir("../../")
                
    # FOR NON-AXI ROW
            

            elif current_row in n_row[:]:

                # ROW SPECIFIC OPERATION  <<<<<<<<<<<<<<<<<<<<<<<<<
                # Read the naxinput file 
                with open("naxinput."+current_row+".dat") as finput:
                    inputs = finput.readlines()
                for num1,line1 in enumerate(inputs,1):
                    seq = line1.split()
                     
            #read span-control points and fourier modes
                    if num1 == 9:
                        inbeta_nspanpoints = int(seq[0])  # used for all properties
                        inbeta_nfmodes = int(seq[1])      # used for all properties
                        
            #read magnitude and phase for angles (in beta)
                    if num1 == 10:
                        mag_span1=seq[1::2]
                        phase_span1=seq[2::2]
                        
                    if num1 == 11:
                        mag_span2=seq[1::2]
                        phase_span2=seq[2::2]
                    if num1 == 12:
                        mag_span3=seq[1::2]
                        phase_span3=seq[2::2]
                    if num1 == 13:
                        mag_span4=seq[1::2]
                        phase_span4=seq[2::2]
            # delta_theta
                    if num1 == 16:
                        dtheta_nspanpoints = int(seq[0])
                        dtheta_nfmodes = int(seq[1])
                        
                    if num1 == 17:
                        dtheta_magspan1=seq[1::2]
                        dtheta_phspan1=seq[2::2]
                        
                    if num1 == 18:
                        dtheta_magspan2=seq[1::2]
                        dtheta_phspan2=seq[2::2]
                    if num1 == 19:
                        dtheta_magspan3=seq[1::2]
                        dtheta_phspan3=seq[2::2]
                    if num1 == 20:
                        dtheta_magspan4=seq[1::2]
                        dtheta_phspan4=seq[2::2]
            # true_lean
                    if num1 == 23:
                        tlean_nspanpoints = int(seq[0])
                        tlean_nfmodes = int(seq[1])
                        
                    if num1 == 24:
                        tlean_magspan1=seq[1::2]
                        tlean_phspan1=seq[2::2]
                    if num1 == 25:
                        tlean_magspan2=seq[1::2]
                        tlean_phspan2=seq[2::2]
                    if num1 == 26:
                        tlean_magspan3=seq[1::2]
                        tlean_phspan3=seq[2::2]
                    if num1 == 27:
                        tlean_magspan4=seq[1::2]
                        tlean_phspan4=seq[2::2]
                # true_sweep
                    if num1 == 30:
                        tsweep_nspanpoints = int(seq[0])
                        tsweep_nfmodes = int(seq[1])
                        
                    if num1 == 31:
                        tsweep_magspan1=seq[1::2]
                        tsweep_phspan1=seq[2::2]
                    if num1 == 32:
                        tsweep_magspan2=seq[1::2]
                        tsweep_phspan2=seq[2::2]
                    if num1 == 33:
                        tsweep_magspan3=seq[1::2]
                        tsweep_phspan3=seq[2::2]
                    if num1 == 34:
                        tsweep_magspan4=seq[1::2]
                        tsweep_phspan4=seq[2::2]
                        
                        os.chdir("./"'row'+ current_row)
                # BLADE SPECIFIC OPERATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        for naxdir in range(1,blades+1):
                            os.makedirs(current_row +'.'+'nax'+'%d'%naxdir)
                   #        
                            # Initialization 
                            blade_position = 0.0                #Blade Postion 
                            blade_location = 0.0 
                   #
                            span1_dtheta_Perturbation = 0.0     #Perturbation Offsets
                            span2_dtheta_Perturbation = 0.0
                            span3_dtheta_Perturbation = 0.0
                            span4_dtheta_Perturbation = 0.0
                            
                            span1_inbeta_Perturbation = 0.0            #InBeta Angles
                            span2_inbeta_Perturbation = 0.0
                            span3_inbeta_Perturbation = 0.0
                            span4_inbeta_Perturbation = 0.0
                            
                            span1_outbeta_Perturbation = 0.0            #OutBeta Angles
                            span2_outbeta_Perturbation = 0.0
                            span3_outbeta_Perturbation = 0.0
                            span4_outbeta_Perturbation = 0.0

                            span1_lean_Perturbation = 0.0       #Lean
                            span2_lean_Perturbation = 0.0
                            span3_lean_Perturbation = 0.0
                            span4_lean_Perturbation = 0.0
                            
                            span1_sweep_Perturbation = 0.0      #Sweep
                            span2_sweep_Perturbation = 0.0
                            span3_sweep_Perturbation = 0.0
                            span4_sweep_Perturbation = 0.0


                            #
                            blade_position = float(naxdir * float(360.0/(blades)))      # [Degree ]
                            blade_location = float(naxdir * float((2 * math.pi)/(blades)))  # [Radians] value of blade position


                            for nft in range(dtheta_nfmodes):
                                
                                span1_dtheta_perturb = float(dtheta_magspan1[nft][0:-1])*(math.sin((nft+1)*blade_location + float(dtheta_phspan1[nft][0:-1])) )
                                span2_dtheta_perturb = float(dtheta_magspan2[nft][0:-1])*(math.sin((nft+1)*blade_location + float(dtheta_phspan2[nft][0:-1])) )
                                span3_dtheta_perturb = float(dtheta_magspan3[nft][0:-1])*(math.sin((nft+1)*blade_location + float(dtheta_phspan3[nft][0:-1])) )
                                span4_dtheta_perturb = float(dtheta_magspan4[nft][0:-1])*(math.sin((nft+1)*blade_location + float(dtheta_phspan4[nft][0:-1])) )
                                
                                span1_dtheta_Perturbation = span1_dtheta_Perturbation + span1_dtheta_perturb
                                span2_dtheta_Perturbation = span2_dtheta_Perturbation + span2_dtheta_perturb
                                span3_dtheta_Perturbation = span3_dtheta_Perturbation + span3_dtheta_perturb
                                span4_dtheta_Perturbation = span4_dtheta_Perturbation + span4_dtheta_perturb
                                

                            for nf in range(inbeta_nfmodes):
        # for Angles - in beta
                                span1_perturb = float(mag_span1[nf][0:-1])*(math.sin((nf+1)*blade_location + float(phase_span1[nf][0:-1])) )
                                span2_perturb = float(mag_span2[nf][0:-1])*(math.sin((nf+1)*blade_location + float(phase_span2[nf][0:-1])) )
                                span3_perturb = float(mag_span3[nf][0:-1])*(math.sin((nf+1)*blade_location + float(phase_span3[nf][0:-1])) )
                                span4_perturb = float(mag_span4[nf][0:-1])*(math.sin((nf+1)*blade_location + float(phase_span4[nf][0:-1])) )
        
                                span1_inbeta_Perturbation = span1_inbeta_Perturbation + span1_perturb
                                span2_inbeta_Perturbation = span2_inbeta_Perturbation + span2_perturb
                                span3_inbeta_Perturbation = span3_inbeta_Perturbation + span3_perturb
                                span4_inbeta_Perturbation = span4_inbeta_Perturbation + span4_perturb
                                
                            
                            
        # IMPORTANT : Calculations for True_lean / true_sweep .
                            for nf in range(tlean_nfmodes):
        # for true lean
                                span1_lean_perturb = float(tlean_magspan1[nf][0:-1])*(math.sin((nf+1)*blade_location + float(tlean_phspan1[nf][0:-1])) )
                                span2_lean_perturb = float(tlean_magspan2[nf][0:-1])*(math.sin((nf+1)*blade_location + float(tlean_phspan2[nf][0:-1])) )
                                span3_lean_perturb = float(tlean_magspan3[nf][0:-1])*(math.sin((nf+1)*blade_location + float(tlean_phspan3[nf][0:-1])) )
                                span4_lean_perturb = float(tlean_magspan4[nf][0:-1])*(math.sin((nf+1)*blade_location + float(tlean_phspan4[nf][0:-1])) )
        
                                span1_lean_Perturbation = span1_lean_Perturbation + span1_lean_perturb
                                span2_lean_Perturbation = span2_lean_Perturbation + span2_lean_perturb
                                span3_lean_Perturbation = span3_lean_Perturbation + span3_lean_perturb
                                span4_lean_Perturbation = span4_lean_Perturbation + span4_lean_perturb
                                
                                
                            for nf in range(tsweep_nfmodes):
        # for true sweep
                                span1_sweep_perturb = float(tsweep_magspan1[nf][0:-1])*(math.sin((nf+1)*blade_location + float(tsweep_phspan1[nf][0:-1])) )
                                span2_sweep_perturb = float(tsweep_magspan2[nf][0:-1])*(math.sin((nf+1)*blade_location + float(tsweep_phspan2[nf][0:-1])) )
                                span3_sweep_perturb = float(tsweep_magspan3[nf][0:-1])*(math.sin((nf+1)*blade_location + float(tsweep_phspan3[nf][0:-1])) )
                                span4_sweep_perturb = float(tsweep_magspan4[nf][0:-1])*(math.sin((nf+1)*blade_location + float(tsweep_phspan4[nf][0:-1])) )
        
                                span1_sweep_Perturbation = span1_sweep_Perturbation + span1_sweep_perturb
                                span2_sweep_Perturbation = span2_sweep_Perturbation + span2_sweep_perturb
                                span3_sweep_Perturbation = span3_sweep_Perturbation + span3_sweep_perturb
                                span4_sweep_Perturbation = span4_sweep_Perturbation + span4_sweep_perturb
                                
#                                
                                
    # new inlet angles : for OGV 
                            naxspan1_in_beta = float(span1_in_beta) + float(span1_inbeta_Perturbation)
                            naxspan2_in_beta = float(span2_in_beta) + float(span2_inbeta_Perturbation)
                            naxspan3_in_beta = float(span3_in_beta) + float(span3_inbeta_Perturbation)
                            naxspan4_in_beta = float(span4_in_beta) + float(span4_inbeta_Perturbation)
                            
                            
    # new outlet angles : For OGV
                            naxspan1_out_beta = float(span1_out_beta) + float(span1_outbeta_Perturbation)            # 0 out beta angles
                            naxspan2_out_beta = float(span2_out_beta) + float(span2_outbeta_Perturbation)
                            naxspan3_out_beta = float(span3_out_beta) + float(span3_outbeta_Perturbation)
                            naxspan4_out_beta = float(span4_out_beta) + float(span4_outbeta_Perturbation)
                            
    # new offset of 4 control points
                            nax_offset1 = float(theta1) + float(span1_dtheta_Perturbation)
                            nax_offset2 = float(theta2) + float(span2_dtheta_Perturbation)
                            nax_offset3 = float(theta3) + float(span3_dtheta_Perturbation)
                            nax_offset4 = float(theta4) + float(span4_dtheta_Perturbation)
                            
    # new true lean
                            nax_tlean1 = float(span1_lean) + float(span1_lean_Perturbation)
                            nax_tlean2 = float(span2_lean) + float(span2_lean_Perturbation)
                            nax_tlean3 = float(span3_lean) + float(span3_lean_Perturbation)
                            nax_tlean4 = float(span4_lean) + float(span4_lean_Perturbation)
                            
    # new true sweep
                            nax_tsweep1 = float(span1_sweep) + float(span1_sweep_Perturbation)
                            nax_tsweep2 = float(span2_sweep) + float(span2_sweep_Perturbation)
                            nax_tsweep3 = float(span3_sweep) + float(span3_sweep_Perturbation)
                            nax_tsweep4 = float(span4_sweep) + float(span4_sweep_Perturbation)

                            os.chdir(current_row +'.'+'nax'+'%d'%naxdir)
                            #filename_nax = "3dbgbinput."+ current_row + ".nax"+'%d'%naxdir + ".dat"
                            filename_nax = "3dbgbinput."+ current_row + "nax"+'%d'%naxdir + ".dat"
                            
#           Write new 3dbgb input file


                            nonaxicount = nonaxicount + 1

                            f3 = open(str(filename_nax), "w")
                            
                            for i in range(0,2):
                                f3.write(lineread[i])
                        #   change the blade row # as bladerow#.bladenum e.g. 1.2 in the file
                        #
                            m=3
                            f3.write(('NAX Design Systems : Blade row#  -  Blade #')  + "\n")
                            #
                            l=4
                            f3.write("          ")
                            f3.write(( '%d'%int(current_row) + '       ' + '%d'%int(naxdir))+ "\n")
                            #
                            m=5
                            f3.write(('Number of blades in this row:')  + "\n")
                            #
                            l=6
                            f3.write("          ")
                            f3.write(( '%d'%int(blades) )+ "\n")
                            #
                            m=7
                            f3.write((' Blade Scaling factor (mm):      Blade Postion (Degree)')  + "\n")
                            #
                            l=8
                            f3.write("          ")
                            f3.write(( '%6f'%float(bsf) + '       ' + '%6f'%float(blade_position) )+ "\n")
                            #


                            for i in range(8,96):
                                f3.write(lineread[i])
                    #
            #
                            d1=96
                            f3.write("  ")
                            f3.write(lineread[d1].split()[0] + "          ")
                            f3.write(lineread[d1].split()[1]  + "      ")
                            f3.write(('%.6f'%nax_tsweep1) + " \n")
                            d2=97
                            f3.write("  ")
                            f3.write(lineread[d2].split()[0] + "         ")
                            f3.write(lineread[d2].split()[1]  + "      ")
                            f3.write(('%.6f'%nax_tsweep2) + " \n")
                            d3=98
                            f3.write("  ")
                            f3.write(lineread[d3].split()[0] + "         ")
                            f3.write(lineread[d3].split()[1]  + "      ")
                            f3.write(('%.6f'%nax_tsweep3) + " \n")
                            d4=99
                            f3.write("  ")
                            f3.write(lineread[d4].split()[0] + "          ")
                            f3.write(lineread[d4].split()[1]  + "      ")
                            f3.write(('%.6f'%nax_tsweep4) + " \n")
        #
                            for i in range(100,104):
                                f3.write(lineread[i])
            
                            t1=104
                            f3.write("  ")
                            f3.write(lineread[t1].split()[0] + "            ")
                            f3.write(('%.6f'%nax_offset1)  + "              ")
                            f3.write(('%.6f'%nax_tlean1) + " \n")
                            t2=105
                            f3.write(" ")
                            f3.write(lineread[t2].split()[0] + "            ")
                            f3.write(('%.6f'%nax_offset2)  + "              ")
                            f3.write(('%.6f'%nax_tlean2) + " \n")
                            t3=106
                            f3.write(" ")
                            f3.write(lineread[t3].split()[0] + "            ")
                            f3.write(('%.6f'%nax_offset3)  +  "              ")
                            f3.write(('%.6f'%nax_tlean3) + " \n")
                            t4=107
                            f3.write("  ")
                            f3.write(lineread[t4].split()[0] + "            ")
                            f3.write(('%.6f'%nax_offset4) +  "              ")
                            f3.write(('%.6f'%nax_tlean4) + " \n")
        #
                            for i in range(108,112):
                                f3.write(lineread[i])
            #
                            p1=112
                            f3.write("  ")
                            f3.write(lineread[p1].split()[0] + "            ")
                            f3.write(('%.6f'%naxspan1_in_beta)  + "\n")
                            p2=113
                            f3.write(" ")
                            f3.write(lineread[p2].split()[0] + "            ")
                            f3.write(('%.6f'%naxspan2_in_beta)  + "\n")
                            p3=114
                            f3.write(" ")
                            f3.write(lineread[p3].split()[0] + "            ")
                            f3.write(('%.6f'%naxspan3_in_beta)  +  "\n")
                            p4=115
                            f3.write("  ")
                            f3.write(lineread[p4].split()[0] + "            ")
                            f3.write(('%.6f'%naxspan4_in_beta) +  "\n")
        #
                            for i in range(116,120):
                                f3.write(lineread[i])
        #
                            q1=120
                            f3.write("  ")
                            f3.write(lineread[q1].split()[0] + "            ")
                            f3.write(('%.6f'%naxspan1_out_beta)  + "\n")
                            q2=121
                            f3.write(" ")
                            f3.write(lineread[q2].split()[0] + "            ")
                            f3.write(('%.6f'%naxspan2_out_beta)  + "\n")
                            q3=122
                            f3.write(" ")
                            f3.write(lineread[q3].split()[0] + "            ")
                            f3.write(('%.6f'%naxspan3_out_beta)  +  "\n")
                            q4=123
                            f3.write("  ")
                            f3.write(lineread[q4].split()[0] + "            ")
                            f3.write(('%.6f'%naxspan4_out_beta) +  "\n")
        #
                            for i in range(124,file_length):
                                f3.write(lineread[i])
                            f3.close
                            
                            ## Writing spancontrol inputs
                            #filename_span = "spancontrolinputs."+ current_row + ".nax"+'%d'%naxdir + ".dat"
                            filename_span = "spancontrolinputs."+ current_row + "nax"+'%d'%naxdir + ".dat"
                            f4 = open(str(filename_span), "w")
                            for s1 in range(0,file_length1):
                                f4.write(lineread2[s1])
                            
                            
                            
                            os.chdir("../")
                        os.chdir("../")


print "                                             "
print "     Axisymmtric Input Files Created : " , axicount
print "     Non-Axisymmtric Input Files Created : " , nonaxicount       


os.chdir("../")