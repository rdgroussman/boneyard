#!/bin/bash

# pppipe.sh : pplacer pipeline shell script

# Last updated 12 August 2013, 2:05pm by RG
# $1 represents the job name
# have your reference alignment ready in the format job.aln.fasta (trimmed FASTA alignment file)

# Build tree with FastTree, creating a log file
/share/apps/bin/FastTree -log $1.tree.log $1.aln.fasta > $1.tree

# Make reference package
taxit create -l nod -P $1.refpkg --aln-fasta $1.aln.fasta --tree-stats $1.tree.log --tree-file $1.tree

# Convert to hmm profile
~/scripts/hmmOfFasta3.py $1.aln.fasta

# Run hmm search *takes a while, may consider running on screen*
# this pipeline is currently configured to search the PapaGO metatranscriptomes
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.PapaGO_PlusFe.hits -u $1.aln.hmm /share/data/seq/meta/transcriptomic/Papa-GO/2008_12_02/R_2008_12_02_16_06_26_rig9_Lindsay_66_PAPA_GO2_FEx66_PAPA_GO2_FE/D_2008_12_02_21_07_57_rig9_fullProcessing/PapaGO_Transcriptome_plusFe-Ccatd.trimmed-noPolyA-noRRNA-Ddupd.6tr.fasta
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.PapaGO_Control.hits -u $1.aln.hmm /share/data/seq/meta/transcriptomic/Papa-GO/2008_12_11/R_2008_12_11_12_02_01_rig9_Lindsay_65_PapaGO1Contx65_PapaGO1Cont/D_2008_12_11_17_03_33_rig9_fullProcessing/PapaGO_Transcriptome_control-Ccatd.trimmed-noPolyA-noRRNA-Ddupd.6tr.fasta


# Run pplacer on the above *hits.hma.fasta files
pplacer -p --keep-at-most 1 -c $1.refpkg $1.vs.PapaGO_PlusFe.hits.hma.fasta
pplacer -p --keep-at-most 1 -c $1.refpkg $1.vs.PapaGO_Control.hits.hma.fasta

# If everything worked correctly you should now have $1.vs.P1-AB.hits.hma.jplace and
# $1.vs.P8-AB.hits.hma.jplace in the folder you launched from, ready to build trees, etc.