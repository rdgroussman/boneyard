#!/usr/bin/env python

# This script will change the headers in a fasta file to a friendlier format (>Genus_species_MMETSPID_UniqID)
# Differs from fnames.py in retention of MMETSP grindstone name
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
# GB = GenBank (only certain styles will work)
# """

# load the in-file
InFile = open(InFileName, 'r')

# to do: change output format to #.fn.fasta
# open the out file
OutFileName = InFileName + ".fn"
OutFile = open(OutFileName,'w')

# declare regexp terms
FindString = r'^>.*CAMPEP_(\w+) \/NCGR_PEP_ID\=(MMETSP\d{4}).+\-\w+\|\w+ \/TAXON_ID=\w+ /ORGANISM="(.{1,})" /LENGTH.+$'
ReplaceString = r'>\3_\2_cp\1'
VannellaString = r'^>.*CAMPEP_(\d+) \/NCGR_PEP_ID=MMETSP0168-20121206.+$'
VannellaFixString = r'>Vannella_sp_MMETSP1068_cp\1'
GymnodiniumString = r'^>.*CAMPEP_(\d+) \/NCGR_PEP_ID=MMETSP0784-20121206.+$'
GymnodiniumFixString = r'>Gymnodinium_catenatum_MMETSP0787_cp\1'
StrainFindString = r'^>([A-Z][a-z-]+)_([a-z]+)_.+_(MMETSP\d{4}_cp\d+)$'
StrainFixString = r'>\1_\2_\3'

# use this to chop or keep strain for select samples
KeepStrain = False


# run through each line
for Line in InFile:
	
	# Could be made more efficient here by if statement acting only on lines that begin with ">"
	
	# Run through CAMERA-formatted headers
	# >CAMPEP_0114615072 /NCGR_PEP_ID=MMETSP0168-20121206|5977_1 /TAXON_ID=95228 /ORGANISM="" /LENGTH=203 /DNA_ID=CAMNT_0001826133 /DNA_START=1 /DNA_END=612 /DNA_ORIENTATION=+
	
	if HeaderType == "CAMERA":
		NewLine = Line
		if Line.startswith(">"):
			HeaderList = Line.split(" ")
			RawCAMPEP = HeaderList[0].strip()
			CAMPEP = RawCAMPEP.replace(">CAMPEP_","cp")
			RawNCGR = HeaderList[1].strip()
			NCGR = re.sub(r"/NCGR_PEP_ID=(MMETSP\d{4}).+",r"\1",RawNCGR)
			RawGenus = HeaderList[3].strip()
			RawGenus = RawGenus.replace(",","")
			RawGenus = RawGenus.replace(".","")
			Genus = RawGenus.replace('/ORGANISM="',"")
			RawSpecies = HeaderList[4].strip('"')
			RawSpecies = RawSpecies.replace(",","")
			Species = RawSpecies.replace(".","")
			Organism = Genus + "_" + Species
			
			# Address issues per sample with missing or bizarre organism names
			if NCGR == "MMETSP0168":
				Organism = "Vannella_sp"
			if NCGR == "MMETSP0015":
				Organism = "Odontella_aurita"
			if NCGR == "MMETSP1067":
				Organism = "Thalassiosira_punctigera"
			if NCGR == "MMETSP0160":
				Organism = "Odontella_sinensis"
			if NCGR in ("MMETSP0103","MMETSP0104"):
				Organism = "Paraphysomonas_imperforata"
			if NCGR in ("MMETSP0107","MMETSP0108"):
				Organism = "Goniomonas_pacifica"
			if NCGR == "MMETSP0086":
				Organism = "Unclassified_rhizaria"
			if NCGR in ("MMETSP0105","MMETSP0106"):
				Organism = "Unclassified_choanoflagellate"
			if NCGR == "MMETSP0101":
				Organism = "Pteridomonas_danica"
			if NCGR == "MMETSP0102":
				Organism = "Pteridomonas_danica"
			if NCGR == "MMETSP0087":
				Organism = "Unclassified_rhizaria"
			if NCGR == "MMETSP1167":
				Organism = "Mallomonas_sp"
			if NCGR in ("MMETSP0974","MMETSP0975","MMETSP0976","MMETSP0977"):
				Organism = "Unclassified_pelagophyte"
			if NCGR in ("MMETSP0982","MMETSP0983","MMETSP0984","MMETSP0985"):
				Organism = "Unclassified_pavlovale"
			if NCGR in ("MMETSP0986","MMETSP0987","MMETSP0988","MMETSP0989"):
				Organism = "Unclassified_cryptophyte"
			if NCGR in ("MMETSP0990","MMETSP0991","MMETSP0992","MMETSP0993"):
				Organism = "Unclassified_pedinellale"
			if NCGR in ("MMETSP0367","MMETSP0368","MMETSP0369"):
				Organism = "Scrippsiella_hangoei"
			if NCGR in ("MMETSP0809","MMETSP0810","MMETSP0811"):
				Organism = "Eutreptiella_gymnastica"
			if NCGR in ("MMETSP1141","MMETSP1142","MMETSP1143","MMETSP1144"):
				Organism = "Unclassified_ochromonadaceae"
			if NCGR == ("MMETSP1329"):
				Organism = "Unclassified_pelagophyte"
			if NCGR == ("MMETSP1178"):
				Organism = "Unclassified_phaeocystale"
			if NCGR == ("MMETSP1310"):
				Organism = "Unclassified_prasinophyte"
			if NCGR == ("MMETSP1162"):
				Organism = "Phaeocystis_sp"
			if NCGR == ("MMETSP0784"):
				Organism = "Gymnodinium_catenatum"
			NewLine = ">" + Organism + "_" + NCGR + "_" + CAMPEP + "\n"
			# Any more broken/bizarre organism names:
			
	# run through each line for remaining 7 in-house MMETSP peptides
	if HeaderType == "MMETSP":
		NewLine = Line
		# CEG-7
		NewLine = re.sub(r"^>.*MMETSP0009_2-\d{8}\|(\d+).+$",r">Grammatophora_oceanica_MMETSP0009_pid\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP0794_2-\d{8}\|(\d+).+$",r">Stephanopyxis_turris_MMETSP0794_pid\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1362-\d{8}\|(\d+).+$",r">Leptocylindrus_CCMP1586_MMETSP1362_pid\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1394-\d{8}\|(\d+).+$",r">Asterionellopsis_glacialis_MMETSP1394_pid\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1423-\d{8}\|(\d+).+$",r">Pseudo-nitzschia_heimii_MMETSP1423_pid\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1360-\d{8}\|(\d+).+$",r">Licmophora_sp_MMETSP1360_pid\1",NewLine)
		NewLine = re.sub(r"^>.*MMETSP1361-\d{8}\|(\d+).+$",r">Nanofrustulum_sp_MMETSP1361_pid\1",NewLine)
		
		
	# fix P. granii
	if HeaderType == "Pgr":
		NewLine = Line
		NewLine = re.sub(r"^>(.+)$",r">Pseudo-nitzschia_granii_\1",NewLine)

	# fix UniProt FASTA headers
    # organisms names with a hyphen (eg Pseudo-nitzchia) need to be fixed in regexp term
	if HeaderType == "UP":
		UPFindString = r'^>(\w{2})\|(\w{6}).+OS\=(\w+) (\w+).+$'
		UPReplaceString = r'>\3_\4_\1\2'
		NewLine = re.sub(UPFindString,UPReplaceString,Line)
		
	if HeaderType == "GB":
		# example: >gi|397609992|gb|EJK60605.1| flavodoxin isoform B [Thalassiosira oceanica]
		GBFindString = r'>\w{2}\|\d{8,11}\|\w{2}\|(\w+).+\[(.+)\]'
		GBReplaceString = r'>\2_\1'
		NewLine = re.sub(GBFindString,GBReplaceString,Line)
		NewLine = NewLine.replace(" ","_")

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
    
        
	OutFile.write(NewLine)
    
InFile.close()
OutFile.close()