#!/usr/bin/env python

import Bio
from Bio import Phylo
from Bio import Nexus
import sys
import re


# this script will take an input raw figtree and:
# add half-radial style elements:
#	mid-point rooting
#	aligned labels
#	radial orientation
# remove bootstrap values under 50 (or 0.5 or likewise)
# capture the node label:
#	remove MMETSP# and place in special comment
#	create a name comment, remove underscores from name special comment
#	give the taxa label OR node a color based on MMETSP grouping
#		extending color to deeper nodes if all descendents share color

# collect input
InFigtree = sys.argv[1]
Figtree = open(InFigtree, 'r')

# determine outfile
OutFileName = InFigtree + ".prettyfig.nx"
OutFile = open(OutFileName,'w')

# load tab delimited file containing list and color information
TCInfoPath = "/share/projects/diatom_est/annotation/scripts/figtree/CAM360_scheme.csv" 
TCInfo = open(TCInfoPath, 'r')
TCInfoDict = {} # treecolor information dictionary
for line in TCInfo:
	linesplit = line.split("\t")	# tab delimited file
	ListFile = linesplit[0]	# the group name file
	ListFilePath = r'/share/projects/diatom_est/annotation/scripts/phylo_lists/CAM360/' + ListFile.strip()
	GroupName = ListFile.split(".")	# pop off the prefix
	NCGRFile = open(ListFilePath, 'r') # open the list file
	NCGRList = []
	for item in NCGRFile: # create a list of MMETSP# from each list file
		item = item.strip()
		NCGRList.append(item)
	GroupName = GroupName[0] # Name of group
	ColorVal = linesplit[1] # Collect that funky value that Figtree uses.  
	ColorString = ",!color=#" + ColorVal.strip()
	TCInfoDict[GroupName] = (ColorString,NCGRList) # Color values and MMETSP# assigned as values to group names

# scan through taxa labels:
taxa_code = False	# toggle when we iterate through this section

for line in Figtree:
	if line.strip() == "begin taxa;":
		taxa_code = True
	if taxa_code == True:
		if line.find("_MMETSP") >= 0: # if we find an MMETSP# here
			GSID = re.sub(r".+(MMETSP\d{4}).+",r"\1",line)
			GSID_trimtag = "_" + GSID
			GSIDNumber = GSID.replace("MMETSP","")
			TrimmedName = line.replace(GSID_trimtag.strip(),"")
			for Group in TCInfoDict.keys(): # search through the tc info dict for presence of GSID
				GroupList = TCInfoDict[Group]
				if GSID.strip() in GroupList[1]: # if the GSID is in a list belonging to one of the groups, return the color value for that group
					ColorValue = GroupList[0]
					CommentHandle = '[&!name="' + TrimmedName.strip() + '"' + ColorValue + ',!MMETSP="' + GSIDNumber.strip() + '"]'
					line = line + CommentHandle
			# create a 'name' value without the grindstone
	if line.strip () == "end;":
		taxa_code = False

#	Emiliania_huxleyi_jgi358500[&!name="Ehux_test",!color=#-65485,!MMETSP="0000"]


	OutFile.write(line)

#	remove MMETSP# and place in special MMETSP comment
#	create a name comment, remove underscores from name special comment
#	give the taxa label a color based on MMETSP grouping
#
#	if I can figure it out, I'd like to color branches instead
#		extending color to deeper nodes if all descendents share color



# import tree
# tree = Phylo.read(Figtree,"nexus")
# print tree.name
# print tree
# for node in tree.get_terminals():
	# print node.name
# for node in tree.get_nonterminals():
	# print node.get_data()
	# print node.name
# for clade in tree.find_clades():
	# if clade.name:
		# print clade.name

###

# internal: Clade(comment='[&bootstrapvalues=57]', branch_length=1.20657828706e-06)
# terminal: Clade(branch_length=1.20657828706e-06, name='Ostreococcus_mediterraneus_MMETSP0927_cp0174464132')

# def lookup_by_names(tree):
    # names = {}
    # for clade in tree.find_clades():
        # if clade.name:
            # if clade.name in names:
                # raise ValueError("Duplicate key: %s" % clade.name)
            # names[clade.name] = clade
    # return names
	
# lookup_by_names(tree)
# for thing in names:
	# print names[thing]

# help(Nexus.Nodes.Node)
# http://biopython.org/wiki/Phylo_cookbook
# http://seqanswers.com/forums/archive/index.php/t-20301.html

# remove bootstrap values under 50 (or 0.5 or likewise)


# add half-radial style elements:
#	mid-point rooting
#	aligned labels
#	radial orientation










# ----------- PSEUDOCODE BELOW ----------------


# #figtree half-radial

# # add MMETSP# to node comments, remove from label

# Pyrodinium_bahamense_cp0179036890[&!name="Checko",!color=#-65485,!MMETSP="2323"]

# ie,
# Cryptomonas_curvata_cp0172156560[&!name="Barfo",!MMETSP="2323"]

# # remove bootstrap values < 50
# find treeline
# capture treeline
# search treeline
# find [&"bootstrap values"=99]
# if value < 50
	# value = ""
# search for names with MMETSP\d{4}
# if name is in a grouplist,
	# give it [&!color=#-\d{8}]
	# where \d{8} = color of grouplist
# remove "MMETSP\d{4}_"

# # manual
# collapse and label unnecessary/excessive nodes
# after collapsing, correct to half-radial
# find tip labels to be removed; annotate with "NOTHING"
# in .figtree file, replace "NOTHING" with ""

# # remove underscores in illustrator. assuming figtree gives PDF gives in text.
