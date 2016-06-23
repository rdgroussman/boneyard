#!/usr/bin/env python

# Using the CAMERA supplied metadata in CSV format (ie CAM_P_0001000.csv)
# CSV file needs to be 'cleaned', added lines and blank fields must be corrected
# Leave only four fields: SAMPLE_ACC	SAMPLE_DESCRIPTION	SAMPLE_NAME	TAXON_ID
# This script will retrieve and store taxonomy and lineage information in a new CSV file
# /share/projects/diatom_est/annotation/scripts/taxgrab.py

import sys
from Bio import Entrez
Entrez.email = "rgroussman@gmail.com"

# Open the in & out files
InFileName = sys.argv[1]
CAMERA_csv = open(InFileName, 'r')

OutFileName = "CAM360_tax.csv" # for this most recent run
OutFile = open(OutFileName,'w')


CAMERA_csv.readline()   # skip the first line
for Line in CAMERA_csv:
	#parse the line - extract NCGR grindstone, binomial, and taxon id
	LineList = Line.split(",")
	BinomialID = LineList[1]
	GrindstoneID = LineList[2]
	TaxonID = LineList[3]
	
	# retrieve taxonomy information for each TaxonID from NCBI
	# skip if TaxonID == 0
	if TaxonID > 0:
		handle = Entrez.efetch(db="Taxonomy", id=TaxonID, retmode="xml")
		records = Entrez.read(handle)
		Lineage = records[0]["Lineage"]
	elif TaxonID == 0:
		Lineage = "No TaxonID given"
		
	# this is just a test
	BackTogether = BinomialID + "\t" + GrindstoneID + "\t" + TaxonID + "\t" + Lineage + "\n"
	OutFile.write(BackTogether)


# close infile & outfile
CAMERA_csv.close()
OutFile.close()