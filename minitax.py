#!/usr/bin/env python

# Calling this script with an NCBI taxon ID as an argument will return the full lineage given by the taxon ID
# Example: >minitax.py 9601
# Returns: cellular organisms; Eukaryota; Opisthokonta; Metazoa; Eumetazoa; Bilateria; Deuterostomia; Chordata; Craniata; Vertebrata; 
# Gnathostomata; Teleostomi; Euteleostomi; Sarcopterygii; Dipnotetrapodomorpha; Tetrapoda; Amniota; Mammalia; Theria; Eutheria; Euarchontoglires; 
# Primates; Haplorrhini; Simiiformes; Catarrhini; Hominoidea; Hominidae; Ponginae; Pongo

import sys
from Bio import Entrez
Entrez.email = "rgroussman@gmail.com"

TaxonID = sys.argv[1]

# retrieve taxonomy information for each TaxonID from NCBI
handle = Entrez.efetch(db="Taxonomy", id=TaxonID, retmode="xml")
records = Entrez.read(handle)
Lineage = records[0]["Lineage"]

print Lineage