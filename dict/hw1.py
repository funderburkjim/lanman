# coding=utf-8
"""hw1.py  ejf 2014-03-24. Modify to work with utf-8 for ben.
 Read  hw0.txt, whose lines were created with:
 out = "%s:%s:%s,%s" %(page,hw,l1,l2)

 'Normalize' all headword spellings, but still leave in HK.
 Then output the same format, using the normalized headword
 See hw_normalize, for the normalizations applied.
 
 Check that the remaining characters are a-z,A-Z or |
"""
import re
import sys,codecs
sys.path.append('../orig/refs/')
import transcoder
transcoder.transcoder_set_dir("")
# hwroman_slp1.xml   

class HW0(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  (self.pagecol,self.hw0,self.line12) = line.split(':')
  self.root = False
  self.hom = None
  self.parse()
 def parse(self):
  key2 = self.hw0
  m = re.search(r'^√',key2)
  if m:
   key2 = key2[1:]  # drop root symbol
   self.root = True
  m = re.search(r'^([1-9])',key2)
  if m:
   self.hom = m.group(1)
   key2 = key2[1:] # drop homonym number
  m = re.search(r',$',key2)
  if m:
   key2 = key2[0:-1]  # drop trailing comma
  m = re.search(r'[.]$',key2)
  if m:
   key2 = key2[0:-1]  # drop trailing period (1 case)
  
  self.key2 = transcoder.transcoder_processString(key2,'hwroman','slp1')
  self.key1 = re.sub(r'[/\^-]','',self.key2)

def check_recs(recs):
 d = {}
 for rec in recs:
  cbad = re.findall('[^a-zA-Z|]',rec.key1)
  for c in cbad:
   if c not in d:
    d[c] = 0
   d[c] = d[c] + 1
  if cbad != []:
   print(cbad,rec.line)
 for c in d:
  print(c,d[c])

if __name__ == "__main__":
 filein=sys.argv[1] 
 fileout =sys.argv[2] 
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HW0(line) for line in f]
 print(len(recs),"read from",filein)
 check_recs(recs)
 
 with codecs.open(fileout,'w','utf-8') as f:
  for rec in recs:
   h = rec.hom
   if h == None:
    h = ''
   out = '%s:%s:%s:%s:%s'%(rec.pagecol,rec.key1,rec.line12,h,rec.key2)
   f.write(out + '\n')
 print(len(recs),"written to",fileout)
