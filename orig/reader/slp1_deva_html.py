#-*- coding:utf-8 -*-
"""slp1_deva_html.py
   06-03-2020

"""
from __future__ import print_function
import codecs,sys,re
import transcoder
from transcoder import transcoder_processString
transcoder.transcoder_set_dir('.')

unused_tagchanges = {
  '<s>':'<s>',  '</s>':'</s>',
  '<section>':'<section>',  '</section>':'</section>',
  '<p>':'<p>',  '</p>':'</p>',
  '<l>':'', '</l>':'', 
  '<lg>':'', '</lg>':'', 
  '<head>':'<h2>', '</head>':'</h2>', 
 }

def adjust_non_s_tags(x):
 parts = re.split(r'(<.*?>)',x)
 newparts = []
 tagchanges = {
  '<s>':'<s>',  '</s>':'</s>',
  '<section>':'<span class="section">',  '</section>':'</span>',
  '<p>':'<span class="p">',  '</p>':'</span>',
  '<l>':'', '</l>':'', 
  '<lg>':'', '</lg>':'', 
  '<head>':'<span class="head">', '</head>':'</span>', 
 }
 for part in parts:
  #if True:print('part=',part)
  if not part.startswith('<'):
   newparts.append(part)
   continue
  if part in tagchanges:
   newpart = tagchanges[part]
   newparts.append(newpart)
  else:
   print('ERROR: unknown tag:"%s"'%part)
   print('line=',x)
   exit(1)
 newline = ''.join(newparts)
 if False:
  print('old=',x)
  print('new=',newline)
  print()
 return newline

def slp1_deva_one(x): 
 tranin = 'slp1'
 tranout = 'deva'
 m = re.search(r'^\[Page.*?\]$',x)
 if m:
  return x+'<br/>'

 def transcode1(m):
  a = m.group(1)
  b = transcoder_processString(a,tranin,tranout)
  return '<span class="deva">%s</span>' %b

 m = re.search(r'^([0-9][0-9][0-9][0-9][0-9]) (.*)$',x)
 lnum = m.group(1)
 body = m.group(2)
 body1 = adjust_non_s_tags(body)
 y = re.sub(r'<s>(.*?)</s>',transcode1,body1)
 if y.startswith('<span'):
  z = lnum + ' ' + y + '<br/>'
 else:
  z = lnum + ' ' + y 
 return z

def html_before():
 return """<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
<title>lsr2 Devanagari</title>
<style>
@font-face { 
 src: url('Sanskrit2003.ttf');
 font-family: sanskrit2003;

}
.deva {
 color:teal;
 font-size:16px;
 font-weight: normal; 
 font-family: sanskrit2003;
}
</style>

</head>

<body>
""".splitlines()

def html_after():
 return """
</body>
</html>
""".splitlines()

def slp1_deva(lines):
 a = []
 a = a + html_before()
 n = 0
 for x in lines:
  y = slp1_deva_one(x)
  if y != x:
   n = n + 1
  a.append(y)
 print('deva_markup: %d lines changed'%n)
 a = a + html_after()
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
