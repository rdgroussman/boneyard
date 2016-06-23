#!/bin/bash

# begin with reference sequences
# BLASTP vs databases

# $1 = name of job

# BLASTP vs MMETSP-100
# this version of blastpipe retrieves only diatoms from MMETSP-100
echo "BLASTing $1.refseqs.fasta versus MMETSP-100..."
blastp -db /home/rgrous83/CAMERA/MMETP_CAMPEP_Jun23/MMETPBLAST -query $1.refseqs.fasta -out $1.refseqs.vs.MMETPBLAST.out -outfmt 6 -evalue 1e-03
echo "Completed BLASTP run on " $1
/home/rgrous83/scripts/blast.hitlist.py $1.refseqs.vs.MMETPBLAST.out
echo "Created BLASTdb hitlist..."
sort $1.refseqs.vs.MMETPBLAST.out.hitlist | uniq > $1.uniq.MMETSP-100.hitlist



blastdbcmd -db /home/rgrous83/CAMERA/MMETP_CAMPEP_Jun23/MMETPBLAST -dbtype prot -entry_batch $1.uniq.MMETSP-100.hitlist -outfmt %f -out $1.MMETSP-100.blasthits.fasta
echo "Retrieved FASTA from database..."

# search FASTA for diatoms
grep -E '^>.+MMETSP0321-|MMETSP0322-|MMETSP0320-|MMETSP0319-|MMETSP0327-|MMETSP0329-|MMETSP0397-|MMETSP0418-|MMETSP1176-|MMETSP1336-|MMETSP1352-' $1.MMETSP-100.blasthits.fasta > $1.diatom.uniq.MMETSP-100.headers

# create hitlist from these results
/home/rgrous83/scripts/diatom_hitlist.py $1.diatom.uniq.MMETSP-100.headers

# retrieve list...
blastdbcmd -db /home/rgrous83/CAMERA/MMETP_CAMPEP_Jun23/MMETPBLAST -dbtype prot -entry_batch $1.diatom.uniq.MMETSP-100.headers.hitlist -outfmt %f -out $1.diatom.MMETSP-100.blasthits.fasta

/home/rgrous83/scripts/fnames.py $1.diatom.MMETSP-100.blasthits.fasta CAMERA
echo "Applied friendly names to FASTA headers..."
echo "Final output: $1.diatom.MMETSP-100.blasthits.fasta.fn"
mkdir $1
mv $1.refseqs.vs.MMETPBLAST.out $1
mv $1.refseqs.vs.MMETPBLAST.out.hitlist $1
mv $1.uniq.MMETSP-100.hitlist $1
mv $1.diatom.uniq.MMETSP-100.hitlist $1
mv $1.diatom.MMETSP-100.blasthits.fasta $1
mv $1.MMETSP-100.blasthits.fasta $1
mv $1.diatom.MMETSP-100.blasthits.fasta.fn $1
echo "Moved files from this run to $1/"


# BLASTP vs MMETSP-24
echo "BLASTing $1.refseqs.fasta versus MMETSP-24..."
blastp -db /home/rgrous83/MMETSP/blastdb/MMETP-24_blastdb -query $1.refseqs.fasta -out $1.refseqs.vs.MMETSP-24.out -outfmt 6 -evalue 1e-03
echo "Completed BLASTP run on $1"
/home/rgrous83/scripts/blast.hitlist.py $1.refseqs.vs.MMETSP-24.out
echo "Created BLASTdb hitlist..."
sort $1.refseqs.vs.MMETSP-24.out.hitlist | uniq > $1.uniq.MMETSP-24.hitlist
blastdbcmd -db /home/rgrous83/MMETSP/blastdb/MMETP-24_blastdb -dbtype prot -entry_batch $1.uniq.MMETSP-24.hitlist -outfmt %f -out $1.MMETSP-24.blasthits.fasta
echo "Retrieved FASTA from database..."
/home/rgrous83/scripts/fnames.py $1.MMETSP-24.blasthits.fasta MMETSP
echo "Applied friendly names to FASTA headers..."
echo "Final output: $1.MMETSP-24.blasthits.fasta.fn"
mv $1.refseqs.vs.MMETSP-24.out $1
mv $1.refseqs.vs.MMETSP-24.out.hitlist $1
mv $1.uniq.MMETSP-24.hitlist $1
mv $1.MMETSP-24.blasthits.fasta $1
mv $1.MMETSP-24.blasthits.fasta.fn $1
echo "Moved files from this run to $1/"




# BLASTP vs Pseudo-nitzschia granii

# fnames.py needs Pgranii compatability
echo "BLASTing $1.refseqs.fasta versus P.granii..."
blastp -db /share/projects/GeoMics/Metatranscriptome/additional_CAMERA_ESTs/P.granii_blastdb/P.granii_UWOSP36 -query $1.refseqs.fasta -out $1.refseqs.vs.Pgranii.out -outfmt 6 -evalue 1e-03
echo "Completed BLASTP run on $1"
/home/rgrous83/scripts/blast.hitlist.py $1.refseqs.vs.Pgranii.out
echo "Created BLASTdb hitlist..."
sort $1.refseqs.vs.Pgranii.out.hitlist | uniq > $1.uniq.Pgranii.hitlist
blastdbcmd -db /share/projects/GeoMics/Metatranscriptome/additional_CAMERA_ESTs/P.granii_blastdb/P.granii_UWOSP36 -dbtype prot -entry_batch $1.uniq.Pgranii.hitlist -outfmt %f -out $1.Pgranii.blasthits.fasta
echo "Retrieved FASTA from database..."
/home/rgrous83/scripts/fnames.py $1.Pgranii.blasthits.fasta Pgr
echo "Applied friendly names to FASTA headers..."
echo "Final output: $1.Pgranii.blasthits.fasta.fn"
mv $1.refseqs.vs.Pgranii.out $1
mv $1.refseqs.vs.Pgranii.out.hitlist $1
mv $1.uniq.Pgranii.hitlist $1
mv $1.Pgranii.blasthits.fasta $1
mv $1.Pgranii.blasthits.fasta.fn $1
echo "Moved files from this run to $1/"



# concatenate into a single FASTA file ...
echo "Concatenating friendly FASTA files..."
cat $1.refseqs.fasta $1/$1.diatom.MMETSP-100.blasthits.fasta.fn $1/$1.MMETSP-24.blasthits.fasta.fn $1/$1.Pgranii.blasthits.fasta.fn > $1.allhits.fasta
echo "Created $1.allhits.fasta"


# Filter out 100% redundant sequences...

# Align with Mafft. . .

# FastTree...


