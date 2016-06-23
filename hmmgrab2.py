#!/usr/bin/env python

# This script utilizes the .ohs output of runHmmsearch3_hmmgrab2.py (written by Erick Matsen, modified by Ryan Groussman)
# Creates a dictionary of hits which is used to extract full-length sequences from the original FASTA database

import re
import sys
from Bio import SeqIO

# /share/projects/diatom_est/annotation/scripts/hmmgrab2.py

# determine file inputs
# input from hmmpipe_mafft.sh : job.ohs ($1.vs.MMETSP-139) and DBName
JobName = sys.argv[1]
DBName = sys.argv[2]
InOHS = JobName + ".ohs"

# load the .ohs
ThisOHS = open(InOHS, 'r')

# create output file, *.fasta
OutFileName = JobName + ".fasta"
OutFile = open(OutFileName,'w')

# create dictionary to store target hits
HitDict={}

for ThisLine in ThisOHS:
	if ThisLine.startswith(">>"):
		LineList = ThisLine.split()
		RawID = LineList[1]
		HitDict[RawID] = 1
		

# FastaDB = "/share/projects/diatom_est/source_data/CAMERA_peptides/CAM_P_0001000.pep.fa"
# FastaDB = "/share/projects/diatom_est/source_data/MMETSP-29/MMETSP-29_peptides.fa"


f = open(DBName)
for record in SeqIO.parse(f, 'fasta'):
    if record.id in HitDict:
		SeqIO.write(record, OutFile, "fasta")
		# OutHeader = ">" + str(record.id) + "\n"
		# OutSeq = str(record.seq) + "\n"
		# OutFile.write(OutHeader)
		# OutFile.write(OutSeq)
f.close()
		

# close infile
# close outfile
ThisOHS.close()
OutFile.close()