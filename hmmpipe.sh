#!/bin/bash

### hmmpipe.sh ###
#  This script will run hmmpipe on a collection of ESTs and return concatenated results with friendly fasta headers
#
# You'll want to begin with a reference alignment in the format JobName.refseqs.aln.fasta
# Call the script as follows: 'hmmpipe.sh JobName' (or '/share/projects/diatom_est/annotation/scripts/hmmpipe.sh JobName' if not in your path)
# This pipeline outputs a fair amount of files so at this point it is recommended to run each job in its own directory

# Create hmm profile of reference alignment
/share/projects/diatom_est/annotation/scripts/hmmOfFasta3.py $1.refseqs.aln.fasta


##  hmmsearch vs MMETSP-139 (139 CAMERA-hosted transcriptomes)
# Run hmm search vs MMETSP-139
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.MMETSP-139 -u $1.refseqs.aln.hmm /share/projects/diatom_est/source_data/CAMERA_peptides/CAM_P_0001000.pep.fa
# call campep_fix.py to fix resultant FASTA headers and output friendly names format (>Genus_species_cp1234567890)
/share/projects/diatom_est/annotation/scripts/campep_fix.py $1.vs.MMETSP-139
echo "Final output of hmmsearch vs MMETSP-139: $1.vs.MMETSP-139.hma.fasta.fn"


##  hmmsearch vs MMETSP_all (all 31 in-house transcriptomes)
# Run hmm search vs MMETSP_all
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.MMETSP_all -u $1.refseqs.aln.hmm /share/projects/diatom_est/source_data/MMETSP_all/MMETSP_allpeptides.fa
# call fnames.py to fix FASTA headers (>Genus_species_12345)
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.MMETSP_all.hma.fasta MMETSP
echo "Final output of hmmsearch vs MMETSP_all: $1.vs.MMETSP_all.hma.fasta.fn"


## Fragilariopsis cylindrus
# /share/data/seq/organisms/Fragilariopsis_cylindrus/genome/Fracy1_GeneModels_FilteredModels2_aa.shortID.fasta
# Run hmm search vs F. cylindrus
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.Fracy -u $1.refseqs.aln.hmm /share/data/seq/organisms/Fragilariopsis_cylindrus/genome/Fracy1_GeneModels_FilteredModels2_aa.shortID.fasta
# call fnames.py to fix FASTA headers (>Genus_species_12345)
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Fracy.hma.fasta Fracy
echo "Final output of hmmsearch vs F.cylindrus: $1.vs.Fracy.hma.fasta.fn"


# Thalassiosira pseudonana
# /share/data/seq/organisms/Thalassiosira_pseudonana/genome/Thaps3_geneModels_FilteredModels2_aa.fasta
# Run hmm search vs Thaps
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.Thaps -u $1.refseqs.aln.hmm /share/data/seq/organisms/Thalassiosira_pseudonana/genome/Thaps3_geneModels_FilteredModels2_aa.fasta
# call fnames.py to fix FASTA headers (>Genus_species_12345)
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Thaps.hma.fasta Thaps
echo "Final output of hmmsearch vs T. pseudonana: $1.vs.Thaps.hma.fasta.fn"


# Phaeodactylum tricornutum
# /share/data/seq/organisms/Phaeodactylum_tricornutum/genome/Phatr2.FilteredModels2_aa.fasta
# Run hmm search vs Phaeo
/share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.Phaeo -u $1.refseqs.aln.hmm /share/data/seq/organisms/Phaeodactylum_tricornutum/genome/Phatr2.FilteredModels2_aa.fasta
# call fnames.py to fix FASTA headers (>Genus_species_12345)
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Phaeo.hma.fasta Phaeo
echo "Final output of hmmsearch vs P.tricornutum: $1.vs.Phaeo.hma.fasta.fn"

# ## hmmsearch requires a target fasta file with .fa or .fasta suffix ! need to find or rename
# # Pseudo-nitzschia multiseries
# # /share/data/seq/organisms/Pseudo-nitzschia_multiseries/genome/Psemu1_GeneCatalog_proteins_20111011.aa.fasta-idcleaned
# # Run hmm search vs Psemu
# /share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.Psemu -u $1.refseqs.aln.hmm /share/data/seq/organisms/Pseudo-nitzschia_multiseries/genome/Psemu1_GeneCatalog_proteins_20111011.aa.fasta-idcleaned
# # call fnames.py to fix FASTA headers (>Genus_species_12345)
# /share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Psemu.hma.fasta Psemu
# echo "Final output of hmmsearch vs P. multiseries: $1.vs.Psemu.hma.fasta.fn"


# ## hmmsearch requires a target fasta file with .fa or .fasta suffix ! need to find or rename
# # Ectocarpus siliculosis
# # /share/data/seq/organisms/Ectocarpus_siliculosus/genome/Ectsi_prot_LATEST.tfa-idcleaned
# # Run hmm search vs Esili
# /share/code/bifx/hmmer/runHmmsearch3.py -o $1.vs.Esili -u $1.refseqs.aln.hmm /share/data/seq/organisms/Ectocarpus_siliculosus/genome/Ectsi_prot_LATEST.tfa-idcleaned
# # call fnames.py to fix FASTA headers (>Genus_species_12345)
# /share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Esili.hma.fasta Esili
# echo "Final output of hmmsearch vs E. siliculosis: $1.vs.Esili.hma.fasta.fn"





# Emiliana_huxleyi
# /share/data/seq/organisms/Emiliana_huxleyi/jgi_annotation/v1/Emihu1_best_proteins.fasta-idcleaned





echo "Concatenating reference alignment and target hits to $1.allhits.aln.fasta..."
cat $1.refseqs.aln.fasta $1.vs.MMETSP-139.hma.fasta.fn $1.vs.MMETSP_all.hma.fasta.fn > $1.allhits.aln.fasta
cat $1.vs.Fracy.hma.fasta.fn $1.vs.Thaps.hma.fasta.fn $1.vs.Phaeo.hma.fasta.fn >> $1.allhits.aln.fasta



# NOTE! Question marks in hmmsearch alignment data (?) must be replaced by dashes (-) before running through pplacer




# # BLASTP vs Pseudo-nitzschia granii
# echo "BLASTing $1.refseqs.fasta versus P.granii..."
# blastp -db /share/projects/GeoMics/Metatranscriptome/additional_CAMERA_ESTs/P.granii_blastdb/P.granii_UWOSP36 -query $1.refseqs.fasta -out $1.refseqs.vs.Pgranii.out -outfmt 6 -evalue 1e-03
# echo "Completed BLASTP run on $1"
# /home/rgrous83/scripts/blast.hitlist.py $1.refseqs.vs.Pgranii.out
# echo "Created BLASTdb hitlist..."
# sort $1.refseqs.vs.Pgranii.out.hitlist | uniq > $1.uniq.Pgranii.hitlist
# blastdbcmd -db /share/projects/GeoMics/Metatranscriptome/additional_CAMERA_ESTs/P.granii_blastdb/P.granii_UWOSP36 -dbtype prot -entry_batch $1.uniq.Pgranii.hitlist -outfmt %f -out $1.Pgranii.blasthits.fasta
# echo "Retrieved FASTA from database..."
# /home/rgrous83/scripts/fnames.py $1.Pgranii.blasthits.fasta Pgr
# echo "Applied friendly names to FASTA headers..."
# echo "Final output: $1.Pgranii.blasthits.fasta.fn"


