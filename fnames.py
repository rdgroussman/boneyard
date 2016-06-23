#!/usr/bin/env python

# This script will change the headers in a fasta file to a friendlier format (>Genus_species_UniqID)
# Currently has support for CAMERA, MMETSP, UniProt, and select transcriptomes/ORFs

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
# Fracy = Fragilariopsis cylindrus
# Thaps = Thalassiosira pseudonana
# Phaeo = Phaeodactylum tricornutum
# Psemu = Pseudo-nitzschia multiseries
# Esili = Ectocarpus siliculosis
# Ehux = Emiliania huxleyi
# UP = UniProt or SwissProt
# Synac = Synedra acus 

# load the in-file
InFile = open(InFileName, 'r')

# open the out file
OutFileName = InFileName + ".fn"
OutFile = open(OutFileName,'w')

# declare regexp terms
FindString = r'^>.*CAMPEP_(\w+) \/NCGR_PEP_ID\=MMETSP\w+\-\w+\|\w+ \/TAXON_ID=\w+ /ORGANISM="(.{1,})" /LENGTH.+$'
ReplaceString = r'>\2_cp\1'
VannellaString = r'^>.*CAMPEP_(\d+) \/NCGR_PEP_ID=MMETSP0168-20121206.+$'
VannellaFixString = r'>Vannella_sp_cp\1'
GymnodiniumString = r'^>.*CAMPEP_(\d+) \/NCGR_PEP_ID=MMETSP0784-20121206.+$'
GymnodiniumFixString = r'>Gymnodinium_catenatum_cp\1'
StrainFindString = r'^>([A-Z][a-z-]+)_([a-z]+)_.+_(cp\d+)$'
StrainFixString = r'>\1_\2_\3'
UPFindString = r'^>(\w{2})\|(\w{6}).+OS\=(\w+) (\w+).+$'
UPReplaceString = r'>\3_\4_\1\2'

# use this to chop or keep strain for select samples
KeepStrain = False

# run through each line
for Line in InFile:
	
	# Could be made more efficient here by if statement acting only on lines that begin with ">"
	
	# Run through CAMERA-formatted headers
	if HeaderType == "CAMERA":
		
		# Fix unclassified species
		if Line.find("MMETSP1329") >= 0:
			NewLine = re.sub(FindString,r'>Unclassified_pelagophyte_cp\1',Line)
		if Line.find("MMETSP1310") >= 0:
			NewLine = re.sub(FindString,r'>Unclassified_prasinophyte_cp\1',Line)
		if Line.find("MMETSP1178") >= 0:
			NewLine = re.sub(FindString,r'>Phaeocystis_sp_cp\1',Line)
				
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
		 
		# Identify if strain should be chopped off
		if NewLine.startswith(('>Amphiprora','>Leptocylindrus','>Skeletonema')):
			KeepStrain = True
		  
		 
		# Remove strain information unless otherwise specified
		if KeepStrain == False:
				NewLine = re.sub(StrainFindString,StrainFixString,NewLine)
		KeepStrain = False # reset KeepStrain
			
	# run through each line for all 31 MMETSP peptides
	if HeaderType == "MMETSP":
		NewLine = Line
		# MMETSP_all
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
		NewLine = re.sub(r"^>.*MMETSP0009_2-\d{8}\|(\d+).+$",r">Grammatophora_oceanica_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0794_2-\d{8}\|(\d+).+$",r">Stephanopyxis_turris_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1362-\d{8}\|(\d+).+$",r">Leptocylindrus_CCMP1586_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1394-\d{8}\|(\d+).+$",r">Asterionellopsis_glacialis_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1423-\d{8}\|(\d+).+$",r">Pseudo-nitzschia_hemeii_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1360-\d{8}\|(\d+).+$",r">Licmophora_sp_\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1361-\d{8}\|(\d+).+$",r">Nanofrustulum_sp_\1",NewLine)
		
		
	# fix P. granii
	if HeaderType == "Pgr":
		NewLine = Line
		NewLine = re.sub(r"^>(.+)$",r">Pseudo-nitzschia_granii_\1",NewLine)
       
       
    # fix UniProt FASTA headers
    # organisms names with a hyphen (eg Pseudo-nitzchia) need to be fixed in regexp term
	if HeaderType == "UP":
		NewLine = re.sub(UPFindString,UPReplaceString,Line)

    # Fragilariopsis cylindrus
    # set to accept input from /share/data/seq/organisms/Fragilariopsis_cylindrus/genome/Fracy1_GeneModels_FilteredModels2_aa.shortID.fasta
	if HeaderType == "Fracy":
		NewLine = re.sub(r"^>(\d+)$",r">Fragilariopsis_cylindrus_jgi\1",Line)

        
    # Thalassiosira pseudonana
    # set to accept from /share/data/seq/organisms/Thalassiosira_pseudonana/genome/Thaps3_geneModels_FilteredModels2_aa.fasta
	if HeaderType == "Thaps":
		NewLine = re.sub(r"^>jgi\|Thaps3\|(\d+)\|.+$",r">Thalassiosira_pseudonana_jgi\1",Line)
        
    # Phaeodactylum tricornutum
    # set to accept from /share/data/seq/organisms/Phaeodactylum_tricornutum/genome/Phatr2.FilteredModels2_aa.fasta
	if HeaderType == "Phaeo":
		NewLine = re.sub(r"^>jgi\|Phatr2\|(\d+)\|.+$",r">Phaeodactylum_tricornutum_jgi\1",Line)
        
    # Pseudo-nitzschia multiseries
    # set to accept from /share/data/seq/organisms/Pseudo-nitzschia_multiseries/genome/Psemu1_GeneCatalog_proteins_20111011.aa.fasta-idcleaned
	if HeaderType == "Psemu":
		NewLine = re.sub(r"^>\w{3}\|Psemu1\|(\d+).+$",r">Pseudo-nitzschia_multiseries_jgi\1",Line)
        
    # Ectocarpus siliculosis
    # set to accept from /share/data/seq/organisms/Ectocarpus_siliculosus/genome/Ectsi_prot_LATEST.tfa-idcleaned
	if HeaderType == "Esili":
		NewLine = re.sub(r"^>\w{3}\|EsiliProt\|(\w+).+$",r">Ectocarpus_siliculosus_\1",Line)
        
    # Emiliania huxleyi
    # accept from /share/data/seq/organisms/Emiliana_huxleyi/jgi_annotation/v1/Emihu1_best_proteins.fasta-idcleaned
	if HeaderType == "Ehux":
		NewLine = re.sub(r"^>\w{3}\|Ehux1best\|(\w+).+$",r">Emiliania_huxleyi_jgi\1",Line)
		
	# Synedra acus
	# /share/data/seq/organisms/Synedra_acus/genome/sac.proteins.fasta
	if HeaderType == "Synac":
		NewLine = re.sub(r">(\d+)",r">Synedra_acus_\1",Line)
    
        
	OutFile.write(NewLine)
    
InFile.close()
OutFile.close()