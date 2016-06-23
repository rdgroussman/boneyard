#! /usr/bin/env python

# This little script will take a .csv file produced by guppy to_csv as input
# Will filter for posterior probability values under a given value

import sys
import re

# load infile
CSVName = sys.argv[1]
InCSV = open(CSVName, 'r')

# load outfile
OutString = r"\1." + "postprob_filtered.csv"
OutFileName = re.sub(r"(.+)\.csv",OutString,CSVName)
OutFile = open(OutFileName,'w')

# collect desired maximum posterior probability value
probmax = raw_input("Posterior probability cut-off?  ")

for line in InCSV:
	elements = line.split(",")
	postprob = elements[5]
	if postprob < probmax:
		OutFile.write(line)

OutFile.close()
InCSV.close()
