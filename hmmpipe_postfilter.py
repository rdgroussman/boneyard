#!/usr/bin/env/ python

# This script is designed to be run in *.allhits.raw.fasta file that is output by hmmpipe_fullseqs.sh

# Functions: remove redundant sequences between CAMERA and MMETSP transcriptome sets.  Universal CAMERA ID will be kept in favor of NCGR ID.

# Using a list of redundant MMETSP transcriptomes (MMETSP-139 to MMETSP_all)
# If the MMETSP#### is on that list, it will not be kept

