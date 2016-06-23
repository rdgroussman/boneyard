#!/usr/bin/env python

import re
import sys

# declare infile name
InFileName = sys.argv[1]
HeaderType = sys.argv[2]

# """
# fnames.py InFileName HeaderType

# Header types:
# CAMERA = CAMERA peptides
# MMETSP = NCGR MMETSP grindstone names
# Pgr = P. granii
# UP = UniProt or SwissProt
# """

# load the in-file
InFile = open(InFileName, 'r')

# open the out file
OutFileName = InFileName + ".fn"
OutFile = open(OutFileName,'w')

# declare regexp terms
FindString = r'^>lcl\|CAMPEP_(\w+) \/NCGR_PEP_ID\=MMETSP\w+\-\w+\|\w+ \/TAXON_ID=\w+ /ORGANISM="(.{1,})" /LENGTH.+$'
ReplaceString = r'>\2_cp\1'
VannellaString = r'^>lcl\|CAMPEP_(\d+) \/NCGR_PEP_ID=MMETSP0168-20121206.+$'
VannellaFixString = r'>Vannella_sp_cp\1'
GymnodiniumString = r'^>lcl\|CAMPEP_(\d+) \/NCGR_PEP_ID=MMETSP0784-20121206.+$'
GymnodiniumFixString = r'>Gymnodinium_catenatum_cp\1'
StrainFindString = r'^>([A-Z][a-z-]+)_([a-z]+)_.+_(cp\d+)$'
StrainFixString = r'>\1_\2_\3'
UPFindString = r'^>(\w{2})\|(\w{6}).+OS\=(\w+) (\w+).+$'
UPReplaceString = r'>\3_\4_\1\2'

# run through each line
for Line in InFile:
	
	# Run through CAMERA-formatted headers
	if HeaderType == "CAMERA":
		
		# Fix most headers
		NewLine = re.sub(FindString,ReplaceString,Line)
		
		# Fix Vannella and Gymnodinium_catenatum
		NewLine = re.sub(VannellaString, VannellaFixString, NewLine)
		NewLine = re.sub(GymnodiniumString, GymnodiniumFixString, NewLine)
		
		# Remove commas and periods, replace spaces with underscores
		NewLine = re.sub("\,","",NewLine)
		NewLine = re.sub("\.","",NewLine)
		NewLine = re.sub(" ","_",NewLine)
		
		# Fix Paraphysomonas and Pteridomonas
		NewLine = re.sub(r"^>Paraphysomonas_Paraphysomonas_imperforata_Strain_PA2_cp(\d+)$",r">Paraphysomonas_imperforata_cp\1",NewLine)
		NewLine = re.sub(r"^>Pteridomonas_Pteridomonas_Strain_PT_cp(\d+)$",r">Pteridomonas_sp_cp\1",NewLine)
		 
		# Remove strain information by default
		NewLine = re.sub(StrainFindString,StrainFixString,NewLine)
		
			
	# run through each line for MMETSP peptides
	if HeaderType == "MMETSP":
		NewLine = Line
		NewLine = re.sub(r"^>.*MMETSP0010_2-\d{8}\|(\d+).+$",r">Corethron_hystrix_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0789-\d{8}\|(\d+).+$",r">Rhizosolenia_setigera_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1064-\d{8}\|(\d+).+$",r">Aulacoseira_subarctica_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1066-\d{8}\|(\d+).+$",r">Coscinodiscus_wailesii_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0015_2-\d{8}\|(\d+).+$",r">Odontella_sp_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0013_2-\d{8}\|(\d+).+$",r">Skeletonema_costatum_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1057-\d{8}\|(\d+).+$",r">Cyclotella_meneghiniana_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1058-\d{8}\|(\d+).+$",r">Detonula_confervacea_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1059-\d{8}\|(\d+).+$",r">Thalassiosira_sp_FW_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1062-\d{8}\|(\d+).+$",r">Ditylum_brightwellii_Pop1_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1063-\d{8}\|(\d+).+$",r">Ditylum_brightwellii_Pop2_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1067-\d{8}\|(\d+).+$",r">Thalassiosira_punctigera_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1070-\d{8}\|(\d+).+$",r">Minutocellus_polymorphus_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1071-\d{8}\|(\d+).+$",r">Thalassiosira_sp_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0800-\d{8}\|(\d+).+$",r">Striatella_unipunctata_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0786-\d{8}\|(\d+).+$",r">Thalassionema_frauenfeldii_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0017_2-\d{8}\|(\d+).+$",r">Cylindrotheca_closterium_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0014_2-\d{8}\|(\d+).+$",r">Nitzschia_sp_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1060-\d{8}\|(\d+).+$",r">Pseudo-nitzschia_pungens_cingulata_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1061-\d{8}\|(\d+).+$",r">Pseudo-nitzschia_pungens_pungens_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1065-\d{8}\|(\d+).+$",r">Amphiprora_sp_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1068-\d{8}\|(\d+).+$",r">Pseudopedinella_elastica_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0785-\d{8}\|(\d+).+$",r">Bolidomonas_pacifica_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0011_2-\d{8}\|(\d+).+$",r">Rhodosorus_marinus_\1",NewLine)
		
	# fix P. granii
	if HeaderType == "Pgr":
		NewLine = Line
		NewLine = re.sub(r"^>lcl\|(\w+) .+$",r">Pseudo-nitzschia_granii_\1",NewLine)
       
       
    # fix UniProt FASTA headers
    # organisms names with a hyphen (eg Pseudo-nitzchia) need to be fixed in regexp term
	if HeaderType == "UP":
		NewLine = re.sub(UPFindString,UPReplaceString,Line)

	OutFile.write(NewLine)
    
InFile.close()
OutFile.close()
