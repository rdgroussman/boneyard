#!/usr/bin/env python

import sys
import re
# Call with MFG.tree.xml MFG.csv MFG.jplace
TreeFileName = sys.argv[1]
CSVFileName = sys.argv[2]
JplaceFileName = sys.argv[3]

TreeFile = open(TreeFileName, 'r')
CSVFile = open(CSVFileName, 'r')
JplaceFile = open(JplaceFileName, 'r')

# load outfile (TreeFileName.num.xml)
OutFileName = re.sub(r"(.+)\.xml",r"\1.num.xml",TreeFileName)
OutFile = open(OutFileName,'w')

# tally up the placed reads from the CSV
EdgeDict={}	# create dictionary to store a count of placements to each edge (null is zero)
CSVFile.readline()   # skip the first line# skipping the first line
for line in CSVFile:
	linelist = line.split(",")
	IndEdgeNum = int(linelist[3])
	if EdgeDict.has_key(IndEdgeNum):
		EdgeDict[IndEdgeNum] += 1
	else:
		EdgeDict[IndEdgeNum] = 1

# from the JPLACE,
# read the second line (1) containing the association of seqid with edge number
JplaceLines = JplaceFile.readlines()
JplaceTreeLine = JplaceLines[1]


xmlLineCount = 0	# count the progression of lines in the xml
SeqEdgeDict={}	# create dictionary to store SeqIDs and edge numbers

# extract leaf names from the xml
for line in TreeFile:
	if xmlLineCount not in {0,1,2,3}: #skip the first four lines; internal file name also uses <name>
		if line.find("<name>") >= 0: # if <name> is found on the line
			SeqID = re.sub(r"\s+<name>(.+)<\/name>",r"\1",line) # capture the sequence id
			SeqID = SeqID.replace("\r","") # remove EOL characters
			SeqID = SeqID.replace("\n","") # " " "
			FixedSeqID = SeqID.replace(r"|",r"\|") # escape the pipes in some unedited leaf names
			# search for this id in JplaceTreeLine useing regexp to capture the edgenumber
			# Ditylum_brightwellii_Pop1_22972\:[\d\.]+\{(\d+)\}
			SearchHandle = r"^.+" + FixedSeqID + r"\:[\d\.]+\{(\d+)\}.+$" # create the search handle
			EdgeNum = re.sub(SearchHandle,r"\1",JplaceTreeLine) # use the search handle to comb through the jplace line 2 for the edge number
			SeqEdgeDict[SeqID] = EdgeNum
			
			# NOW, if EdgeNum is in EdgeDict, replace the </name>$ with _(EdgeCount)</name>\r\n
			if EdgeDict.has_key(int(EdgeNum)):
				EdgeCount = str(EdgeDict[int(EdgeNum)])
				print SeqID + " has placed reads: " + EdgeCount
				ReplaceHandle = "_(" + EdgeCount + ")</name>\r\n"
				line = line.replace("</name>",ReplaceHandle)
							
	# write the line out to outfile
	OutFile.write(line)
	xmlLineCount += 1 # increment the loop counter by one

# close everything
OutFile.close()
TreeFile.close()
CSVFile.close()
JplaceFile.close()