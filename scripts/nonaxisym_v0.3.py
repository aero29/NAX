#!/usr/bin/python3

# NAX v0.3 Aero-Design Systems
# Python script (v3.5)to produce Non-Axisymmetric designs
# Python script (v2.7) was used till NAX v0.2
# Support script that reads 3dbgbinput files genearted from TAXI
# Reads input data from naxinput.<row#>.dat for process
# Produces Individual blade files for corresponding row
# makes directory for all the blades separately
# >> -------------------------------------------------------------
# >> --------------------------------------------------------------
# Sandeep Kumar , DEC 2K18
# GTSL , Dept of Aerospace Engg, University of Cincinnati
# --------------------------------------------------------
# ------------------------------------------------------------


# Library Imports
import os , math
import numpy as np
import glob
import shutil
from itertools import islice
# ------------------------------------------------------------

os.chdir("./inputs")  

# ------------------------------------------------------------
# check if 3dbgbinput files are present in current directory
# else exit the script 
# check if required files are present in current directory
# else exit the script


print (" ")
print ("     Checking Inputs Validity -")

if any(File.startswith("naxinfo") for File in os.listdir(".")):
    print (" ")
    print ( "     nax-info file Exist ")
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

if any(File.startswith("3dbgbinput.") for File in os.listdir(".")):
    print ( "     tblade3/3dbgb input files Exist ")
else:
    print( "    ERROR : tblade3/3dbgbinput files not found")
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

# for 0 blade row declaration - used for just 1 blade rows

if n_row=="0":
    totalnaxrows=0
    all_rows = a_row
else:
    totalnaxrows = len(n_row.split(','))
    all_rows = a_row + ',' + n_row


if a_row=="0":
    totalaxirows=0
    all_rows = n_row
else:
    totalaxirows = len(a_row.split(','))
    all_rows = a_row + ',' + n_row
    
# counter for number of files
axicount = 0
nonaxicount = 0

total = totalaxirows + totalnaxrows

print ('     Total nax-input files :', totalnaxrows)
print ('     Total 3dbgb input files :', total)

# ------------------------------------------------------------


for row in range(total):                        

    current_row = all_rows.split(',')[row]
    os.makedirs('row'+current_row)
    
    curr_3dbgbfile = "3dbgbinput." + current_row +".dat"
    curr_spanfile  = "spancontrolinputs."+ current_row + ".dat"
    
    with open(curr_spanfile) as fspanc:
        file_length1 = file_len(curr_spanfile)
        fspan = open(curr_spanfile, "r")
        lineread2 = fspan.readlines()
    
    with open(curr_3dbgbfile, 'r') as f:
        
        file_length = file_len(curr_3dbgbfile)
        f3dbgb= open(curr_3dbgbfile, "r")
        lineread = f3dbgb.readlines()

        temp_sw = []
        temp_sw2 = []
        temp_ln = []
        temp_ln2 = []
        temp_inb = []
        temp_inb2 = []
        temp_outb = []
        temp_outb2 = []
        temp_cm = []
        temp_cm2 = []
        temp_tmc= []
        temp_tmc2= []
        t_sw = []
        t_sw2 = []
        t_ln = []
        t_ln2 = []
        t_inb = []
        t_inb2 = []
        t_outb = []
        t_outb2 = []
        t_cm = []
        t_cm2 = []
        t_tmc = []
        t_tmc2 = []
        var1=[]
        temp6=0
        
        for num, line in enumerate(f,3):
            if line ==' Number of blades in this row:\n':
                blades=int(next(f).strip())
            
            if line ==' Blade Scaling factor (mm):\n':
                bsf=float(next(f).strip())

            if line ==' Control points for sweep:\n':
                swline=num
                cp_sweep=int(next(f).strip())
                next(f)
                for i in range(cp_sweep):
                    var1=(next(f).strip())
                    temp_sw=var1.split()[1]
                    t_sw.append(temp_sw)
                    temp_sw2=var1.split()[0]
                    t_sw2.append(temp_sw2)

            if line ==' Control points for lean:\n':
                cp_lean=int(next(f).strip())
                next(f)
                for i in range(cp_lean):
                    var1=(next(f).strip())
                    temp_ln=var1.split()[1]
                    t_ln.append(temp_ln)
                    temp_ln2=var1.split()[0]
                    t_ln2.append(temp_ln2)

            if line ==' Control points for in_beta*:\n':
                cp_inbeta=int(next(f).strip())
                next(f)
                for i in range(cp_inbeta):
                    var1=(next(f).strip())
                    temp_inb=var1.split()[1]
                    t_inb.append(temp_inb)
                    temp_inb2=var1.split()[0]
                    t_inb2.append(temp_inb2)

            if line ==' Control points for out_beta*:\n':
                cp_outbeta=int(next(f).strip())
                next(f)
                for i in range(cp_outbeta):
                    var1=(next(f).strip())
                    temp_outb=var1.split()[1]
                    t_outb.append(temp_outb)
                    temp_outb2=var1.split()[0]
                    t_outb2.append(temp_outb2)

            if line ==' Control points for chord_multiplier:\n':
                cp_cm=int(next(f).strip())
                next(f)
                for i in range(cp_cm):
                    var1=(next(f).strip())
                    temp_cm=var1.split()[1]
                    t_cm.append(temp_cm)
                    temp_cm2=var1.split()[0]
                    t_cm2.append(temp_cm2)

            if line ==' Control points for tm/c:\n':
                cp_tmc=int(next(f).strip())
                next(f)
                for i in range(cp_tmc):
                    var1=(next(f).strip())
                    temp_tmc=var1.split()[1]
                    t_tmc.append(temp_tmc)
                    temp_tmc2=var1.split()[0]
                    t_tmc2.append(temp_tmc2)


#        # FOR AXI SYM ROW
        if current_row in a_row[:]:

            os.chdir("./"'row'+ current_row)
            for naxdir in range(1,2):
                os.makedirs(current_row +'.'+'axi1')

            blade_position = 0.0                #Blade Postion
#                #
            temp1=[0.000000]*10                                     # temporary variable, default
            sweep_Perturbation = [0.000000] * cp_sweep             #Sweep
            nax_tsweep = [0.000000] * cp_sweep
            lean_Perturbation = [0.000000] * cp_lean                #Lean
            nax_tlean = [0.000000] * cp_lean
            inbeta_Perturbation = [0.000000] * cp_inbeta            #InBeta Angles
            nax_in_beta = [0.000000] * cp_inbeta
            outbeta_Perturbation = [0.000000] * cp_outbeta          #OutBeta Angles
            nax_out_beta = [0.000000] * cp_outbeta
            cm_Perturbation = [0.000000] * cp_cm                    #chord multiplier
            nax_cm = [0.000000] * cp_cm
            tmc_Perturbation = [0.000000] * cp_tmc                  #tmc
            nax_tmc = [0.000000] * cp_tmc

#                # new true sweep
            for i in range(cp_sweep):
                #temp1=t_sw[i]+ sweep_Perturbation[i]
                nax_tsweep.append(float(t_sw[i]))

#                # new true lean
            for i in range(cp_lean):
                #temp1=t_ln[i]+ lean_Perturbation[i]
                nax_tlean.append(float(t_ln[i]))

            # new inlet angles
            for i in range(cp_inbeta):
                #temp1=t_inb[i]+inbeta_Perturbation[i]
                nax_in_beta.append(float(t_inb[i]))

#                # new outlet angles
            for i in range(cp_outbeta):
                #temp1=t_outb[i] + outbeta_Perturbation[i]
                nax_out_beta.append(float(t_outb[i]))

#                # new chord multiplier
            for i in range(cp_cm):
                #temp1=t_cm[i] + cm_Perturbation[i]
                nax_cm.append(float(t_cm[i]))

#                # new tm/c
            for i in range(cp_tmc):
                #temp1=t_tmc[i]+ tmc_Perturbation[i]
                nax_tmc.append(float(t_tmc[i]))
#
            os.chdir(current_row +'.'+'axi1')

#           Write new 3dbgb input file
            axicount = axicount + 1
#
            filename_nax = "3dbgbinput."+ current_row + "axi1" + ".dat"
            f3 = open(str(filename_nax), "w")

            for i in range(0,2):
                f3.write(lineread[i])
#
            #   change the blade row # as bladerow#.blade num e.g. 1.2 in the file
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
            temp6=swline+2
            for i in range(8,temp6):
                f3.write(lineread[i])
            #             #
            for i in range(cp_sweep):
                f3.write(t_sw2[i] + "            " + ('%.16f'%float(nax_tsweep[i])) + " \n")
                    
            temp6= temp6 + cp_sweep
            for i in range(temp6,temp6+4):
                f3.write(lineread[i])
                
            for i in range(cp_lean):
                f3.write(t_ln2[i] + "            " + ('%.16f'%float(nax_tlean[i])) + " \n")
                    
            temp6= temp6 + cp_lean +4
            for i in range(temp6,temp6+4):
                f3.write(lineread[i])
            for i in range(cp_inbeta):
                f3.write(t_inb2[i] + "            " + ('%.16f'%float(nax_in_beta[i])) + " \n")
                
            temp6= temp6 + cp_inbeta +4
            for i in range(temp6,temp6+4):
                f3.write(lineread[i])
            for i in range(cp_outbeta):
                f3.write(t_outb2[i] + "            " + ('%.16f'%float(nax_out_beta[i])) + " \n")
                    
            temp6= temp6 + cp_outbeta +4
            for i in range(temp6,temp6+4):
                f3.write(lineread[i])
            for i in range(cp_cm):
                f3.write(t_cm2[i] + "            " + ('%.16f'%float(nax_cm[i])) + " \n")
        
            temp6= temp6 + cp_cm +4
            for i in range(temp6,temp6+4):
                f3.write(lineread[i])
            for i in range(cp_tmc):
                f3.write(t_tmc2[i] + "            " + ('%.16f'%float(nax_tmc[i])) + " \n")
            
            temp6= temp6 + cp_tmc +4
            for i in range(temp6,file_length):
                f3.write(lineread[i])
                    
            f3.close

            # Write spancontrol file
            filename_span = "spancontrolinputs."+ current_row + ".axi1" + ".dat"
            filename_span = "spancontrolinputs."+ current_row + "axi1" + ".dat"
            f4 = open(str(filename_span), "w")
            for s1 in range(0,file_length1):
                f4.write(lineread2[s1])

            os.chdir("../../")
#
    # FOR NON-AXI ROW
    
        elif current_row in n_row[:]:
            # ROW SPECIFIC OPERATION  <<<<<<<<<<<<<<<<<<<<<<<<<
            # Read the naxinput file  <<<<<<<<<<<<<<<<<<<<<<<<<
            
            with open("naxinput."+current_row+".dat") as finput:
                # Variable declaration
                ninp_sw=[]
                ninp_ln=[]
                ninp_inb=[]
                ninp_outb=[]
                ninp_cm=[]
                ninp_tmc=[]
                
                for inputline in finput:
                    
                    # Sweep
                    if inputline =='Sweep Span Control Points     Fourier Modes (Magnitude , Phase)\n':
                        temp1=(next(finput).strip())
                        ninp_swspan=int((temp1).split()[0])
                        ninp_swfmode=int((temp1).split()[1])

                        temp2=[]
                        for i in range(ninp_swspan):
                            temp2=(next(finput).strip()).split()[1:(2*ninp_swfmode+1)]
                            ninp_sw.append(temp2)

                    # Lean
                    if inputline =='Lean Span Control Points     Fourier Modes (Magnitude , Phase)\n':
                        temp1=(next(finput).strip())
                        ninp_lnspan=int((temp1).split()[0])
                        ninp_lnfmode=int((temp1).split()[1])

                        temp2=[]
                        for i in range(ninp_lnspan):
                            temp2=(next(finput).strip()).split()[1:(2*ninp_lnfmode+1)]
                            ninp_ln.append(temp2)

                    # Inlet Beta
                    if inputline =='In_beta Span Control Points     Fourier Modes (Magnitude , Phase)\n':
                        temp1=(next(finput).strip())
                        ninp_inbspan=int((temp1).split()[0])
                        ninp_inbfmode=int((temp1).split()[1])

                        temp2=[]
                        for i in range(ninp_inbspan):
                            temp2=(next(finput).strip()).split()[1:(2*ninp_inbfmode+1)]
                            ninp_inb.append(temp2)

                    # Outlet Beta
                    if inputline =='Out_beta Span Control Points     Fourier Modes (Magnitude , Phase)\n':
                        temp1=(next(finput).strip())
                        ninp_outbspan=int((temp1).split()[0])
                        ninp_outbfmode=int((temp1).split()[1])
                        
                        temp2=[]
                        for i in range(ninp_outbspan):
                            temp2=(next(finput).strip()).split()[1:(2*ninp_outbfmode+1)]
                            ninp_outb.append(temp2)

                    # Chord_multiplier
                    if inputline =='Chord_multiplier Span Control Points     Fourier Modes (Magnitude , Phase)\n':
                        temp1=(next(finput).strip())
                        ninp_cmspan=int((temp1).split()[0])
                        ninp_cmfmode=int((temp1).split()[1])
    
                        temp2=[]
                        for i in range(ninp_cmspan):
                            temp2=(next(finput).strip()).split()[1:(2*ninp_cmfmode+1)]
                            ninp_cm.append(temp2)

                    # Tm/c
                    if inputline =='tm/c Span Control Points     Fourier Modes (Magnitude , Phase)\n':
                        temp1=(next(finput).strip())
                        ninp_tmcspan=int((temp1).split()[0])
                        ninp_tmcfmode=int((temp1).split()[1])

                        temp2=[]
                        for i in range(ninp_tmcspan):
                            temp2=(next(finput).strip()).split()[1:(2*ninp_tmcfmode+1)]
                            ninp_tmc.append(temp2)

                os.chdir("./"'row'+ current_row)

            # BLADE SPECIFIC OPERATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                for naxdir in range(1,blades+1):
                    
                    os.makedirs(current_row +'.nax'+'%d'%naxdir)


        # Initialization
                    blade_position = 0.0                #Blade Postion
                    blade_location = 0.0
                    blade_position = float(naxdir * float(360.0/(blades)))      # [Degree ]
                    blade_location = float(naxdir * float((2 * math.pi)/(blades)))  # [Radians] value of blade_position
                    
        # Sweep calculations
                    temp3=[]          #Local variable declaration
                    sum3=[]
                    temp5=[]
                    sweep_Perturbation=[]

                    for nf in range(ninp_swspan):               # loop through no of span locations
                        temp3=np.asarray(ninp_sw[nf])
                        temp4=0.0
                        sum4=0.0
                        for i in range(ninp_swfmode):           # loop through no of modes
                            temp4=float(temp3[2*i][:-1])*(math.sin(blade_location*(i+1) + float(temp3[2*i+1][:-1])))
                            sum4=sum4+temp4
                        sum3.append(sum4)                       # contains values of non-axisymmetry
                        
                        temp5= sum3[nf]+float(t_sw[nf])
                        sweep_Perturbation.append(temp5)

        # Lean calculations
                    temp3=[]
                    sum3=[]
                    temp5=[]
                    lean_Perturbation=[]
                    for nf in range(ninp_lnspan):               # loop through no of span locations
                        temp3=np.asarray(ninp_ln[nf])
                        temp4=0.0
                        sum4=0.0
                        for i in range(ninp_lnfmode):           # loop through no of modes
                            temp4=float(temp3[2*i][:-1])*(math.sin(blade_location*(i+1) + float(temp3[2*i+1][:-1])))
                            sum4=sum4+temp4
                        sum3.append(sum4)                       # contains values of non-axisymmetry

                        temp5=sum3[nf]+float(t_ln[nf])
                        lean_Perturbation.append(temp5)

        # InBeta calculations
                    temp3=[]
                    sum3=[]
                    temp5=[]
                    inbeta_Perturbation=[]
                    for nf in range(ninp_inbspan):               # loop through no of span locations
                        temp3=np.asarray(ninp_inb[nf])
                        temp4=0.0
                        sum4=0.0
                        for i in range(ninp_inbfmode):           # loop through no of modes
                            temp4=float(temp3[2*i][:-1])*(math.sin(blade_location *(i+1) + float(temp3[2*i+1][:-1])))
                            sum4=sum4+temp4
                        sum3.append(sum4)                       # contains values of non-axisymmetry
                        
                        temp5=sum3[nf]+float(t_inb[nf])
                        inbeta_Perturbation.append(temp5)

        # OutBeta calculations
                    temp3=[]
                    sum3=[]
                    temp5=[]
                    outbeta_Perturbation=[]
                    for nf in range(ninp_outbspan):               # loop through no of span locations
                        temp3=np.asarray(ninp_outb[nf])
                        temp4=0.0
                        sum4=0.0
                        for i in range(ninp_outbfmode):           # loop through no of modes
                            temp4=float(temp3[2*i][:-1])*(math.sin(blade_location*(i+1) + float(temp3[2*i+1][:-1])))
                            sum4=sum4+temp4
                        sum3.append(sum4)                       # contains values of non-axisymmetry
                        
                        temp5=sum3[nf]+float(t_outb[nf])
                        outbeta_Perturbation.append(temp5)

        # Chord Multiplier calculations
                    temp3=[]
                    sum3=[]
                    temp5=[]
                    cm_Perturbation=[]
                    for nf in range(ninp_cmspan):               # loop through no of span locations
                        temp3=np.asarray(ninp_cm[nf])
                        temp4=0.0
                        sum4=0.0
                        for i in range(ninp_cmfmode):           # loop through no of modes
                            temp4=float(temp3[2*i][:-1])*(math.sin(blade_location*(i+1) + float(temp3[2*i+1][:-1])))
                            sum4=sum4+temp4
                        sum3.append(sum4)                       # contains values of non-axisymmetry
                        
                        temp5=sum3[nf]+float(t_cm[nf])
                        cm_Perturbation.append(temp5)

        # Tm/c calculations
                    temp3=[]
                    sum3=[]
                    temp5=[]
                    tmc_Perturbation=[]
                    for nf in range(ninp_tmcspan):               # loop through no of span locations
                        temp3=np.asarray(ninp_tmc[nf])
                        temp4=0.0
                        sum4=0.0
                        for i in range(ninp_tmcfmode):           # loop through no of modes
                            temp4=float(temp3[2*i][:-1])*(math.sin(blade_location*(i+1) + float(temp3[2*i+1][:-1])))
                            sum4=sum4+temp4
                        sum3.append(sum4)                       # contains values of non-axisymmetry
                        
                        temp5=sum3[nf]+float(t_tmc[nf])
                        tmc_Perturbation.append(temp5)
                    
                    os.chdir(current_row +'.'+'nax'+'%d'%naxdir)
#
##           Write new 3dbgb input file
                    filename_nax = "3dbgbinput."+ current_row + "nax"+'%d'%naxdir + ".dat"
                    nonaxicount = nonaxicount + 1
#
                    f3 = open(str(filename_nax), "w")

                    for i in range(0,2):
                        f3.write(lineread[i])
                #   change the blade row # as bladerow#.bladenum e.g. 1.2 in the file
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
                    f3.write(( '%6f'%float(bsf) + '                     ' + '%6f'%float(blade_position) )+ "\n")
#             #
                    temp6=swline+2
                    for i in range(8,temp6):
                        f3.write(lineread[i])
#             #
                    for i in range(cp_sweep):
                        f3.write(t_sw2[i] + "            " + ('%.16f'%float(sweep_Perturbation[i])) + " \n")
                    
                    temp6= temp6 + cp_sweep
                    for i in range(temp6,temp6+4):
                        f3.write(lineread[i])
                    for i in range(cp_lean):
                        f3.write(t_ln2[i] + "            " + ('%.16f'%float(lean_Perturbation[i])) + " \n")

                    temp6= temp6 + cp_lean +4
                    for i in range(temp6,temp6+4):
                        f3.write(lineread[i])
                    for i in range(cp_inbeta):
                        f3.write(t_inb2[i] + "            " + ('%.16f'%float(inbeta_Perturbation[i])) + " \n")

                    temp6= temp6 + cp_inbeta +4
                    for i in range(temp6,temp6+4):
                        f3.write(lineread[i])
                    for i in range(cp_outbeta):
                        f3.write(t_outb2[i] + "            " + ('%.16f'%float(outbeta_Perturbation[i])) + " \n")

                    temp6= temp6 + cp_outbeta +4
                    for i in range(temp6,temp6+4):
                        f3.write(lineread[i])
                    for i in range(cp_cm):
                        f3.write(t_cm2[i] + "            " + ('%.16f'%float(cm_Perturbation[i])) + " \n")

                    temp6= temp6 + cp_cm +4
                    for i in range(temp6,temp6+4):
                        f3.write(lineread[i])
                    for i in range(cp_tmc):
                        f3.write(t_tmc2[i] + "            " + ('%.16f'%float(tmc_Perturbation[i])) + " \n")

                    temp6= temp6 + cp_tmc +4
                    for i in range(temp6,file_length):
                        f3.write(lineread[i])
                    f3.close

                    ## Writing spancontrol inputs

                    filename_span = "spancontrolinputs."+ current_row + "nax"+'%d'%naxdir + ".dat"
                    f4 = open(str(filename_span), "w")
                    for s1 in range(0,file_length1):
                        f4.write(lineread2[s1])

                    os.chdir("../")
#
#
print ("                                             ")
print ("     Axisymmtric Input Files Created : " , axicount)
print ("     Non-Axisymmtric Input Files Created : " , nonaxicount)
#
os.chdir("../")
