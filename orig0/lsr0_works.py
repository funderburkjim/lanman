#-*- coding:utf-8 -*-
"""lsr0_works.py
   04-09-2020

"""
from __future__ import print_function
import codecs,sys,re

def find_first_difference(rec1,rec2):
 n1 = len(rec1)
 n2 = len(rec2)
 n = max(n1,n2)
 for i in range(0,n):
  if (i < n1) and (i < n2):
   if (rec1[i] != rec2[i]):
    return i
   else:
    # continue in loop
    continue
  else:
   return i

def parse_input(filein1):
 with codecs.open(filein1,"r","utf8") as f:
  recs1=[]
  recs2=[]
  for idx,x in enumerate(f):
   #recs1 = [x.rstrip('\r\n') for x in f]
   x = x.rstrip('\r\n')
   if idx == 0:
    header = x
    continue
   m = re.search(r'^([0-9]{5}[+])([AB])(<>.*)$',x)
   if not m:
    print("unexpected format at line,",idx+1)
    print(x.encode('utf-8'))
    exit(1)
   lineid = m.group(1)
   group = m.group(2) #A,B
   text = m.group(3)
   if group == 'A':
    recs1.append((lineid,group,text))
   else:
    recs2.append((lineid,group,text))
 print("idx=",idx)
 print(len(recs1),len(recs2))
 return (header,recs1,recs2)

def splitlines(lines):
 idx_text_last = 2401  # line number of last text line.
 a = lines[0:2401] # text lines
 b = lines[2401:] # reference lines
 return a,b

if __name__ == "__main__":
 filein = sys.argv[1]
 fileout1 = sys.argv[2]
 fileout2 = sys.argv[3]
 with codecs.open(filein,"r","utf8") as f:
  lines = [x.rstrip('\r\n') for x in f]

 textlines,reflines = splitlines(lines)

 with codecs.open(fileout1,"w","utf8") as f:  
  for out in textlines:
   f.write(out+'\n')
 print(len(textlines),"records written to",fileout1)

 with codecs.open(fileout2,"w","utf8") as f:  
  for out in reflines:
   f.write(out+'\n')
 print(len(reflines),"records written to",fileout2)
