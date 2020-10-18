# coding=utf-8
""" check_as.py
"""
import sys,re,codecs
#import transcoder
#transcoder.transcoder_set_dir("");
import unicodedata


def update_asdict(line,asdict):
 if line == '':
  return
 ascodes = re.findall(r'[a-zA-Z][0-9]+',line)
 for c in ascodes:
  if c not in asdict:
   asdict[c] = 0
  asdict[c] = asdict[c] + 1

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

class ASRoman(object):
 def __init__(self,line):
  line= line.rstrip('\r\n') 
  self.status = False
  m = re.search(r'^<e> +<s>INIT</s> +<in>(.*?)</in> +<out>(.*?)</out> +</e>',line)
  if not m:
   return
  self.status = True
  self.line = m.group(0)
  self.asval = m.group(1)
  self.unival = m.group(2)
  self.count = 0  # number of times used

def init_iast(filein):
 with codecs.open(filein,"r","utf-8") as f:
  d = {}
  for iline,x in enumerate(f):
   r = ASRoman(x)
   if r.status:
    if r.asval in d:
     print('init_iast unexpected duplicate at line %s: %s'%(iline,r.asval))
    d[r.asval] = r
 return d

def write_asroman(fileout,iastd):
 keys = sorted(iastd.keys())
 outlines = []
 outlines.append("<fsm start='INIT' inputDecoding='UTF-8' outputEncoding='UTF-8'>")
 for key in keys:
  rec = iastd[key]
  if rec.count != 0:
   outlines.append(rec.line)
 outlines.append('</fsm>')
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print(len(outlines),"lines written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1]  # xxxwithmeta1.txt
 tranfile = sys.argv[2] # transcoder file for as to iast
 fileout = sys.argv[3] # xxxwithmeta2.txt
 fileout1 = sys.argv[4] # revised transcoder file
 iastd = init_iast(tranfile)
 with codecs.open(filein,"r","utf-8") as f:
  inlines = [x.rstrip('\r\n') for x in f]
  print(len(inlines),"lines read from",filein)
 d = check_as(inlines)
 write_as(d,iastd,fileout)
 write_asroman(fileout1,iastd)
