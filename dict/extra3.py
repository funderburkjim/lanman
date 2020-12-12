# coding=utf-8
""" extra3.py
    See readme.txt for discussion
"""
import sys,re,codecs

def adjust_page_line_helper(line):
 parts = re.split(r'([0-9]+\^[0-9]+\^)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^([0-9]+)\^([0-9]+)\^$',part)
  if m:
   pagenum = int(m.group(1))
   if pagenum <= 106:
    newpart = '<ls n="lan,%s,%s">%s</ls>' %(m.group(1),m.group(2),part)
    newparts.append(newpart)
   else:
    newparts.append(part)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_page_line(lines):
 """ X^Y^  (X and Y digit-sequences) ->
   <ls n="lan,X,Y">X^Y</ls>
   X <= 106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = adjust_page_line_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
 print(nadj,"cases changed in 'adjust_page_line'")

def adjust_page_lines_helper(line):
 parts = re.split(r'([0-9]+\^[0-9]+[, ]+[0-9, ]+\^)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^([0-9]+)\^([0-9]+[, ]+[0-9, ]+)\^$',part)
  if m:
   pagenum = int(m.group(1))
   if pagenum <= 106:
    newpart = '<ls n="lan,%s,%s">%s</ls>' %(m.group(1),m.group(2),part)
    newparts.append(newpart)
   else:
    newparts.append(part)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_page_lines(lines):
 """ X^Y^  (X and Y digit-sequences) ->
   <ls n="lan,X,Y">X^Y</ls>
   X <= 106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = adjust_page_lines_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False:
    print('; Case %s' % nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_page_line'")

def adjust_whitney_sup_helper(line):
 parts = re.split(r'([0-9]+\^[0-9]+\^)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^([0-9]+)\^([0-9]+)\^$',part)
  if m:
   section = int(m.group(1))
   if section > 106:
    newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),part)
    newparts.append(newpart)
   else:
    newparts.append(part)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_sup(lines):
 """ X^Y^  (X and Y digit-sequences) ->
   <ls n="wg,X">X^Y</ls>
   X>106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = adjust_whitney_sup_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
 print(nadj,"cases changed in 'adjust_whitney_sup'")

def adjust_whitney_az_helper(line):
 parts = re.split(r'([0-9][0-9][0-9]+[a-z])',line)
 newparts = []
 for part in parts:
  m = re.search(r'^([0-9][0-9][0-9]+)([a-z])$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),part)
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_az(lines):
 """ X^Y^  (X and Y digit-sequences) ->
   <ls n="wg,X">X^Y</ls>
   X>106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = adjust_whitney_az_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
 print(nadj,"cases changed in 'adjust_whitney_az'")

def adjust_whitney_4_period_helper(line):
 parts = re.split(r'(1[0-9][0-9][0-9][.,\]])',line)
 newparts = []
 for part in parts:
  m = re.search(r'^(1[0-9][0-9][0-9])([.,\]])$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),part)
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_4_period(lines):
 """ X.  X a 4-digit sequence, then a period or comma or right square bracket->
   <ls n="wg,X">X.</ls>
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = adjust_whitney_4_period_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
 print(nadj,"cases changed in 'adjust_whitney_4_period'")

def adjust_whitney_3_period_helper(line):
 parts = re.split(r'([0-9][0-9][0-9][.,\]])|(<ls.*?</ls>)',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  m = re.search(r'^([0-9][0-9][0-9])([.,\]])$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),part)
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_3_period(lines):
 """ X.  X a 4-digit sequence, then a period or comma or right square bracket->
   <ls n="wg,X">X.</ls>
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = adjust_whitney_3_period_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: 
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_whitney_3_period'")

def adjust_whitney_3a_helper(line):
 parts = re.split(r'([\[ ][0-9][0-9][0-9]+)|(<ls.*?</ls>)',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  m = re.search(r'^([\[ ])([0-9][0-9][0-9]+)$',part)
  if m:
   newpart = '%s<ls n="wg,%s">%s</ls>' %(m.group(1),m.group(2),m.group(2))
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_3a(lines):
 """ ZX  where Z is space or [
    and X is a sequence of 3 or more digits
   Z<ls n="wg,X">X</ls>
  We exclude 3 known lines 
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  if (iline+1) in [9834, 11588, 15668]:
   # transform not applicable: not a whitney reference
   continue
  newline = adjust_whitney_3a_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False:
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_whitney_3a'")

def adjust_whitney_3b_helper(line):
 parts = re.split(r'(^[0-9][0-9][0-9]+)',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  m = re.search(r'^([0-9][0-9][0-9]+)$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),m.group(1))
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_3b(lines):
 """ X at beginning of line, where 
   X is a sequence of 3 or more digits
   Z<ls n="wg,X">X</ls>
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  #if (iline+1) in [9834, 11588, 15668]:
   # transform not applicable: not a whitney reference
   continue
  newline = adjust_whitney_3b_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if True: 
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_whitney_3b'")

def adjust_whitney_2b_helper(line):
 parts = re.split(r'(^[0-9][0-9]+)',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  m = re.search(r'^([0-9][0-9]+)$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),m.group(1))
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_2b(lines):
 """ X at beginning of line, where 
   X is a sequence of 2 or more digits
   but only for a particular set of lines
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  if (iline+1) not in [38,5213, 12054, 17320, 17693]:
   # transform not applicable: not a whitney reference
   continue
  newline = adjust_whitney_2b_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if True: 
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_whitney_2b'")

def adjust_sup(lines):
 """ ^X^ -> <sup>X</sup>
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = re.sub(r'\^(.*?)\^',r'<sup>\1</sup>',oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: 
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))
 print(nadj,"cases changed in 'adjust_sup'")

def adjust_whitney_Whitney_helper(line):
 parts = re.split(r'(Whitney,? +[0-9]+[a-z]?)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^(Whitney,? +)([0-9]+)([a-z]?)$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(2),part)
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_Whitney(lines):
 """ Whitney XY -> 
   <ls n="wg,X">Whitney XY</ls>
   X>106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = adjust_whitney_Whitney_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
 print(nadj,"cases changed in 'adjust_whitney_Whitney'")

def adjust_whitney_see_helper(line):
 # see X or {%see%} X
 parts = re.split(r'({?%?see%?}? +[0-9]+[a-z]?)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^({?%?see%?}? +)([0-9]+)([a-z]?)$',part)
  if m:
   newpart = '%s<ls n="wg,%s">%s%s</ls>' %(m.group(1),m.group(2),m.group(2),m.group(3))
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_see(lines):
 """ Whitney XY -> 
   <ls n="wg,X">Whitney XY</ls>
   X>106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  newline = adjust_whitney_see_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False:
    print('; Case %s' % nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))
 print(nadj,"cases changed in 'adjust_whitney_see'")

if __name__=="__main__":
 filein = sys.argv[1]  # xxxwithmeta1.txt
 fileout = sys.argv[2] # xxxwithmeta2.txt
 with codecs.open(filein,"r","utf-8") as f:
  inlines = [x.rstrip('\r\n') for x in f]
  print(len(inlines),"lines read from",filein)
 outlines = inlines
 adjust_page_line(outlines)
 adjust_page_lines(outlines)
 adjust_whitney_sup(outlines)
 adjust_whitney_az(outlines)
 adjust_whitney_Whitney(outlines)
 adjust_whitney_see(outlines)
 adjust_whitney_4_period(outlines)
 adjust_whitney_3_period(outlines)
 adjust_whitney_3a(outlines)
 adjust_whitney_3b(outlines)
 adjust_whitney_2b(outlines)
 adjust_sup(outlines)
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print(len(outlines),"lines written to",fileout)
