# coding=utf-8
""" as_iast.py
"""
import sys,re,codecs
import transcoder
transcoder.transcoder_set_dir("");
#import unicodedata


def check_as(inlines):
# set up regex callback 'repl' with access to dictionary asdict
 asdict = {}
 # read the lines of the file
 n = 0
 for iline,line in enumerate(inlines):
  if line.startswith('[Page'):
   continue
  line = line.rstrip()
  n = n + 1
  update_asdict(line,asdict)
 return asdict

def write_as(d,iastd,fileout):
 keys = d.keys()
 print(len(keys),"extended ascii codes found")
 #print("n=",n)
 keys = sorted(keys)
 print(len(keys))
 outlines = []
 for key in keys:
  asobj = d[key]
  #out = "%s  (%s) %5d := %s" %(key,ordstr,asobj,namestr)
  if key in iastd:
   r = iastd[key]
   unival = r.unival
   r.count = asobj
  else:
   unival = '?'
  out = "%s %s %d" %(key,unival,asobj)
  outlines.append(out)
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print(len(outlines),"lines written to",fileout)

def transcode_line(line,tranin,tranout):
 if line.startswith('[Page'):
  return line
 else:
  return transcoder.transcoder_processString(line,tranin,tranout)

def transcode_lines(inlines,tranin,tranout):
 outlines = []
 for iline,line in enumerate(inlines):
  outlines.append(transcode_line(line,tranin,tranout))
 return outlines
def test(tranin,tranout):
 line = 'Sam2hit'
 out = transcode_line(line,tranin,tranout)
 print(line,'->',out)
 exit()
if __name__=="__main__":
 filein = sys.argv[1]  # lsr0_refs
 tranin,tranout = sys.argv[2].split('_')
 print(tranin,tranout)
 #test(tranin,tranout)
 fileout = sys.argv[3] # lsr1_refs
 with codecs.open(filein,"r","utf-8") as f:
  inlines = [x.rstrip('\r\n') for x in f]
  print(len(inlines),"lines read from",filein)
 outlines = transcode_lines(inlines,tranin,tranout)
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print(len(outlines),"lines written to",fileout)
