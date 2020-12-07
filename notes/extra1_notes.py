# coding=utf-8
""" extra1_notes.py
    See readme for discussion
"""
import sys,re,codecs

def adjust_lend_helper(lines,idx0,idx1):
 # modify lines in place
 # return boolean. False means no adjustment, True means adjustment
 lendline = lines[idx1]
 idx2 = idx1 - 1
 idx = idx2
 movelines = [lendline]
 while True:
  curline = lines[idx]
  # for BUR
  if (curline.startswith(('[Page','<H>'))) or (curline.strip() == ''):
   movelines.append(lines[idx])
   idx = idx - 1
  else:
   break
 if idx == idx2:  
  # usual case. No change needed
  return False
 # adjustment required. lines[idx] does NOT start with page or H.
 # put lendline first, then movelines
 j = 0
 for i in range(idx+1,idx1+1):
  lines[i] = movelines[j]
  j = j + 1
 return True

def unused_adjust_specialchars(inlines):
 """ change inlines in place"""
 nadj = 0
 replacements = [
  #(u'…',' '),
  ('--',u'—'),  # emdash
  #('<sic>',''), 
  (u'[µ',''), # wide-spacing left boundary
  (u'µ]',''), # wide-spacing right boundary
  (u'{µ',''), # wide-spacing left boundary
  (u'µ}',''), # wide-spacing right boundary
  (u'§',''),  # before certain <P>, <P1>
 ]
 for idx,line in enumerate(inlines):
  line1 = line
  for (old,new) in replacements:
   line1 = line1.replace(old,new)
  if line1 != line:
   nadj = nadj + 1
   inlines[idx]=line1
 print(nadj,"changes in 'adjust_specialchars'")

class Abbrev(object):
 def __init__(self,abbrv,meaning):
  self.abbrv = abbrv
  self.meaning = meaning
  # trailing period changed to [.] for regex search
  if abbrv.endswith('.'):
   abbrv1 = re.sub(r'[.]$','[.]',abbrv)
   self.regex = '([^a-zA-Z0-9>])' + abbrv1
   self.replace = r'\1<ab>%s</ab>' %abbrv
  else:
   abbrv1 = abbrv + '([^.])'
   self.regex = '([^a-zA-Z0-9>])' + abbrv1
   self.replace = r'\1<ab>%s</ab>\2' % abbrv
  self.count = 0 # number of instances found

def init_abbrevs(filein):
 #filein = "abbrev.txt"
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 recs = []
 for line in lines:
  if line.startswith(';'):
   continue
  abbrv,meaning = line.split(':')
  rec = Abbrev(abbrv,meaning)
  recs.append(rec)
 print(len(recs),"Abbreviations from",filein)
 return recs

def check_abbrev_helper(line,rec,dbg=False):
 # Some abbreviations are substrings of others.
 # e.g. 'f.' is substring of 'U. f.'.  We want
 # <ab>U. f.</ab> NOT <ab>U. <ab>f.</ab></ab>
 # In the caller, we assume <ab>U. f.</ab> is formed before f. is analyzed
 #dbg = (line == '--U. f. {@śrī-s@} (174) {@iva āyata-locanā,@} ‘like') and (rec.abbrv in ['U. f.','f.'])
 parts = re.split(r'(<ab>.*?</ab>)',line)
 newparts = []
 for part in parts:
  if part.startswith('<ab>'):
   newpart = part
  else:
   newpart = re.sub(rec.regex,rec.replace,part)
  newparts.append(newpart)
  if dbg:
   print('part=%s\nnewpart=%s\n' %(part,newpart))
 newline = ''.join(newparts)
 return newline

def check_abbrev(lines,fileabbr):
 recs = init_abbrevs(fileabbr)
 # sort by descending length
 recs.sort(key = lambda x: len(x.abbrv), reverse = True)
 #for rec in recs:
 # print('%2d %s' %(len(rec.abbrv),rec.abbrv))
 #exit(1)
 nchg = 0
 for iline,oldline in enumerate(lines):
  oldline1 = ' ' + oldline # to catch abbreviations at start of line
  line = oldline1
  for rec in recs:
   # dbg = (iline == 433) and (rec.abbrv in ['U. f.','f.'])
   line1 = check_abbrev_helper(line,rec)
   #line1 = re.sub(rec.regex,rec.replace,line)
   if line1 != line: 
    # in 72 cases, an abbreviation appears to be within bold text.
    # Examination shows this is probably always not an abbreviation
    #line1 = re.sub(r'({@[^@]*)<ab>(.*?)</ab>',r'\1\2',line1)
    if line1 != line:
     if True and (iline == 433):
      print(rec.abbrv,'Before',line)
      print(rec.abbrv,'After',line1)
     rec.count = rec.count+1
     line = line1
  if line != oldline1: # add markup
   assert line.startswith(' ')
   lines[iline] = line[1:] # remove initial space
   nchg = nchg + 1
 print("check_abbrev:",nchg,"lines changed")
 print("check_abbrev: list of abbreviation frequency")
 for rec in recs:
  print(rec.abbrv,rec.count)

def adjust_lang(inlines):
 """change inlines in place"""
 nadj = 0
 regexes0 = [
  #(r'<g>(.*?)</g>',r'<lang n="greek">\1</lang>'),
  (r'<gr></gr>',r'<lang n="greek"></lang>'),
  (r'<gr>-',r'<lang n="greek"></lang>-'),  # 27 cases
  (r'</gr>',r'<lang n="greek"></lang>'),   # 27 cases
  (r'<gr>,',r'<lang n="greek"></lang>,'),  #  3 cases
 ]
 regexes = [(re.compile(a),b) for (a,b) in regexes0]
 for idx,line in enumerate(inlines):
  line1 = line
  for (regex,repl) in regexes:
   line1 = re.sub(regex,repl,line1)
  if line1 != line:
   nadj = nadj + 1
   inlines[idx]=line1
 print(nadj,"lines changed in 'adjust_lang'")

def write_dbg(filein,outlines):
 with codecs.open(filein,"r","utf-8") as f:
  inlines = [x.rstrip('\r\n') for x in f]
 filedbg = "extra1_dbg.txt"
 with codecs.open(filedbg,"w","utf-8") as fout:
  nout = 0
  for iline,line in enumerate(outlines):
   #fout.write(line+'\n')
   oldline = inlines[iline]
   if oldline != line:
    nout = nout + 1
    outarr = []
    outarr.append('; Case %d'%nout)
    lnum = iline + 1
    outarr.append('%d old %s' %(lnum,oldline))
    outarr.append('%d new %s' %(lnum,line))
    for out in outarr:
     fout.write(out+'\n')
 print(nout,"cases written to",filedbg)

if __name__=="__main__":
 filein = sys.argv[1]  # 
 fileabbr = sys.argv[2] # abbreviation file
 fileout = sys.argv[3] # 
 with codecs.open(filein,"r","utf-8") as f:
  inlines = [x.rstrip('\r\n') for x in f]
  print(len(inlines),"lines read from",filein)
 #outlines = adjust_lend(inlines)
 #outlines = remove_lnum(outlines)
 outlines = inlines
 check_abbrev(outlines,fileabbr)
 #adjust_HI(outlines)
 #adjust_p(outlines)
 #adjust_num_section(outlines)
 #adjust_lang(outlines)
 
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print(len(outlines),"lines written to",fileout)
 if True: # dbg
  write_dbg(filein,outlines)  # we have to re-read inlines
