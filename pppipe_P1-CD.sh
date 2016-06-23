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
# this pipeline is currently configured to hit the unfiltered replicates (C & D) from stations P1 of the GeoMICS cruise
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.P1-C.hits -u $1.aln.hmm /share/projects/GeoMics/Metatranscriptome/reads/processed/allreads/P1-C.qc.allreads.6tr.fasta
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.P1-D.hits -u $1.aln.hmm /share/projects/GeoMics/Metatranscriptome/reads/processed/allreads/P1-D.qc.allreads.6tr.fasta

# Concatenate the resultant replicates into one hma.fasta file:
cat $1.vs.P1-C.hits.hma.fasta $1.vs.P1-D.hits.hma.fasta > $1.vs.P1-CD.hits.hma.fasta

# Run pplacer on the above *hits.hma.fasta files
pplacer -p --keep-at-most 1 -c $1.refpkg $1.vs.P1-CD.hits.hma.fasta

# If everything worked correctly you should now have $1.vs.P1-CD.hits.hma.jplace
# in the folder you launched from, ready to build trees, etc.