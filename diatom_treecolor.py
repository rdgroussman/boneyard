#! /usr/bin/env python

import sys
import re

XMLName = sys.argv[1]

RadialCentricListFile = r'/share/projects/diatom_est/annotation/scripts/phylo_lists/radialcentric.list'
PolarCentricListFile = r'/share/projects/diatom_est/annotation/scripts/phylo_lists/polarcentric.list'
AraphidPennateListFile = r'/share/projects/diatom_est/annotation/scripts/phylo_lists/araphidpennate.list'
RaphidPennateListFile = r'/share/projects/diatom_est/annotation/scripts/phylo_lists/raphidpennate.list'

# load infiles
InXML = open(XMLName, 'r')

# load list files
RadialCentricList = open(RadialCentricListFile, 'r')
PolarCentricList = open(PolarCentricListFile, 'r')
AraphidPennateList = open(AraphidPennateListFile, 'r')
RaphidPennateList = open(RaphidPennateListFile, 'r')

# declare color settings for each group

# for black background:
# DiatomColorString = r"<color><red>255</red><green>102</green><blue>0</blue></color>"
# NonDiatomStramenopileColorString = r"<color><red>255</red><green>255</green><blue>0</blue></color>"
# GreenColorString = r"<color><red>0</red><green>255</green><blue>0</blue></color>"
# RedColorString = r"<color><red>255</red><green>0</green><blue>0</blue></color>"

# for a white background:
RadialCentricColorString = r"<color><red>255</red><green>0</green><blue>0</blue></color>"
PolarCentricColorString = r"<color><red>255</red><green>102</green><blue>0</blue></color>"
AraphidPennateColorString = r"<color><red>0</red><green>153</green><blue>0</blue></color>"
RaphidPennateColorString = r"<color><red>0</red><green>0</green><blue>255</blue></color>"


# expand with stramenopiles, chlorlophytes, dinos, etc.

# load outfile
OutString = r"\1." + "diatom_color.xml"
OutFileName = re.sub(r"(.+)\.xml",OutString,XMLName)
OutFile = open(OutFileName,'w')

# create dictionary with genera names as key values
RadialCentricDict = {}
for Entry in RadialCentricList:
	CleanedEntry = Entry.strip() # remove whitespace
	if CleanedEntry not in RadialCentricDict: # if it's not already there...
		RadialCentricDict[CleanedEntry] = 1 # add the entry to the dictionary w arbitrary value
        
PolarCentricDict = {}
for Entry in PolarCentricList:
	CleanedEntry = Entry.strip() # remove whitespace
	if CleanedEntry not in PolarCentricDict: # if it's not already there...
		PolarCentricDict[CleanedEntry] = 1 # add the entry to the dictionary w arbitrary value

AraphidPennateDict = {}
for Entry in AraphidPennateList:
	CleanedEntry = Entry.strip() # remove whitespace
	if CleanedEntry not in AraphidPennateDict: # if it's not already there...
		AraphidPennateDict[CleanedEntry] = 1 # add the entry to the dictionary w arbitrary value
       
RaphidPennateDict = {}
for Entry in RaphidPennateList:
	CleanedEntry = Entry.strip() # remove whitespace
	if CleanedEntry not in RaphidPennateDict: # if it's not already there...
		RaphidPennateDict[CleanedEntry] = 1 # add the entry to the dictionary w arbitrary value



xmlLineCount = 0	# count the progression of lines in the xml
InsertColorHere = 0 # this will be used to insert the color tag

for line in InXML:
	if xmlLineCount not in {0,1,2,3}: #skip the first four lines; internal file name also uses <name>
		if line.find("<name>") >= 0: # if <name> is found on the line
			LineElements = line.split("_") # separate the ID by underscore
			RawGenus = LineElements[0] # Capture the genus
			RawGenus = RawGenus.strip() # remove whitespace
			Genus = RawGenus.replace("<name>","") # remove <name>
			if str(Genus) in RadialCentricDict:
				InsertColorHere = xmlLineCount + 2
				ColorString = RadialCentricColorString
			if str(Genus) in PolarCentricDict:
				InsertColorHere = xmlLineCount + 2
				ColorString = PolarCentricColorString
			if str(Genus) in AraphidPennateDict:
				InsertColorHere = xmlLineCount + 2
				ColorString = AraphidPennateColorString
			if str(Genus) in RaphidPennateDict:
				InsertColorHere = xmlLineCount + 2
				ColorString = RaphidPennateColorString
		elif line.find("<branch_length>") == -1 and InsertColorHere > xmlLineCount: # if branch length is not indicated we'll need to insert the color string earlier
			InsertColorHere -= 1
			
			if xmlLineCount == InsertColorHere:
			OutFile.write(ColorString)
				
	OutFile.write(line)
	xmlLineCount += 1 # increment the loop counter by one
	
	
	
# close it all!
#in file
#lists
InXML.close()
OutFile.close()
