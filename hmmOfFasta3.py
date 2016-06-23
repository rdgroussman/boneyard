#!/share/apps/python2.5/bin/python

# build an HMM from a fasta file
# it would be best to do this directly through biopython, but couldn't figure out how to add RF line there

import os, sys, re, getopt, commands
from Bio import SeqIO

# hmmbuild_str = "/home/rkodner/bin/hmmbuild3"
hmmbuild_str = "/share/apps/bin/hmmbuild"
def usage():
  print '''usage: hmmOfFasta fastaFiles
'''
  sys.exit(0)

def die(str):
  print str
  sys.exit(2)

#defaults


#functions

args = sys.argv[1:]

if len(args) == 0:
  usage()
  sys.exit(0)

# translate the gaps for stockholm
def trans_gaps(seq):
  return re.sub("\?","~",seq)

for fastaName in args:
  count=1

  fastaFile = open(fastaName, "r")
  (fastaPrefix, fastaSuffix) = os.path.splitext(os.path.basename(fastaName))

  if fastaSuffix != ".fasta" and fastaSuffix != ".fa":
    die("fasta files with fasta suffix, please")

  maxNameLen = 7
  seqLength = None

  fastaDict = {}

  for seqRecord in SeqIO.parse(fastaFile, "fasta"):
    fastaDict[seqRecord.name] = seqRecord.seq
    thisSeqLen = len(str(seqRecord.seq))
    if seqLength != None:
      if thisSeqLen != seqLength:
	die("not all seqs same length in "+fastaName)
    else :
      seqLength = thisSeqLen

  for name in fastaDict:
    nameLen = len(name)
    if nameLen > maxNameLen:
      maxNameLen = nameLen

  desiredWidth = maxNameLen+5

  stoName = fastaPrefix+".sto"
  hmmName = fastaPrefix+".hmm"

  print "writing "+stoName+"..."

  stoFile = open(stoName, "w")
  stoFile.write("# STOCKHOLM 1.0\n\n")

  for name in fastaDict:
    stoFile.write(name.ljust(desiredWidth)+trans_gaps(str(fastaDict[name]))+'\n')

  stoFile.write('#=GC RF'.ljust(desiredWidth)+''.ljust(seqLength,'x')+'\n')
  stoFile.write("//\n")
  stoFile.close()

  print "making "+hmmName+"..."
  print commands.getoutput(hmmbuild_str+" --hand %s %s" % (hmmName, stoName))
