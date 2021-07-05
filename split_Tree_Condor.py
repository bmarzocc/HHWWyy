#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
import itertools
from optparse import OptionParser
import operator
import os

def replaceString(fileName,inputFile):
  with open(fileName) as f:
    newText=f.read().replace('INPUTFILE', inputFile)
  with open(fileName, "w") as f:
    f.write(newText)


if __name__ == '__main__':


  parser = OptionParser()
  parser.add_option( "-i", "--inList", dest="inList", default="", type="string", help="inList" )
  (options, args) = parser.parse_args() 

  inList = options.inList
  print "inList:",inList
  
  local = os.getcwd()
  if not os.path.isdir('error'): os.mkdir('error') 
  if not os.path.isdir('output'): os.mkdir('output') 
  if not os.path.isdir('log'): os.mkdir('log') 
   
  # Prepare condor jobs
  condor = '''executable              = run_script.sh
output                  = output/strips.$(ClusterId).$(ProcId).out
error                   = error/strips.$(ClusterId).$(ProcId).err
log                     = log/strips.$(ClusterId).log
transfer_input_files    = run_script.sh
on_exit_remove          = (ExitBySignal == False) && (ExitCode == 0)
periodic_release        = (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > (60*60))
    
+JobFlavour             = "workday"
+AccountingGroup        = "group_u_CMS.CAF.ALCA"
queue arguments from arguments.txt
'''

  with open("condor_job.txt", "w") as cnd_out:
     cnd_out.write(condor)

  outputDir = os.getcwd()

  script = '''#!/bin/sh -e

JOBID=$1; 
LOCAL=$2; 
LIST=$3; 

echo -e "Select category"
cd ${LOCAL}/
eval `scramv1 ru -sh`
python split_Tree.py -i ${LIST}

echo -e "DONE";
'''
  arguments=[]
  with open(str(inList)) as f_List:
    data_List = f_List.read()
  lines_List = data_List.splitlines() 
  for i,line in enumerate(lines_List):
    if(line.find("#") != -1):
       continue
    print "JobID ",i,": ",line  
    arguments.append("{} {} {}".format(i,local,line))  

  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments)) 
  with open("run_script.sh", "w") as rs:
     rs.write(script) 
   
