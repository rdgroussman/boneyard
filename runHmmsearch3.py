#!/usr/bin/python
# 
# $Rev: 1615 $
# $Date: 2013-06-10 10:46:22 -0700 (Mon, 10 Jun 2013) $
# 
# written by Erick Matsen
# this program runs hmmsearch, then parse the output to get the alignment of the HMM-selected
# sequences back in fasta format.
# the raw output from hmmsearch is put in a <prefix>.ohs file for Output of HmmSearch.
# the output is then parsed to get it back to fasta format
# the ohs file works as follows:

hmmsearchPath = "hmmsearch"
ohs_to_fasta_path = "/share/code/bifx/hmmer/ohs_to_fasta"

import os, sys, re, optparse, commands


# *** functions ***
def die(str):
  print str
  sys.exit(2)

# will fail if mask is too long
def maskStr(str, mask):
  assert(mask != None)
  masked = ""
  for i in range(len(mask)):
    if mask[i] == 'x':
      masked += str[i]
  return masked

# *** main ***
usage = "usage: runHmmsearch.py hmmfile queries"
op = optparse.OptionParser(usage)
op.add_option("-E", "--eValueCutoff", dest="eValueCutoff", default=1e-5, help="set E-value cutoff", type="float")
op.add_option("-o", "--outPrefix", dest="outPrefix", default="", help="set the output prefix", type="string")
op.add_option("-u", "--heuristics", dest="heuristics", default="--max", const="", help="enable heuristics for speed up", action="store_const")

(options, args) = op.parse_args()

hmmName = args.pop(0)

for queryName in args:
  if not re.search(".fa(sta)?$", queryName):
    die("subsequent arguments need to be fasta files with .fasta or .fa suffixes")
  
  # make ohsFname
  if options.outPrefix == "":
    basename = re.sub(".fa(sta)?$", "", queryName)
    # N.B. With this change .ohs and hma.fasta files always created in cwd
    basename = os.path.split(basename)[1] # just filename
  else :
    basename = options.outPrefix
  ohsFname = basename+".ohs"
  
  # run hmmsearch and pipe out to ohs file
  hmmsearch_str = hmmsearchPath+" %s -E %g %s %s > %s" \
                  % (options.heuristics, options.eValueCutoff, hmmName, queryName, ohsFname)
  print "running: %s" % hmmsearch_str
  if os.system(hmmsearch_str) != 0:
    die("hmmsearch had a problem")
  
  # run ohs_to_fasta
  if os.system(ohs_to_fasta_path+" %s" % (ohsFname)) != 0:
    die("ohs_to_fasta had a problem")

