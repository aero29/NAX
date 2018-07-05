# !/bin/sh

# NAX v0.2 Aero-Design Systems
# Sandeep Kumar ,MARCH 2K18
# GTSL , Dept of Aerospace Engineering
# University of Cincinnati , USA
# -------------------------------------------------------------
# ------------------------------------------------------------ 


# Cleaning the Direcotory of pre-existing directories/files

rm *.geomTurbo
rm -r row*
rm *.log *.txt
rm *.jpg
clear


echo " -----------------------------------------------" |tee caserun.log
echo " -----------------------------------------------" |tee -a caserun.log
echo "          NAX v0.2 " 								|tee -a caserun.log
echo " Non-Axisymmetric Turbomachinery Design System" |tee -a caserun.log
echo " -----------------------------------------------"|tee -a caserun.log
echo " -----------------------------------------------"|tee -a caserun.log
echo " NAX v0.2 Harmonics based Aero-Design Systems ">>caserun.log
echo "  Working Sequence "|tee -a caserun.log
echo " pre-proc_v0.2.py - nonaxisym_v0.2.py - T-Blade3 - multirowGeomTurbo_v0.2 " |tee -a caserun.log
echo " Run Stat:"   $(date | tee -a)  
      date|tee -a >> caserun.log
echo "  "
echo " Developed by "|tee -a caserun.log
echo " Sandeep Kumar , Mark G Turner " |tee -a caserun.log
echo " email : turnermr@ucmail.uc.edu" |tee -a caserun.log
echo " Gas Turbine Simulation Laboratory "|tee -a caserun.log
echo " Dept of Aerospace Engineering, Univ of Cincinnati , USA "|tee -a caserun.log
echo " -----------------------------------------------"|tee -a caserun.log


echo "	"

case_dir=$(pwd)
#echo $case_dir

cd inputs

case_inputs=$(pwd)

cd ../..
cd scripts/
scripts_dir=$(pwd)
#echo $scripts_dir

cd ..
cd executables/
executables_dir=$(pwd)
#echo $executables_dir

cd ..
cd post_process/
post_proc_dir=$(pwd)
#echo $post_proc_dir

cd ..
base_dir=$(pwd)
#echo $base_dir

cd "$case_dir"
#ls


SECONDS=0  
echo " -----------------------------------------------"|tee -a caserun.log
echo "  >>>>>     MODULE 1 : PRE-PROCESSING " |tee -a caserun.log
echo " -----------------------------------------------" |tee -a caserun.log
echo " "

echo " Part A : Generating NAX input files .. " |tee -a caserun.log

chmod +x "$scripts_dir"/preproc_v0.2.py 
"$scripts_dir"/preproc_v0.2.py 
 echo "  "

echo " Part B : Generating Non-Axisymmetric Input files ..." |tee -a caserun.log

chmod +x "$scripts_dir"/nonaxisym_v0.2.py 
"$scripts_dir"/nonaxisym_v0.2.py |tee -a caserun.log
echo "  "

mv inputs/row* ./ | >>/dev/null



echo " "
echo " -----------------------------------------------"|tee -a caserun.log
echo "  >>>>>     MODULE 2 : 3D-CAD Generation  " |tee -a caserun.log
echo " -----------------------------------------------" |tee -a caserun.log
echo " "

# #Run 3dbgb recursively

echo " Part A : Running T-Blade3 to create blade geometry files ..." |tee -a caserun.log
echo "    "

 for d in ./row*/; do ( cd "$d" && for e in ./*/; do ( cd "$e" &&
 "$executables_dir"/./tblade3 3dbgbinput.*.dat );
 done); done>>caserun.log

echo " Part B : Geometry Files Created " |tee -a caserun.log
echo "    " |tee -a caserun.log
echo "    " |tee -a caserun.log
echo " -----------------------------------------------"|tee -a caserun.log
echo "  >>>>>     MODULE 3 : Multirow 'GeomTurbo' files Generation " |tee -a caserun.log
echo " -----------------------------------------------" |tee -a caserun.log
echo "	"
echo " Part A : Creating individual geomTurbo files ..." |tee -a caserun.log

for f in ./row*/; do ( cd "$f" && for g in ./*/; do ( cd "$g" &&
"$executables_dir"/./geomturbo 3dbgbinput.*.dat 241 );
done); done>>caserun.log
echo "  "

# # echo "Changing the geomTurbo file names    "
for h in ./row*/; do ( cd "$h" && for i in *; do mv $i/*.geomTurbo row.$i.geomTurbo; done;) done>>caserun.log

# # move all geomTurbo files to main directory
for h in ./row*/; do ( mv $h/row.*.*.geomTurbo ./;) done>>caserun.log

# # 
# ##ls -1 *.geomTurbo | sort -n

echo " Part B : Combining all geomTurbo files for multi-row analysis"

chmod +x "$scripts_dir"/multirowGeomturbo_v0.2.py 
"$scripts_dir"/multirowGeomturbo_v0.2.py |tee -a caserun.log
echo "  "

# #clean up the directory with from geomTurbo files
rm row.*.*.geomTurbo | >>/dev/null

echo " Part C : multi-row geomTurbo file generated " |tee -a caserun.log

# # python nax2_m_theta.py

echo "" 

echo " -----------------------------------------------" |tee -a caserun.log
duration=$SECONDS
echo "    Total Run Time :" |tee -a caserun.log
echo "    $(($duration / 60)) minutes and $(($duration % 60)) seconds ." |tee -a caserun.log
echo " -----------------------------------------------"|tee -a caserun.log
echo " -----------------------------------------------"|tee -a caserun.log
echo " " |tee -a caserun.log
echo "  	NAX Run Complete !" |tee -a caserun.log
echo " -----------------------------------------------" |tee -a caserun.log
echo " -----------------------------------------------" |tee -a caserun.log