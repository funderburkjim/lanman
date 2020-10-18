#-*- coding:utf-8 -*-
"""deva_markup.py
   04-10-2020

"""
from __future__ import print_function
import codecs,sys,re
import transcoder
from transcoder import transcoder_processString
transcoder.transcoder_set_dir('.')

def slp1_deva_one(x): 
 tranin = 'slp1'
 tranout = 'deva'
 def transcode1(m):
  a = m.group(1)
  b = transcoder_processString(a,tranin,tranout)
  return '<s>%s</s>' %b

 y = re.sub(r'<s>(.*?)</s>',transcode1,x)
 return y

def slp1_deva(lines):
 a = []
 n = 0
 for x in lines:
  y = slp1_deva_one(x)
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

 outlines = slp1_deva(lines)

 with codecs.open(fileout,"w","utf8") as f:  
  for out in outlines:
   f.write(out+'\n')
 print(len(outlines),"records written to",fileout)
