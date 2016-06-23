#!/usr/bin/env python

# HMM search . . . 
# resultant FASTA returns CAMPEP_#
# resultant OHS returns CAMPEP_# & MMETSP grindstone
# create dict {cp:ncgr}

import re
import sys

# determine file inputs
JobName = sys.argv[1]
InFASTA = JobName + ".hma.fasta"
InOHS = JobName + ".ohs"

# load the .hma.fasta and .ohm
ThisFASTA = open(InFASTA, 'r')
ThisOHS = open(InOHS, 'r')

# create output file, *.hma.fasta.fn
OutFileName = InFASTA + ".fn"
OutFile = open(OutFileName,'w')


# open and parse fixed CAMERA metadata file, create dictionary of MMETSP# & Binomials
MetadataPath = "/home/rgrous83/scripts/CAM-139_BinomialGrindstone.csv"
Metadata = open(MetadataPath,'r')
MetaDict={}
for Line in Metadata:
	DataList = Line.split(",")
	BinomialName = DataList[0]
	RawGrindstoneID = DataList[1]
	FixedGrindstoneID = re.sub(r'(MMETSP\d{4})\r\n',r'\1',RawGrindstoneID)
	MetaDict[FixedGrindstoneID] = BinomialName

Metadata.close()
	

# declare regular expression terms
# /NCGR_PEP_ID=MMETSP0947-20121206|21202_1
GrindstoneFindString = r'\/NCGR_PEP_ID\=MMETSP(\d{4}).+'
# MMETSP0947
GrindstoneFixString = r'MMETSP\1'
# CAMPEP_0117686320
CampepFindString = r'CAMPEP_(\d{10})'
CampepFixString = r'cp\1'


# Create dictionary to store OHS values
ohsDict={}
# for line in ohs
for ThisLine in ThisOHS:
	if ThisLine.startswith(">>"):
		LineList = ThisLine.split()
		RawCampepID = LineList[1]
		FixedCampepID = re.sub(CampepFindString,CampepFixString,RawCampepID)
		RawGrindstoneID = LineList[2]
		FixedGrindstoneID = re.sub(GrindstoneFindString,GrindstoneFixString,RawGrindstoneID)
		Binomial = MetaDict[FixedGrindstoneID]
		ohsDict[FixedCampepID] = Binomial
            
# Use these dictionaries to replace individual campep ids with binomial & campep
for Line in ThisFASTA:
	if Line.startswith(">"):
		ThisCampep = Line.replace(">","")
		NewCampepID = re.sub(r'CAMPEP_(\d{10})\n',CampepFixString,ThisCampep) 
		NewLine = ">" + ohsDict[NewCampepID] + "_" + NewCampepID + '\n'
		OutFile.write(NewLine)
	else:
		OutFile.write(Line)

		
ThisFASTA.close()
ThisOHS.close()
OutFile.close()