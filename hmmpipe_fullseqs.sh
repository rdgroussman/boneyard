#!/bin/bash

### hmmpipe_fullseqs.sh ###
#  This script will run hmmpipe on a collection of ESTs and return concatenated results with friendly fasta headers
#  Utilizes 'runHmmsearch3_hmmgrab2.py', a variant of runHmmsearch3.py by Erick Matsen
#
# You'll want to begin with a reference alignment in the format JobName.refseqs.aln.fasta
# Call the script as follows: 'hmmpipe.sh JobName' (or '/share/projects/diatom_est/annotation/scripts/hmmpipe_mafft.sh JobName' if not in your path)
# This pipeline outputs a fair amount of files so at this point it is recommended to run each job in its own directory

# Create hmm profile of reference alignment
/share/projects/diatom_est/annotation/scripts/hmmOfFasta3.py $1.refseqs.aln.fasta


##  hmmsearch vs MMETSP-139 (139 CAMERA-hosted transcriptomes)
# Run hmm search vs MMETSP-139
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.MMETSP-139 -u $1.refseqs.aln.hmm /share/projects/diatom_est/source_data/CAMERA_peptides/CAM_P_0001000.pep.fa
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.MMETSP-139 /share/projects/diatom_est/source_data/CAMERA_peptides/CAM_P_0001000.pep.fa
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.MMETSP-139.fasta CAMERA
echo "Final output of hmmsearch vs MMETSP-139: $1.vs.MMETSP-139.fasta.fn"


##  hmmsearch vs MMETSP_all (all 31 in-house transcriptomes)
# Run hmm search vs MMETSP_all
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.MMETSP_all -u $1.refseqs.aln.hmm /share/projects/diatom_est/source_data/MMETSP_all/MMETSP_allpeptides.fa
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.MMETSP_all /share/projects/diatom_est/source_data/MMETSP_all/MMETSP_allpeptides.fa
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.MMETSP_all.fasta MMETSP
echo "Final output of hmmsearch vs MMETSP_all: $1.vs.MMETSP_all.fasta.fn"

# Concatenate refseqs and hits from MMETSP sets
cat $1.refseqs.aln.fasta $1.vs.MMETSP-139.fasta.fn $1.vs.MMETSP_all.fasta.fn > $1.allhits.raw.fasta


## Fragilariopsis cylindrus
# /share/data/seq/organisms/Fragilariopsis_cylindrus/genome/Fracy1_GeneModels_FilteredModels2_aa.shortID.fasta
# Run hmm search vs F. cylindrus
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.Fracy -u $1.refseqs.aln.hmm /share/data/seq/organisms/Fragilariopsis_cylindrus/genome/Fracy1_GeneModels_FilteredModels2_aa.shortID.fasta
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.Fracy /share/data/seq/organisms/Fragilariopsis_cylindrus/genome/Fracy1_GeneModels_FilteredModels2_aa.shortID.fasta
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Fracy.fasta Fracy
echo "Final output of hmmsearch vs F.cylindrus: $1.vs.Fracy.fasta.fn"
cat $1.vs.Fracy.fasta.fn >> $1.allhits.raw.fasta


# Thalassiosira pseudonana
# /share/data/seq/organisms/Thalassiosira_pseudonana/genome/Thaps3_geneModels_FilteredModels2_aa.fasta
# Run hmm search vs Thaps
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.Thaps -u $1.refseqs.aln.hmm /share/data/seq/organisms/Thalassiosira_pseudonana/genome/Thaps3_geneModels_FilteredModels2_aa.fasta
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.Thaps /share/data/seq/organisms/Thalassiosira_pseudonana/genome/Thaps3_geneModels_FilteredModels2_aa.fasta
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Thaps.fasta Thaps
echo "Final output of hmmsearch vs T.pseudonana: $1.vs.Thaps.fasta.fn"
cat $1.vs.Thaps.fasta.fn >> $1.allhits.raw.fasta


# Phaeodactylum tricornutum
# /share/data/seq/organisms/Phaeodactylum_tricornutum/genome/Phatr2.FilteredModels2_aa.fasta
# Run hmm search vs Phaeo
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.Phaeo -u $1.refseqs.aln.hmm /share/data/seq/organisms/Phaeodactylum_tricornutum/genome/Phatr2.FilteredModels2_aa.fasta
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.Phaeo /share/data/seq/organisms/Phaeodactylum_tricornutum/genome/Phatr2.FilteredModels2_aa.fasta
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Phaeo.fasta Phaeo
echo "Final output of hmmsearch vs P.tricornutum: $1.vs.Phaeo.fasta.fn"
cat $1.vs.Phaeo.fasta.fn >> $1.allhits.raw.fasta


# Pseudo-nitzschia multiseries
# /share/data/seq/organisms/Pseudo-nitzschia_multiseries/genome/Psemu1_GeneCatalog_proteins_20111011.aa.fasta-idcleaned
# Run hmm search vs Psemu
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.Psemu -u $1.refseqs.aln.hmm /share/data/seq/organisms/Pseudo-nitzschia_multiseries/genome/Psemu1_GeneCatalog_proteins_20111011.aa.fasta-idcleaned
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.Psemu /share/data/seq/organisms/Pseudo-nitzschia_multiseries/genome/Psemu1_GeneCatalog_proteins_20111011.aa.fasta-idcleaned
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Psemu.fasta Psemu
echo "Final output of hmmsearch vs P.multiseries: $1.vs.Psemu.fasta.fn"
cat $1.vs.Psemu.fasta.fn >> $1.allhits.raw.fasta


# Ectocarpus siliculosis
# /share/data/seq/organisms/Ectocarpus_siliculosus/genome/Ectsi_prot_LATEST.tfa-idcleaned
# Run hmm search vs Esili
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.Esili -u $1.refseqs.aln.hmm /share/data/seq/organisms/Ectocarpus_siliculosus/genome/Ectsi_prot_LATEST.tfa-idcleaned
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.Esili /share/data/seq/organisms/Ectocarpus_siliculosus/genome/Ectsi_prot_LATEST.tfa-idcleaned
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Esili.fasta Esili
echo "Final output of hmmsearch vs E.siliculosis: $1.vs.Esili.fasta.fn"
cat $1.vs.Esili.fasta.fn >> $1.allhits.raw.fasta


## Emiliana_huxleyi
# /share/data/seq/organisms/Emiliana_huxleyi/jgi_annotation/v1/Emihu1_best_proteins.fasta-idcleaned
# Run hmm search vs Ehux
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.Ehux -u $1.refseqs.aln.hmm /share/data/seq/organisms/Emiliana_huxleyi/jgi_annotation/v1/Emihu1_best_proteins.fasta-idcleaned
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.Ehux /share/data/seq/organisms/Emiliana_huxleyi/jgi_annotation/v1/Emihu1_best_proteins.fasta-idcleaned
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Ehux.fasta Ehux
echo "Final output of hmmsearch vs E.huxleyi: $1.vs.Ehux.fasta.fn"
cat $1.vs.Ehux.fasta.fn >> $1.allhits.raw.fasta


## Psudo-nitzchia granii
# /share/projects/GeoMics/Metatranscriptome/additional_CAMERA_ESTs/P.granii_UWOSP36_454.cabog.all.6tr.fasta
# Run hmm search vs Psegr
/share/projects/diatom_est/annotation/scripts/runHmmsearch3_hmmgrab2.py -o $1.vs.Psegr -u $1.refseqs.aln.hmm /share/projects/GeoMics/Metatranscriptome/additional_CAMERA_ESTs/P.granii_UWOSP36_454.cabog.all.6tr.fasta
# call hmmgrab2.py to collect full-length sequences
/share/projects/diatom_est/annotation/scripts/hmmgrab2.py $1.vs.Psegr /share/projects/GeoMics/Metatranscriptome/additional_CAMERA_ESTs/P.granii_UWOSP36_454.cabog.all.6tr.fasta
# call fnames.py to rename headers
/share/projects/diatom_est/annotation/scripts/fnames.py $1.vs.Psegr.fasta Pgr
echo "Final output of hmmsearch vs E.huxleyi: $1.vs.Psegr.fasta.fn"
cat $1.vs.Psegr.fasta.fn >> $1.allhits.raw.fasta

echo "Concatenated reference alignment and target hits to $1.allhits.raw.fasta..."


# Micromonas (2 strains) needs to be translated
# Ostreococcus needs to be translated


# align with mafft...

# NOTE! Question marks in hmmsearch alignment data (?) must be replaced by dashes (-) before running through pplacer