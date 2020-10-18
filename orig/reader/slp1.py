#-*- coding:utf-8 -*-
"""deva_markup.py
   04-10-2020

"""
from __future__ import print_function
import codecs,sys,re
import transcoder
from transcoder import transcoder_processString
transcoder.transcoder_set_dir('.')

def slp1_one(x): 
 tranin = 'lsrhk'
 tranout = 'slp1'
 def transcode1(m):
  a = m.group(1)
  b = transcoder_processString(a,tranin,tranout)
  return '<s>%s</s>' %b

 y = re.sub(r'<s>(.*?)</s>',transcode1,x)
 return y

def slp1(lines):
 a = []
 n = 0
 for x in lines:
  y = slp1_one(x)
  if y != x:
   n = n + 1
  a.append(y)
 print('deva_markup: %d lines changed'%n)
 return a

def corrections(lines):
 """ some spelling corrections, in place """
 data = {
  #'':('',''),
  '00152':('karipyasi','karizyasi'),
  '00332':('upya','uzya'),
  '00398':('rAjIvAca','rAjovAca'),
  '02009':('{??}','^'),
  '02015':('{??}','^'),
  '02000':('{??}','^'),
  #'':('',''),
  #'':('',''),
  #'':('',''),
  #'':('',''),
  #'':('',''),
  #'':('',''),
 }
 n = 0
 for idx,line in enumerate(lines):
  m = re.search('^([0-9]+)(.*)$',line)
  if m:
   (num,text) = (m.group(1),m.group(2))
   if num in data:
    old,new = data[num]
    lines[idx] = line.replace(old,new)
    n = n + 1
 print('corrections in',n,'lines')
if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 with codecs.open(filein,"r","utf8") as f:
  lines = [x.rstrip('\r\n') for x in f]
  print(len(lines),"lines read from",filein)
 outlines = slp1(lines)
 corrections(outlines)

 with codecs.open(fileout,"w","utf8") as f:  
  for out in outlines:
   f.write(out+'\n')
 print(len(outlines),"records written to",fileout)
