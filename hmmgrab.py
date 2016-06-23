#!/usr/bin/env python

import re
import sys

# /share/projects/diatom_est/annotation/scripts/hmmgrab.py

# determine file inputs
# input from hmmpipe.sh : job.ohs ($1.vs.MMETSP-139)
JobName = sys.argv[1]
InOHS = JobName + ".ohs"

# load the .ohs
ThisOHS = open(InOHS, 'r')

# create output file, *.hitlist
OutFileName = JobName + ".hitlist"
OutFile = open(OutFileName,'w')

for ThisLine in ThisOHS:
	if ThisLine.startswith(">>"):
		LineList = ThisLine.split()
		RawID = LineList[1]
		OutID = RawID + "\n"
		OutFile.write(OutID)
        

# close infile
# close outfile
ThisOHS.close()
OutFile.close()