#-*- coding:utf-8 -*-
"""deva_markup.py
   04-10-2020

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

def preadjust1(lines):
 a = []
 for i,x in enumerate(lines):
  if i == 0:
   y = lines[2]  # put page break line first
  elif i == 1:
   y = lines[0] 
   y = y.replace('I.','{#I.#}')
  elif i == 2:
   y = lines[1]
  else:
   y = x
  a.append(y)
 return a

def preadjust2(lines):
 a = []
 n = 0
 for x in lines:
  y = re.sub(r'<head>{#(.+)#}</head>',r'<section>\1</section>',x)
  if y != x:
   n = n + 1
  a.append(y)
 print('preadjust2: %d lines changed'%n)
 return a

def deva_markup_one(x): 
 if x.startswith('[Page'):
  return x
 if re.search(r'<section>',x):
  return x
 m = re.search(r'^([0-9][0-9][0-9][0-9][0-9]) (.*)$',x)
 linenum,data = m.group(1),m.group(2)
 parts = re.split(r'(<.*?>)',data)
 newparts = []
 for part in parts:
  if part == '':
   continue
  if part.startswith('<'):
   newpart = part
  else:
   newpart = '<s>%s</s>' % part
  newparts.append(newpart)
 newdata = ''.join(newparts)
 newline = '%s %s' %(linenum,newdata)
 temp = re.findall('<s>',newline)
 if len(temp) > 1:
  print('anomaly',newline)
 return newline

def deva_markup(lines):
 a = []
 n = 0
 for x in lines:
  y = deva_markup_one(x)
  if y != x:
   n = n + 1
  a.append(y)
 print('deva_markup: %d lines changed'%n)
 return a

if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 with codecs.open(filein,"r","utf8") as f:
  lines = [x.rstrip('\r\n') for x in f]
  print(len(lines),"lines read from",filein)

 lines1 = preadjust1(lines)
 lines2 = preadjust2(lines1)
 lines3 = deva_markup(lines2)
 outlines = lines3
 with codecs.open(fileout,"w","utf8") as f:  
  for out in outlines:
   f.write(out+'\n')
 print(len(outlines),"records written to",fileout)
