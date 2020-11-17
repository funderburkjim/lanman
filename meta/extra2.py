# coding=utf-8
""" extra2.py
    See readme.txt for discussion
"""
import sys,re,codecs

def adjust_hyphen(lines):
 """Some lines end with 'X-'.
   get the rest, Y, from next line
   replace first line with XY <lbinfo n="X-Y"/>
   Remove Y from next line
 """
 nadj = 0
 regbeg = r'( [^ ]*)-$'
 regend = r'^(.*?[ .;,])'
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  if not oldline.endswith('-'):
   continue
  if oldline.endswith('--'):
   continue
  if oldline.endswith('</lang>-'):
   continue
  line = oldline
  m = re.search(regbeg,line)
  beg = m.group(1)
  i = 1
  while True:
   iline1 = iline+i
   line1 = lines[iline1]
   if line1.startswith('[Page'):
    i = i + 1
    continue
   if line1.startswith(('<L>','<LEND>')):
    print('adjust_hyphen ERROR 1 at line',iline1,line1)
    exit(1)
   m = re.search(regend,line1)
   if not m:
    print('adjust_hyphen ERROR 2 at line',iline1,line1)
    exit(1)
   end = m.group(1)
   # do the correction
   newline = re.sub(regbeg,r'\1' + end,line)
   begend = '%s-%s'%(beg,end)
   begend = begend.strip()
   lbinfo = ' <lbinfo n="%s"/>'%begend
   newline = newline + lbinfo
   lines[iline] = newline
   newline1 = re.sub(regend,'',line1)
   lines[iline1] = newline1
   nadj = nadj + 1
   break # While True
 print(nadj,"cases changed in 'adjust_hyphen'")

def adjust_hyphen_bold(lines):
 """Some lines end with 'X-@}'.
   get the rest, Y, from next line {@Y.
   replace first line with XY@} <lbinfo n="X-Y"/>
   Remove Y from next line
 """
 nadj = 0
 regbeg = r'( [^ ]*)-@}$'
 regend = r'^{@(.*?[ .;,@])'
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  if not oldline.endswith('-@}'):
   continue
  line = oldline
  m = re.search(regbeg,line)
  beg = m.group(1)
  i = 1
  while True:
   iline1 = iline+i
   line1 = lines[iline1]
   if line1.startswith('[Page'):
    i = i + 1
    continue
   if line1.startswith(('<L>','<LEND>')):
    print('adjust_hyphen ERROR 1 at line',iline1,line1)
    exit(1)
   m = re.search(regend,line1)
   if not m:
    print('adjust_hyphen WARNING 2 at line',iline1,line1)
    break
   end = m.group(1)
   # do the correction
   if end.endswith('@'):
    end1 = end[0:-1]
    newline = re.sub(regbeg,r'\1' + end1 +'@}',line)
   else:
    end1 = end
    newline = re.sub(regbeg,r'\1' + end1 +'@}',line)

   begend = '%s-%s'%(beg,end1)
   begend = begend.strip()
   begend1 = re.sub(r'{@','',begend)
   lbinfo = ' <lbinfo n="%s"/>'%begend1
   newline = newline + lbinfo
   lines[iline] = newline
   newline1 = re.sub(regend,'{@',line1)
   newline1 = re.sub(r'{@ *@}','',newline1)
   newline1 = newline1.lstrip()
   newline1 = re.sub(r'^{@ +','{@',newline1)
   newline1 = re.sub(r' *{@}','',newline1)
   newline1 = newline1.lstrip()
   lines[iline1] = newline1
   nadj = nadj + 1
   break # While True
 print(nadj,"cases changed in 'adjust_hyphen_bold'") 

def adjust_hyphen_italic(lines):
 """Some lines end with 'X-%}'.
   get the rest, Y, from next line {%Y.
   replace first line with XY%} <lbinfo n="X-Y"/>
   Remove Y from next line
 """
 nadj = 0
 regbeg = r'( [^ ]*)-%}$'
 regend = r'^{%(.*?[ .;,%])'
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  if not oldline.endswith('-%}'):
   continue
  if oldline.endswith('--%}'):
   continue # 2 cases
  line = oldline
  m = re.search(regbeg,line)
  beg = m.group(1)
  i = 1
  while True:
   iline1 = iline+i
   line1 = lines[iline1]
   if line1.startswith('[Page'):
    i = i + 1
    continue
   if line1.startswith(('<L>','<LEND>')):
    print('adjust_hyphen ERROR 1 at line',iline1,line1)
    exit(1)
   m = re.search(regend,line1)
   if not m:
    print('adjust_hyphen WARNING 2 at line',iline1,line1)
    break
   end = m.group(1)
   # do the correction
   if end.endswith('%'):
    end1 = end[0:-1]
    newline = re.sub(regbeg,r'\1' + end1 +'%}',line)
   else:
    end1 = end
    newline = re.sub(regbeg,r'\1' + end1 +'%}',line)
   #newline = re.sub(regbeg,r'\1' + end +'%}',line)
   begend = '%s-%s'%(beg,end)
   begend = begend.strip()
   begend1 = re.sub(r'{%','',begend)
   lbinfo = ' <lbinfo n="%s"/>'%begend1
   newline = newline + lbinfo
   lines[iline] = newline
   newline1 = re.sub(regend,'{%',line1)
   newline1 = re.sub(r'{% *%}','',newline1)
   newline1 = newline1.lstrip()
   newline1 = re.sub(r'^{% +','{%',newline1)
   newline1 = re.sub(r'^ *{%}','',newline1)
   newline1 = newline1.lstrip()
   lines[iline1] = newline1
   nadj = nadj + 1
   break # While True
 print(nadj,"cases changed in 'adjust_hyphen_italic'")

if __name__=="__main__":
 filein = sys.argv[1]  # xxxwithmeta1.txt
 fileout = sys.argv[2] # xxxwithmeta2.txt
 with codecs.open(filein,"r","utf-8") as f:
  inlines = [x.rstrip('\r\n') for x in f]
  print(len(inlines),"lines read from",filein)
 outlines = inlines
 adjust_hyphen(outlines)
 adjust_hyphen_bold(outlines)
 adjust_hyphen_italic(outlines)
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print(len(outlines),"lines written to",fileout)
