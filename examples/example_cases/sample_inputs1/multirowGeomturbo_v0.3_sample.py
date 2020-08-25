#!/usr/bin/env python

# Legacy file from V0.2 
# This is successfully used for a 3 blade row case.
# Users can modify it based on NAX v0.3 and their design config.
# Sandeep Kumar, GTSL, Feb 2k18
# UC Aerospace Engineering


from glob import glob
import os


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def arrange(file_list):
    for i in range(len(file_list)):    
        temp1 , row , rowtype, ext  = file_list[i].split('.')
        int_part = (filter(str.isdigit,rowtype))
        str_part = rowtype[0:3]
        new_int_part = int_part.zfill(2)
        new_name = '{}.{}.{}{}.{}'.format(temp1,row,str_part,new_int_part,ext)
        os.rename(file_list[i],new_name)
    newfiles=glob("*.geomTurbo")
    return sorted(newfiles) 


files = glob('row.*.axi*.geomTurbo')+glob('row.*.nax*.geomTurbo')
nonaxi_files=len(glob('row.*.nax*.geomTurbo'))

sfiles = arrange(files)
#print "NON-axi files:", nonaxi_files
#print " len sfiles : " , len(sfiles)


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

if n_row == "NONE":
    n_row = []

totalaxirows = len(a_row.split(','))
totalnaxrows = len(n_row.split(','))

all_rows = a_row + ',' + n_row
#print all_rows

totalrows = totalaxirows + totalnaxrows
#print totalrows


os.chdir("../")                     # Navigate out of 'inputs' dir

for counter in range(totalrows):

    rowno = all_rows.split(',')[counter]
    #print "row no ", rowno

    totalfiles = len(glob('row.'+rowno+'*.geomTurbo'))
    #print " File match", totalfiles



    # if totalfiles = 1 , its axisymmteric , else not 
    if totalfiles == 1:
        
        filename = "row."+rowno+".axi01.geomTurbo"
        with open(filename) as f_geom:
            file_length = file_len(filename)
            f = open(filename, "r")
            lineread = f.readlines()
            
            
            #'row.1.axi1.geomTurbo':       - First blade
                
            bladefile = "temp."+rowno+".1.geomTurbo"
            f1 = open(bladefile,"a")
            
            for s1 in range(0,68):
                f1.write(lineread[s1])
            
            m6=69
            f1.write(("    GEOMETRY_PERIODICITY_NUMBER 1") + "\n")
            

            for s1 in range(68,file_length-4):
                f1.write(lineread[s1])
            f1.close()



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

                        bladefile = "temp."+rowno+".1.geomTurbo"
                        f2 = open(str(bladefile),"w")
                        for s1 in range(64,67):
                            f2.write(lineread[s1])
                            
                        m5=68
                        f2.write(("    PERIODICITY  1") + "\n")
                        
                        m=69
                        f2.write(("    GEOMETRY_PERIODICITY_NUMBER 1") + "\n")
                        
                        for s1 in range(68,77):
                            f2.write(lineread[s1])
        #                    
                        m2=78
                        f2.write(("    NAME     Blade-1") + "\n")
        #               
                        for s1 in range(78,91):
                            f2.write(lineread[s1])
                            
                        m21=92
                        f2.write(("number_of_blades          1") + "\n")
                        
                        for s1 in range(92,file_length-5):
                            f2.write(lineread[s1])
        #                 
                        f2.close()

                    

                elif i == int(index+totalfiles-1):                 # row's  last blade
                 
                    with open(sfiles[i]) as f_geom:
                        file_length = file_len(sfiles[i])
                        f = open(sfiles[i], "r")
                        lineread = f.readlines()

                        bladefile = "temp."+rowno+".3x.geomTurbo"
                            
                        f4 = open(str(bladefile),"w")
                            
                        for s1 in range(76,77):
                            f4.write(lineread[s1])
                            
                        m3=78
                        f4.write(("    NAME     Blade-") + '%d'%int(totalfiles) +"\n")
                            
                        for s1 in range(78,91):
                            f4.write(lineread[s1])
                                
                        m31=92
                        f4.write(("number_of_blades          1") + "\n")
                        
                        for s1 in range(92,file_length-3):
                            f4.write(lineread[s1])
                        f4.close() 

                else:
                  
                    with open(sfiles[i]) as f_geom:
                        file_length = file_len(sfiles[i])
                        f = open(sfiles[i], "r")
                        lineread = f.readlines()
#                                                           
                        for s1 in range(76,77):
                            midf.write(lineread[s1])
                        
                        m4=78
                        midf.write(("    NAME     Blade-") + '%d'%i +"\n")
                        
                        for s1 in range(78,91):
                            midf.write(lineread[s1])
                            
                        m41=92
                        midf.write(("number_of_blades          1") + "\n")
                        
                        for s1 in range(92,file_length-5):
                            midf.write(lineread[s1])

        midf.close() 


# # combining all the files to 1 Geomturbo file  

files2 = sorted(glob("temp.*"))
#print files2 

with open('turbomultirow.geomTurbo', 'w') as outfile:
    for fname in files2:
        with open(fname) as infile:
            for readlines in infile:
                outfile.write(readlines)


# # Deleting all temporary files
for filename in files2:
   os.remove(filename)
