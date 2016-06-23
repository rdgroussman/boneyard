#!/bin/bash -e
#wget ftp://portal.camera.calit2.net/ftp-links/cam_datasets/projects/assemblies/CAM_P_0001000.pep.fa.gz
# Extract peptides for the following data sets, from email from Sara Bender
# May 28 2013
# - Leptocylindrus danicus var. danicus B650 (MMETSP 0321)
# - Leptoclindrus danicus var. apora B651 (MMETSP 0322)
# - Skeletonema marinoi SM1012 Den-03 (MMETSP 0320)
# - Skeletonema marinoi SM1012 Hels-07 (MMETSP 0319)
# - Pseudo-nitzschia delicatissima B596 (MMETSP 0327)
# - Pseudo-nitzschia arenysensis B593 (MMETSP 0329)
zgrep -E '^>.+MMETSP0321-|MMETSP0322-|MMETSP0320-|MMETSP0319-|MMETSP0327-|MMETSP0329-' CAM_P_0001000.pep.fa.gz | gawk '{print substr($1, 2)}' >target_pep_ids.txt
seqtools subseq -c target_pep_ids.txt <(gunzip -c CAM_P_0001000.pep.fa.gz) >CAMERA_EST.pep.fasta

