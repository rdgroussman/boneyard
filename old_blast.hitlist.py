#!/usr/bin/env python

import re
import sys

InFileName = sys.argv[1]

# load the in-file
InFile = open(InFileName, 'r')

# open the out file
OutFileName = InFileName + ".hitlist"
OutFile = open(OutFileName,'w')

# run through each line and isolate the ID for the hit
for Line in InFile:
	LineList = Line.split('\t')
	NewLine = LineList[1] + '\n'
	OutFile.write(NewLine)
		 
InFile.close()
OutFile.close()