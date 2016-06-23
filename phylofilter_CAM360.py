#! /usr/bin/env python

# This script will utilize the list of diatom or stramenopile genera (diatom.list and stramenopile.list) 
# along with a FASTA file input.  The user will specify whether to filter the input FASTA for stramenopiles
# or diatoms, which will then check against the list of genera in the .list file.

import sys
import re
from Bio import SeqIO

# input: FASTA, 'diatom' or 'stramenopile'
FastaName = sys.argv[1]
FilterType = sys.argv[2]

if FilterType == 'diatom':
	ListString = r'/share/projects/diatom_est/annotation/scripts/phylo_lists/CAM360/AllDiatom.list'
elif FilterType == 'stramenopile':
	ListString = r'/share/projects/diatom_est/annotation/scripts/phylo_lists/CAM360/AllStramenopile.list'
else:
	print "Usage: phylofilter.py FASTA_file type"
	print "Where type = diatom or stramenopile"
	sys.exit(2)

# load infiles
InFASTA = open(FastaName, 'r')
InList = open(ListString, 'r')

# load outfile
OutString = r"\1." + FilterType + ".fasta"
OutFileName = re.sub(r"(.+)\.fasta",OutString,FastaName)
OutFile = open(OutFileName,'w')

# create dictionary with genera names as key values
PhyloDict = {}
for Entry in InList:
	CleanedEntry = Entry.strip() # remove whitespace
	if CleanedEntry not in PhyloDict: # if it's not already there...
		PhyloDict[CleanedEntry] = 1 # add the entry to the dictionary w arbitrary value

for record in SeqIO.parse(InFASTA, 'fasta'):
	RecordID = record.id
	GSID = "Null"
	LineElements = RecordID.split("_") # separate the ID by underscore
	for item in LineElements:
		if item.find("MMETSP") >= 0: # Find and collect the grindstone id (MMETSP####)
			GSID = item.strip()
	if GSID in PhyloDict:
		SeqIO.write(record, OutFile, "fasta")   # if it's in the list, write it out

# close it all!
InFASTA.close()
InList.close()
OutFile.close()
