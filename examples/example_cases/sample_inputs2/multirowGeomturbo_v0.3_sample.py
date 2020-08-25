#!/usr/local/bin/python3

# NAX v0.3 Aero-Design Systems
# Python 3.5 script 
# used to create multi-row geomTurbo file
# These Module may need to be rewritten/ edited for ..
# ... different number of blade rows cases ( configurations)
# For eg, this file is tested for 1 blade row (axi/non-axi) case
# Sandeep Kumar, OCT 2k18
#  GTSL ,UC Aerospace Engineering

from glob import glob
import os

a_row =0 
n_row =0

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def arrange(file_list):
    for i in range(len(file_list)):    
        temp1 , row , rowtype, ext  = file_list[i].split('.')
        int_part = rowtype[3:]
        str_part = rowtype[0:3]
        new_int_part = int_part.zfill(2)
        new_name = '{}.{}.{}{}.{}'.format(temp1,row,str_part,new_int_part,ext)
        os.rename(file_list[i],new_name)
    newfiles=glob("*.geomTurbo")
    return sorted(newfiles) 


files = glob('row.*.axi*.geomTurbo')+glob('row.*.nax*.geomTurbo')
nonaxi_files=len(glob('row.*.nax*.geomTurbo'))
sfiles = arrange(files)

os.chdir("./inputs")                # Navigate in  'inputs' dir

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

# 
if n_row=="0":
    totalnaxrows=0
    all_rows=a_row
else:
    totalnaxrows = len(n_row.split(','))
    all_rows = n_row + ',' + a_row  
    
if a_row=="0":
    totalaxirows=0
    all_rows=n_row
else:
    totalaxirows = len(a_row.split(','))
    all_rows = n_row + ',' + a_row


totalrows = totalaxirows + totalnaxrows

os.chdir("../")                     # Navigate out of 'inputs' dir


for counter in range(totalrows):

    rowno = all_rows.split(',')[counter]

    totalfiles = len(glob('row.'+rowno+'*.geomTurbo'))

    #if totalfiles == 1 and rowno in a_row:
    if totalfiles == 1:

        filename = "row."+rowno+".axi01.geomTurbo"

        
        with open(filename) as f_geom:
            file_length = file_len(filename)
            f = open(filename, "r")
            lineread = f.readlines()

            bladefile = "temp."+rowno+".axi1.geomTurbo"
            f1 = open(bladefile,"a")
            
            for s1 in range(0,68):
                f1.write(lineread[s1])
            
            m6=69
            f1.write(("    GEOMETRY_PERIODICITY_NUMBER 1") + "\n")
            
            for s1 in range(68,file_length-4):
                f1.write(lineread[s1])
            f1.close()

     # write non-axisymmteric geomturbo file
    else:

        filename = "row."+rowno+".nax01.geomTurbo"
        index = sfiles.index(filename)

        with open("temp."+rowno+".2x.geomTurbo","w") as midf:

            for i in range(index,(index+totalfiles)):
   
                if i == int(index) :
  
                    with open(sfiles[i]) as f_geom:
                        file_length = file_len(sfiles[i])
                        f = open(sfiles[i], "r")
                        lineread = f.readlines()

                        bladefile = "temp."+rowno+".1x.geomTurbo"
                        f2 = open(str(bladefile),"w")
                        
                        
                        for s1 in range(0,69):
                            f2.write(lineread[s1])
                        
                        
                        m5=70
                        f2.write(("    PERIODICITY  1") + "\n")
                        
                        m=71
                        f2.write(("    GEOMETRY_PERIODICITY_NUMBER 1") + "\n")
                        
                        for s1 in range(70,79):
                            f2.write(lineread[s1])
        ##                    
                        m2=80
                        f2.write(("    NAME     Blade-1") + "\n")
        ##               
                        for s1 in range(80,93):
                            f2.write(lineread[s1])
                            
                        m21=94
                        f2.write(("number_of_blades          1") + "\n")
                        

        #               
                        for s1 in range(94,file_length-5):
                            f2.write(lineread[s1])
                        f2.close()


                elif i == int(index+totalfiles-1):                 # row's  last blade
                    #print "i  as last index", i, sfiles[i]
                 
                    with open(sfiles[i]) as f_geom:
                        file_length = file_len(sfiles[i])
                        f = open(sfiles[i], "r")
                        lineread = f.readlines()

                        bladefile = "temp."+rowno+".3x.geomTurbo"
                            
                        f4 = open(str(bladefile),"w")
                        
                        
                        for s1 in range(78,79): 
                            f4.write(lineread[s1])
                        
                        m3=80
                        f4.write(("    NAME     Blade-") + '%d'%int(totalfiles) +"\n")
                            

                        for s1 in range(80,93):
                            f4.write(lineread[s1])
                                
                        m31=94
                        f4.write(("number_of_blades          1") + "\n")
                        
                        for s1 in range(94,file_length-3):   
                            f4.write(lineread[s1])
                        f4.close() 

                else:
                  
                    with open(sfiles[i]) as f_geom:

                        file_length = file_len(sfiles[i])
                        f = open(sfiles[i], "r")
                        lineread = f.readlines()
#                                                           
                        for s1 in range(78,79):
                            midf.write(lineread[s1])
                        
                        m4=80
                        midf.write(("    NAME     Blade-") + '%d'%(i+1) +"\n")

                        for s1 in range(80,93):
                            midf.write(lineread[s1])
                            
                        m41=94
                        midf.write(("number_of_blades          1") + "\n")

                        for s1 in range(94,file_length-5):    
                            midf.write(lineread[s1])

        midf.close() 


# # combining all the files to 1 Geomturbo file  

files2 = sorted(glob("temp.1.*"))

with open('multirow.geomTurbo', 'w') as outfile:   # change final geomTurbo file name here 
    for fname in files2:
        with open(fname) as infile:
            for readlines in infile:
                outfile.write(readlines)


# # Deleting all temporary files
for filename in files2:
   os.remove(filename)

