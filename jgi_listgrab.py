#! /usr/bin/env python

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
	JGIElements = record.id.split("|") # separate the ID by pipe character
	ProteinID = JGIElements[2] # Capture the protein ID
	if ProteinID in ListDict:
		SeqIO.write(record, OutFile, "fasta")   # if it's in the list, write it out

# close it all!
InFASTA.close()
InList.close()
OutFile.close()
