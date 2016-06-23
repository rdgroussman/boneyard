#! /usr/bin/env python

# This script will take a list of FASTA headers, and retrieve sequences with these headers from a source FASTA file
# >listgrab.py in_fasta header_list out_fasta

import sys
import re
from Bio import SeqIO

# input: FASTA file, sequence list
FastaName = sys.argv[1]
ListName = sys.argv[2]
OutName = sys.argv[3]

# load infiles
InFASTA = open(FastaName, 'r')
InList = open(ListName, 'r')

# load outfile
OutFile = open(OutName,'w')

# create dictionary with listed values as keys
ListDict = {}
for Entry in InList:
	CleanedEntry = Entry.strip() # remove whitespace
	if CleanedEntry not in ListDict: # if it's not already there...
		ListDict[CleanedEntry] = 1 # add the entry to the dictionary w arbitrary value
		
for record in SeqIO.parse(InFASTA, 'fasta'):
	if record.id in ListDict:
		SeqIO.write(record, OutFile, "fasta")   # if it's in the list, write it out

# close it all!
InFASTA.close()
InList.close()
OutFile.close()
