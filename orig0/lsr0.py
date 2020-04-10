#-*- coding:utf-8 -*-
"""lsr0.py
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

def adjust(lines):
 outarr = []  # result
 npage = 0
 for line in lines:
  assert line.startswith(('NE ','EQ '))
  x = line[3:]  # remove ('NE ','EQ ')
  m = re.search(r'^([0-9][0-9][0-9][0-9][0-9])[+]B<>(.*)$',x)
  lid = m.group(1)  # 5-digit
  data = m.group(2)
  
  m = re.search(r' \[Page[0-9][0-9][0-9](-1?[ab])?[+] ([0-9]+)\]$',data)
  #m = re.search(r' \[Page.*?\]$',data)
  if m:
   page = m.group(0)
   data = data.replace(page,'')
   page = page[1:]  # remove initial ' '
   outarr.append('%s %s'%(lid,data))
   outarr.append(page)
   npage = npage + 1
  else:
   outarr.append('%s %s'%(lid,data))
 print("%s lines adjusted, with %s page breaks"%(len(lines),npage))
 return outarr
if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 filepage = sys.argv[3]
 with codecs.open(filein,"r","utf8") as f:
  lines = [x.rstrip('\r\n') for x in f if x.startswith(('NE ','EQ '))]

 newlines = adjust(lines)

 with codecs.open(fileout,"w","utf8") as f:  
  for out in newlines:
   f.write(out+'\n')
   #if out.startswith('[Page'):
   # print(out)
 print(len(newlines),"records written to",fileout)
 with codecs.open(filepage,"w","utf8") as f:
  n = 0
  for out in newlines:
   if out.startswith('[Page'):
    f.write(out+'\n')
    n = n + 1
 print(n,"records written to",filepage)
