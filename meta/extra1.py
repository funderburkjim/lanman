# coding=utf-8
""" extra1.py
    See readme.txt for discussion
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

def adjust_lend(inlines):
 ans = []
 idx0 = None
 nadj = 0
 for idx,line in enumerate(inlines):
  if line.startswith('<L>'):
   idx0 = idx
  ans.append(line)
  if line.startswith('<LEND>'):
   if adjust_lend_helper(ans,idx0,idx):
    nadj = nadj + 1
    #out = "LEND Adjustment # %s (%s): %s" %(nadj,idx+1,inlines[idx0])
    #print(out )
 print('adjust_lend. %s adjustments'%nadj)
 return ans

def remove_lnum(outlines):
 ans = []
 for line in outlines:
  m = re.search(r'^[0-9][0-9][0-9][0-9][0-9] (.*)$',line)
  if m:
   newline = m.group(1)
  else:
   # page breaks
   # meta line  <L>...
   # end meta line <LEND>...
   newline = line
  ans.append(newline)
 return ans

def unused_adjust_empty(inlines):
 ans = []
 nadj = 0
 inflag = False
 for idx,line in enumerate(inlines):
  if line.startswith('<L>'):
   ans.append(line)
   inflag = True
  elif line.startswith('<LEND>'):
   ans.append(line)
   inflag = False
  elif not inflag:
   ans.append(line)
  elif line == '':
   nadj = nadj + 1   # skip this line
  else:
   ans.append(line)
 print(nadj,"empty lines removed")
 return ans


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

def unused_adjust_div_lb(inlines):
 """ change inlines in place"""
 nadj = 0
 replacements = [
  #('<><H>','<H>'), # letter break. Outside entries
  ('<>','<div n="lb">'),
  #('<P1>','<div n="P1">'),
  #('<H>','<div n="H">'),

 ]
 for idx,line in enumerate(inlines):
  line1 = line
  for (old,new) in replacements:
   line1 = line1.replace(old,new)
  if line1 != line:
   nadj = nadj + 1
   inlines[idx]=line1
 print(nadj,"changes in 'adjust_div_lb'")

def unused_adjust_div_HI_c(inlines):
 """ change inlines in place"""
 nadj = 0
 replacements = [
  (u'<HI>(c[.] {#.*?#})¦?',r'<div n="pfx">\1'), # prefix for verb
 ]
 flag = False
 for idx,line in enumerate(inlines):
  if line.startswith('<L>'):
   flag = True
   continue
  if line.startswith('<LEND>'):
   flag = False
   continue
  if line.startswith('[Page'):
   continue
  if not flag:  
   continue
  line1 = line
  for (old,new) in replacements:
   line1 = re.sub(old,new,line1)
  if line1 != line:
   nadj = nadj + 1
   inlines[idx]=line1
  elif line.startswith('<HI>'):
   # make note of any variants
   out = "check_HI_c: %s %s" %(idx+1,line)
   print(out  )
 print(nadj,"changes in 'adjust_div_HI_c'")


def unused_adjust_page(inlines):
 """ change inlines in place
  Change [Page0v.pppp] to [Pagev-pppp], so page break format consistent
  with the meta-line variable <pc>
 """
 nadj = 0
 nwarn=0
 regex = re.compile(r'^\[Page0(.)[.](....)\]$')
 for idx,line in enumerate(inlines):
  if not line.startswith('[Page'):
   continue
  line1 = re.sub(regex,r'[Page\1-\2]',line)
  if line1 == line:
   print("adjust_page WARNING at line#",idx+1,line.encode('utf-8'))
   nwarn = nwarn+1
  else:
   nadj = nadj + 1
   inlines[idx]=line1
 print(nadj,"changes in 'adjust_page' AND",nwarn,"WARNINGS")

def adjust_lex(inlines):
 """ change inlines in place"""
 nadj = 0
 replacements = [(u'•%s.'%x,'<lex>%s.</lex>'%x) for x in ['adj','f','m','n']]
 for idx,line in enumerate(inlines):
  line1 = line
  if not u'•' in line: # for efficiency
   continue
  for (old,new) in replacements:
   line1 = line1.replace(old,new)
  if line1 != line:
   nadj = nadj + 1
   inlines[idx]=line1
 print(nadj,"changes in 'adjust_lex'")

def adjust_ls(inlines):
 ans = []
 nadj = 0
 regex0 = u'¯{¤(.*?)¤}'
 regex = re.compile(regex0)
 regex0a = r'<ls>([^(<]*)\)</ls>'
 regex1 = re.compile(regex0a)
 regex0b = r'<ls>\(([^<]*)\)</ls>'
 regex2 = re.compile(regex0b)
 for idx,line in enumerate(inlines):
  line1 = re.sub(regex,r'<ls>\1</ls>',line)
  if line1 != line:
   nadj = nadj + 1
   # insert a space between consecutive <ls>X</ls><ls>Y</ls>
   line1 = line1.replace('</ls><ls>','</ls> <ls>')
   # replace )</ls> with </ls>), provided there is no LP in the ls.
   line1 =re.sub(regex1,r'<ls>\1</ls>)',line1)
   # replace <ls>(X)</ls> with (<ls>X</ls>) about 1000
   line1 = re.sub(regex2,r'(<ls>\1</ls>)',line1)
   line = line1
  ans.append(line)
 print(nadj,"lines changed in 'adjust_ls'")
 return ans


def adjust_sic(inlines):
 ans = []
 nadj = 0
 for idx,line in enumerate(inlines):
  if '<sic>'  in line:
   line = line.replace('<sic>','<sic/>')
   nadj = nadj + 1
  ans.append(line)
 print(nadj,"changes in 'adjust_sic'")
 return ans

def adjust_e(inlines):
 """ <e> tag occurs at end of meta line for about 4000 cases
   Adjusts inlines list
 """
 nadj = 0
 for idx,line in enumerate(inlines):
  m = re.search(r'^<L>(.*?)<.*<e>(.*)$',line)
  if not m:
   continue
  # save contents for next line
  L = m.group(1)
  e = m.group(2)
  # remove in current line
  line = re.sub(r'<e>(.*)$','',line) 
  inlines[idx]=line
  # Begin work on next line
  idx1 = idx + 1
  line1 = inlines[idx1]
  line1a = line1
  nadj = nadj + 1
  # most common case: e = ',' Install comma after broken bar
  if e == ',':
   line1a = line1.replace(u'¦',u'¦' + e)
  elif e == ';':
   # 6 cases
   # by examination of print, semicolons also go after broken bar
   line1a = line1.replace(u'¦',u'¦' + e)
  elif e == '.':
   # 18 cases. Examine text for all, and change acc. to L-number
   if L in ['20037','21088','76824',]:
    # The period should be a comma
    line1a = line1.replace(u'¦',u'¦' + ',')
   elif L in ['18263']:
    # no change to line1. line1a has default value of line1
    line1a = line1
   elif L in ['24522','25039','27684','31905','46978','95091',
               '95384','95903','100552','101350','108579','109595',
              '118631','119452']:
    # retain the period after broken bar
    line1a = line1.replace(u'¦',u'¦' + '.')
   else: # don't know
    print(line.encode('utf-8'),"   e=",e)
    print(line1.encode('utf-8'))
  elif e == '^(1)':
   # 1 case L = 122349
   # This is a homonym number in parens.
   # Insert (1.) at beginning of line1
   line1a = '(1.) ' + line1
  else:
   print(line.encode('utf-8'),"   e=",e)
   print(line1.encode('utf-8'))
  # install modified next line
  inlines[idx1] = line1a
 print(nadj,"changes in 'adjust_e'")
 #return ans

def unused_adjust_wide_helper1(x):
 # some special cases
 """
 if x in ['-','10','2','=','?']:
  # example  in Mitra - Varuna
  # Don't add <is> tag.
  return x  
 """
 # see https://github.com/sanskrit-lexicon/Cologne/issues/190#issuecomment-345485448
 #if x in ['Nax']:
 # # part of literary source (book or article by Weber)
 # return x
 m = re.search(r'^([\(\[]*)(.*?)([),.:;!\]]*)$',x)
 a = m.group(1) # usu empty string
 b = m.group(2)
 c = m.group(3) # usu empty string
 # don't remove 's at end. -- baSed on print, the 's is also widely spaced
 """
 if b.endswith(r"'s"):
 # also, remove 's at end 
  b = b[0:-2]
  c = "'s" + c
 """
 if b in ['-','10','2','=','?']:
  y = a + b + c  # no <is>
 else:
  y = a + ('<is>%s</is>'%b) + c
 return y

def unused_adjust_wide_helper(m):
 """
 m.group(0) = †{X}
 m.group(1) = X
 Usually, we want to return <is>X</is>
 However, we want to do some 'cleaning' of X first.
 E.g., if X = (Y), we want to return (<is>Y</is>)
 and if X = Y Z, we want to return <is>Y</is> <is>Z</is>
 """
 x = m.group(1)
 # 1) split on spaces
 parts = re.split(r' +',x)
 outs = []  # cleanup of each part of x
 for part in parts:
  out = adjust_wide_helper1(part)
  outs.append(out)
 # reconstruct a string, by inserting spaces
 ans = ' '.join(outs)
 return ans

def unused_adjust_wide(inlines):
 """change inlines in place"""
 nadj = 0
 regexes0 = [
  (u'†{(.*?)}',r'<is>\1</is>')
 ]
 regexes = [(re.compile(a),b) for (a,b) in regexes0]
 for idx,line in enumerate(inlines):
  line1 = line
  for (regex,repl) in regexes:
   #line1 = re.sub(regex,repl,line1)
   line1 = re.sub(regex,adjust_wide_helper,line1)
  if line1 != line:
   nadj = nadj + 1
   inlines[idx]=line1
 print(nadj,"lines changed in 'adjust_wide'")

def unused_adjust_wide1(inlines):
 """change inlines in place  
    a smaller batch of <is> tags
 """
 nadj = 0
 regexes0 = [
  (u'†([A-Za-z0-9]+)',r'<is>\1</is>')
 ]
 regexes = [(re.compile(a),b) for (a,b) in regexes0]
 for idx,line in enumerate(inlines):
  if not re.search(u'†',line):
   continue
  line1 = line
  for (regex,repl) in regexes:
   #line1 = re.sub(regex,repl,line1)
   line1 = re.sub(regex,repl,line1)
  if line1 != line:
   nadj = nadj + 1
   inlines[idx]=line1
 print(nadj,"lines changed in 'adjust_wide1'")

def unused_check_Htag(inlines):
 """ Look for any <H> or <H1> within scope of <L>...<LEND>"""
 nadj = 0
 entryFlag=False  # are we in scope of <L>, <LEND> ?
 for idx,line in enumerate(inlines):
  if line.startswith('<L>'):
   entryFlag = True
   continue
  if line.startswith('<LEND>'):
   entryFlag = False
   continue
  # not a meta line
  if entryFlag:
   # we are in an entry
   if '<H' in line:
    nadj = nadj + 1
    print("Case",nadj,"of '<H' at line#",idx+1)
    print(line.encode('utf-8'))
    print
 print(nadj,"'<H' instances in entries. (check_Htag)")

def unused_adjust_blanklines(inlines):
 """ Insert blank line preceding each meta-line 
 """
 ans = []
 for idx,line in enumerate(inlines):
  if line.startswith('<L>'):
   ans.append('')
  ans.append(line)
 return ans

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

def init_abbrevs():
 filein = "abbrev.txt"
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

def check_abbrev(lines):
 recs = init_abbrevs()
 nchg = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  oldline1 = ' ' + oldline # to catch abbreviations at start of line
  line = oldline1
  for rec in recs:
   line1 = re.sub(rec.regex,rec.replace,line)
   if line1 != line: 
    # in 72 cases, an abbreviation appears to be within bold text.
    # Examination shows this is probably always not an abbreviation
    line1 = re.sub(r'({@[^@]*)<ab>(.*?)</ab>',r'\1\2',line1)
    if line1 != line:
     rec.count = rec.count+1
     line = line1
  if line != oldline1: # add markup
   assert line.startswith(' ')
   lines[iline] = line[1:] # remove initial space
   nchg = nchg + 1
 print("check_abbrev:",nchg,"lines changed")
 for rec in recs:
  print(rec.abbrv,rec.count)

def adjust_HI(lines):
 nchg = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  line = re.sub(r'^<HI>({@[^+][^@]*?@}¦)',r'\1',oldline)
  if line != oldline:
   lines[iline] = line
   nchg = nchg + 1
   continue
  line = re.sub(r'^<HI>({@[+][^@]*?@})¦',r'<div n="p"/>\1',oldline)
  if line != oldline:
   lines[iline] = line
   nchg = nchg + 1
   continue
 print("adjust_HI:",nchg,"lines changed")
 #for rec in recs:
 # print(rec.abbrv,rec.count)

def adjust_p(lines):
 nchg = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  line = oldline
  # make <p>...</p>   <div n="1"/>  (an empty tag. not closed by make_xmlp.py)
  line = line.replace('<p>','<div n="1"/>')
  #line = line.replace('</p>','</div>')
  line = line.replace('</p>','')
  if line != oldline:
   lines[iline] = line
   nchg = nchg + 1
   continue
 print("adjust_p:",nchg,"lines changed")

def adjust_num_section(lines):
 nchg = 0
 for iline,oldline in enumerate(lines):
  if oldline.startswith(('<L>','<LEND>')):
   continue
  line = oldline
  # make <p>...</p>   <div n="1"/>  (an empty tag. not closed by make_xmlp.py)
  # — == emdash
  line = re.sub(r'{@--([1-9]+)',r'<div n="2"/>{@—\1',line)
  if line != oldline:
   lines[iline] = line
   nchg = nchg + 1
   continue
 print("adjust_num_section:",nchg,"lines changed")

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


if __name__=="__main__":
 filein = sys.argv[1]  # xxxwithmeta1.txt
 fileout = sys.argv[2] # xxxwithmeta2.txt
 with codecs.open(filein,"r","utf-8") as f:
  inlines = [x.rstrip('\r\n') for x in f]
  print(len(inlines),"lines read from",filein)
 outlines = adjust_lend(inlines)
 outlines = remove_lnum(outlines)
 check_abbrev(outlines)
 adjust_HI(outlines)
 adjust_p(outlines)
 adjust_num_section(outlines)
 adjust_lang(outlines)
 
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print(len(outlines),"lines written to",fileout)
