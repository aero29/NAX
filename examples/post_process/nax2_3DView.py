#!/usr/bin/env python

# Post Processing script for 3D visualization for NAX v2 support 
# Python 2.7 
# Uses blde3d files generated using T-Blade3
# Sandeep Kumar , UC Aerospace Engineering
# some parts of script adapted from script by Kiran siddappaji ( GTSL -Tblade3 website)
# Feb 2K18

###########################################################


from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import sys , os
import math
import numpy as np
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import glob , shutil

print "    "
print " 3D visualization script for NAX v2 "

row=str(2)
count = 0 
nfiles = 31       # bladerows (29) + casing and hub (2) 

base_dir = os.getcwd()
dest_dir = os.getcwd() + ("/row"+row)


for root, dirs, files in os.walk(dest_dir):
    for filename in files:

        if filename == "blade3d.nasafan.dat" :
            count = count+1
            old_name = os.path.join(os.path.abspath(root),filename)
            base, extension = os.path.splitext(filename)
            new_name = os.path.join(base_dir, base +"."+ str(format(count,'02d')) +extension)
            shutil.copy(old_name,new_name)


for root, dirs, files in os.walk(dest_dir+"/2.nax1"):
    for filename2 in files:
        
        if filename2 == "casing.nasafan.sldcrv" :
            old_name2 = os.path.join(os.path.abspath(root),filename2)
            base2, extension2 = os.path.splitext(filename2)
            new_name2 = os.path.join(base_dir, base2 + extension2)
            shutil.copy(old_name2,new_name2)
            
        elif filename2 == "hub.nasafan.sldcrv" :
            
            old_name2 = os.path.join(os.path.abspath(root),filename2)
            base2, extension2 = os.path.splitext(filename2)
            new_name2 = os.path.join(base_dir, base2 + extension2)
            shutil.copy(old_name2,new_name2)
            

def set_aspect_equal_3d(ax):
	
    xlim = ax.get_xlim3d()
    ylim = ax.get_ylim3d()
    zlim = ax.get_zlim3d()

    from numpy import mean
    xmean = mean(xlim)
    ymean = mean(ylim)
    zmean = mean(zlim)

    plot_radius = max([abs(lim - mean_)
                       for lims, mean_ in ((xlim, xmean),
                                           (ylim, ymean),
                                           (zlim, zmean))
                       for lim in lims])

    ax.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
    ax.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
    ax.set_zlim3d([zmean - plot_radius, zmean + plot_radius])	
	
nskip =  1 
npt   = -1 
ndim  = -1 
pltcoord = [-1] 
coordnames  = ['x','y','z']


pi = math.pi
nskips = [1]*nfiles
npts = [-1]*nfiles


fname = glob.glob("blade3d.nasafan.??.dat")
fnames = fname + ['casing.nasafan.sldcrv','hub.nasafan.sldcrv']

def file_dim(fname, nskip):
  f = open(fname, 'r')
  for i in range(nskip+1):
    datastr = f.readline()

  f.close()
  return len(datastr.split())


def file_len(fname):
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

fig = plt.figure(figsize=(8,8), dpi = 100)
ax = fig.add_subplot(111,projection='3d')

ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.axis('off')

for k in xrange(len(fnames)): 
  fname = fnames[k]
  npt = npts[k]
  nskip = nskips[k]

  if npt < 0:
   npt = file_len(fname) - nskip

  if ndim < 0:
   ndim = file_dim(fname, nskip)

  if pltcoord[0] < 0:
   pltcoord = []
   for i in range(ndim):
     pltcoord.append(i)
    
  nplt = len(pltcoord)

  x3d = np.zeros(npt)
  y3d = np.zeros(npt)
  z3d = np.zeros(npt)

#
  #Read file
  f = open(fname, 'r')

  for i in range(nskip):
   datastr = f.readline()

  line = np.zeros((nplt,npt))
  for i in range(npt):
   datastr = f.readline()
   data    = datastr.split()
   for j in range(nplt):
    line[j][i] = data[pltcoord[j]]
   #
  #####

  for i in range(npt):
   x3d[i] = line[0][i]
   y3d[i] = line[1][i]
   z3d[i] = line[2][i]


  ax.set_aspect('equal')

  # Plotting\ 
  ax.plot_wireframe(y3d,x3d,z3d,color ='k',lw=1.5)
#

plt.xlabel("Y dim : Engine CS  ")
plt.ylabel("X dim : Engine Axis")
set_aspect_equal_3d(ax)

ax.view_init(0,90)
#ax.view_init(0,90)
# One of the good view : Choose azimuth 65 deg, elev = -171 deg
plt.title("NAX v0.2 Design 3D View")
    #plt.legend(["3D Airfoil (x,y,z)"], loc='upper center', bbox_to_anchor=(0.9, 1.10),
#       fancybox=True, shadow=True, ncol=2)  
		  
print "  "		  
plt.savefig("3DView.png",dpi=300)
print " Figure saved ... !"
print "  "
#plt.show()
 # rotate the axes and update
 #for angle in range(0, 360):
    #    ax.view_init(50, angle)
#plt.draw()
#    plt.pause(0.25)

# remove imported files 
for file in fnames:
  os.remove(file)
