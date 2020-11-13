# coding=utf-8
""" close_bold.py for lan
   11-13-2020

"""
from __future__ import print_function
import sys, re,codecs

def unused_italic_adjust(line,lnum):
 adj = {
  22525: (
   "et {%klis2t2a.%} Agiter, tourmenter: {%maru%}||{%tas [Page194-1]%}",
   "et {%klis2t2a.%} Agiter, tourmenter: {%maru%}||{%tas%} [Page194-1]"
  ),
  31994: (
   "{%[Page271-2] jus2antu%} que les dieux nous accordent cela, Vd. ;; Se",
   "[Page271-2]{% jus2antu%} que les dieux nous accordent cela, Vd. ;; Se"
  )
 }
 if lnum in adj:
  (old,new) = adj[lnum]
  assert line == old,"italic adjust error"
  return new
 # otherwise, change %}||{% to || (6 cases)
 new = line.replace('%}||{%','||')
 return new
class Subls(object):
 def __init__(self,idx,nls,fls):
  self.idx = idx
  self.nls = nls
  self.fls = fls

def make_subls(sublsObj):
 def subls(m):
  # for adjusting page breaks with an ls
  # m.group(0) = {¤X¤}
  x0 = m.group(0)
  x = m.group(1)
  if not ('[Page' in x):  # almost always True
   return x0
  # we do have a page break 
  # separate x into a + [Page...] + b
  # replace with a + b 
  m1 = re.search(r'^(.*?)(\[Page.*?\])(.*)$',x)
  a = m1.group(1)
  p = m1.group(2) # [Page...]
  b = m1.group(3)
  # return {¤ + a + b + ¤} + p, so entire ls ref precedes page break
  y = u'{¤' + a + b + u'¤}' + p
  # before returning y, update the documentation of this
  sublsObj.nls = sublsObj.nls + 1
  idx = sublsObj.idx
  fls = sublsObj.fls
  out = "%04d %s %s" %(sublsObj.nls,idx+1,x0)  
  fls.write(out + '\n')
  return y
 return subls

def line_page_adj(lines):
 """ The page-col break notation is [Page...]
 """
 # keep track of adjustments to page breaks within ls, as we make a
 # variance from the printed text here.
 filels="lan_ls_page_adj.txt"
 fls = codecs.open(filels,"w","utf-8")
 print("OPENING",filels)
 # prepare sublsObj for use in loop
 sublsObj = Subls(0,0,fls)  # idx,nls,fls
 # page break regex
 rePage = re.compile(r"\[Page(.*?)]")   # 
 # We must wrap 
 # end of subls
 ans = [] # new array of lines
 rePageAfter = re.compile(r"\[Page.*?\]") 
 # the first page break is handled separately, not by foundfirst Logic
 foundfirst=True  
 # next flag is True when we need to add an extra {% at beginning of next line
 pending_italic = False
 # similar for bold
 pending_bold = False
 nls = 0
 for idx,line in enumerate(lines):
  if idx > 1000000: #2000: 
   print("DEBUG QUIT at idx=",idx)
   break
  if pending_italic:
   assert line.startswith('<>'),"PENDING ITALIC ERROR. idx=%s"%idx
   line = line.replace('<>','<>{%')
   pending_italic=False  # unset the flag
   out = 'PENDING ITALIC: %05d %s' %(idx+1,line)
   fls.write(out + '\n')
   nls = nls + 1
  elif pending_bold:
   assert line.startswith('<>'),"PENDING BOLD ERROR. idx=%s"%idx
   line = line.replace('<>','<>{@')
   pending_bold=False  # unset the flag
   out = 'PENDING BOLD: %05d %s' %(idx+1,line)
   fls.write(out + '\n')
   nls = nls + 1 
  if not re.search(rePage,line): 
   ans.append(line)
   continue
  ans1 = []
  idx0 = 0
  l = len(line)
  for m in rePage.finditer(line):
   idx1 = m.end()   
   idx1a=m.start()  # start of [Page...]
   line1 = line[idx0:idx1a]
   ans1.append(line1)
   pagetmp = line[idx1a:idx1] # [Page...]
   pagetmp1 = pagetmp[1:-1]   # Page.*
   linepage = '[' + pagetmp1 + ']' # same as pagetmp for pwg
   ans1.append(linepage)
   idx0 = idx1
  # possible text after last
  if idx0 < l:
   line1 = line[idx0:l]
   if re.search(r'^ *$',line1):
    # don't append all blanks
    pass
   else:
    # there IS extra text after [Page..]
    ans1.append(line1)
  if not foundfirst:
   # special handling for first instance of Page
   # We know that ans1 has TWO elements
   if False:  # debug messages
    print("First:,len ans1=",len(ans1))
    for itmp,xtmp in enumerate(ans1):
     print("check first before:",itmp,xtmp.encode('utf-8'))
   foundfirst = True
   assert len(ans1)==2,"foundfirst ERROR"
   ans1 = [ans1[1],ans1[0]]   # Put the Page first
   if False:  # debug messages
    for itmp,xtmp in enumerate(ans1):
     print("check first after:",itmp,xtmp.encode('utf-8'))
  # --------------------------------------
  # ans1 loop has ended.
  # Adjustments to ans1
  # Adjustment #1
  # Often, page-break lines have space characters at end.
  # There is no reason for this in any line.
  # Thus, trim ending spaces in all lines
  # Similarly, trim beginning spaces in all lines
  #  [They are only introduced by our splitting.
  for itmp,xtmp in enumerate(ans1):
   if xtmp.endswith(' ') or xtmp.startswith(' '):
    xtmp = re.sub(r' +$','',xtmp) # remove trailing blanks
    xtmp = re.sub(r'^ +','',xtmp) # remove initial blanks.
    ans1[itmp]=xtmp
  # Adjustment #2
  # In some cases, a page break formerly occured within a section of
  # italic text. After introducing a new line , the line before the
  #  [Page] line has an unclosed open-italic, and the line after has an
  # an unclosed close-italic. 
  # Adjust so that these unclosed parts are reclosed.
  # Previous examination (in Emacs) shows that the original line has NO
  # unclosed italic sections.
  for itmp,xtmp in enumerate(ans1):
   if re.search(r'{%[^%]*$',xtmp):
    xtmp = xtmp + '%}'
    ans1[itmp]=xtmp
    assert ans1[itmp+1].startswith('[Page'), "ITALIC CLOSURE ERROR"
    if (itmp+2) < len(ans1):
     ans1[itmp+2] = '{%' + ans1[itmp+2]
    else:
     # need next line to start with {%
     pending_italic=True
   elif re.search(r'{@[^@]*$',xtmp):
    xtmp = xtmp + '@}'
    ans1[itmp]=xtmp
    assert ans1[itmp+1].startswith('[Page'), "BOLD CLOSURE ERROR"
    if (itmp+2) < len(ans1):
     ans1[itmp+2] = '{@' + ans1[itmp+2]
    else:
     # need next line to start with {@
     pending_bold=True
  # Possible also with Devanagari {#...Page...#}  (doesn't occur in pwg)
  # So, there is no adjustment logic here.
  # add the ans1 lines to ans
  ans = ans + ans1
 fls.close()
 nls = nls + sublsObj.nls
 print(nls,"lines written to",filels)

 return ans

def line_len_stats(inlines):
 # line-length stats
 breaks=(50,60,70,80,90,100,110,120,130,140,150,200,300,400,500,999999)
 dbg=False
 c = {}
 for b in breaks:
  c[b]=0
 for idx,line in enumerate(inlines):
  l = len(line)
  if dbg:
   if l >= 80:
    print("line#%d has length %s" %(idx+1,l))
    print(line.encode('utf-8'))
  for b in breaks:
   if l <=b:
    c[b] = c[b] + 1
    break
 for b in breaks:
  print("line length < %s = %s" %(b,c[b]))

def line_len_adj_helper(line):
 mc = 70
 l = len(line)
 if l <= mc:
  return[line]
 # otherwise split the line into roughly mc-sized parts
 words = re.split(r'( +)',line)
 ans = []
 idx0 = 0
 idx1 = 0
 for w in words:
  idx1 = idx1 + len(w)
  if (idx1-idx0) > mc:
   ans.append(line[idx0:idx1])
   idx0 = idx1
 # last part
 r = line[idx0:] 
 lr = len(r)
 if lr <= 15:
  lastline =ans.pop()  # remove last line
  lastline = lastline + r
  ans.append(lastline) 
 else:
  ans.append(r)
 if False and (len(ans)!=1): # debug
  print(line.encode('utf-8'))
  print()
  for a in ans:
   print(a.encode('utf-8'))
  print("debug exit")
  exit(1)
 return ans

def line_len_adj(lines):
 """
 """
 ans = []
 for idx,line in enumerate(lines):
  ans1 = line_len_adj_helper(line)
  ans = ans + ans1
  if (idx % 10000) == 0:
   print(idx)
 return ans

class Change(object):
 def __init__(self,case):
  self.case = case
  self.changes = []  # (linenum,old,new)

def unused_close_bold(lines):
 changes = []
 iline = 0
 nlines = len(lines)
 case = 0
 while(iline < nlines):
  line = lines[iline]
  if not re.search(r'{@[^@]*$',line):
   iline = iline + 1
   continue
  # line ends with unclosed bold markup. close it
  case = case + 1
  changerec = Change(case)
  changes.append(changerec)
  iline0 = iline
  newline = line + '@}'
  changerec.changes.append((iline,line,newline))
  i = 1
  while True:
   iline = iline0 + i
   line = lines[iline]
   if line.startswith('[Page'):
    newline = line
    changerec.changes.append((iline,line,newline))
    i = i + 1
    continue
   # line assumed of form NNNNN xxx
   m = re.search(r'^([0-9][0-9][0-9][0-9][0-9]) (.*)$',line)
   num,text = (m.group(1),m.group(2))
   if re.search(r'^([^@]+@})',text):
    newtext = re.sub(r'^([^@]+@})',r'{@\1',text)
   elif re.search('@',text):
    # error condition
    print('change_bold ERROR',iline,line)
    exit(1)
   else:
    newtext = '{@%s@}' % text
   newline = '%s %s' %(num,newtext)
   changerec.changes.append((iline,line,newline))
   iline = iline + 1
   break # while True
 return changes

def close_bold(lines):
 changes = []
 iline = 0
 nlines = len(lines)
 case = 0
 while(iline < nlines):
  line = lines[iline]
  if not re.search(r'{@[^@]*$',line):
   iline = iline + 1
   continue
  # line ends with unclosed bold markup. close it
  case = case + 1
  changerec = Change(case)
  changes.append(changerec)
  iline0 = iline
  newline = line + '@}'
  changerec.changes.append((iline,line,newline))
  i = 1
  while True:
   iline = iline0 + i
   line = lines[iline]
   if line.startswith('[Page'):
    newline = line
    changerec.changes.append((iline,line,newline))
    i = i + 1
    continue
   # line assumed of form NNNNN xxx
   m = re.search(r'^([0-9][0-9][0-9][0-9][0-9]) (.*)$',line)
   num,text = (m.group(1),m.group(2))
   if re.search(r'^([^@]+@})',text):
    # Last record of this case
    newtext = re.sub(r'^([^@]+@})',r'{@\1',text)
    newline = '%s %s' %(num,newtext)
    changerec.changes.append((iline,line,newline))
    #iline = iline + 1   There might be another instance for this line.
    lines[iline] = newline
    break  # while True
   elif re.search('@',text):
    # error condition
    print('change_bold ERROR',iline,line)
    exit(1)
   else:
    # intermediate line of case
    newtext = '{@' + text + '@}'
    newline = '%s %s' %(num,newtext)
    changerec.changes.append((iline,line,newline))
    i = i + 1  # continue While True for this case
 return changes

def close_italic(lines):
 changes = []
 iline = 0
 nlines = len(lines)
 case = 0
 while(iline < nlines):
  line = lines[iline]
  if not re.search(r'{%[^%]*$',line):
   iline = iline + 1
   continue
  # line ends with unclosed bold markup. close it
  case = case + 1
  changerec = Change(case)
  changes.append(changerec)
  iline0 = iline
  newline = line + '%}'
  changerec.changes.append((iline,line,newline))
  i = 1
  while True:
   iline = iline0 + i
   line = lines[iline]
   if line.startswith('[Page'):
    newline = line
    changerec.changes.append((iline,line,newline))
    i = i + 1
    continue
   # line assumed of form NNNNN xxx
   m = re.search(r'^([0-9][0-9][0-9][0-9][0-9]) (.*)$',line)
   num,text = (m.group(1),m.group(2))
   if re.search(r'^([^%]+%})',text):
    # Last record of this case
    newtext = re.sub(r'^([^%]+%})',r'{%\1',text)
    newline = '%s %s' %(num,newtext)
    changerec.changes.append((iline,line,newline))
    #iline = iline + 1   There might be another instance for this line.
    lines[iline] = newline
    break  # while True
   elif re.search('%',text):
    # error condition
    print('change_italic ERROR',iline,line)
    exit(1)
   else:
    # intermediate line of case
    newtext = '{%' + text + '%}'
    newline = '%s %s' %(num,newtext)
    changerec.changes.append((iline,line,newline))
    i = i + 1  # continue While True for this case
 return changes

def make_changes(filein,option):
 # slurp txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  inlines0 = [x.rstrip('\r\n') for x in f]
 nlines0 = len(inlines0)
 print(nlines0,"lines from",filein)
 if option == 'bold':
  changes = close_bold(inlines0)
 elif option == 'italic':
  changes = close_italic(inlines0)
 else:
  print('make_changes ERROR. Unknown option',option)
  exit(1)
 return changes

def write_changes(fileout,changes):
 with codecs.open(fileout,'w','utf-8') as f:
  for changerec in changes:
   outarr = []
   outarr.append('; Case %d'%changerec.case)
   for iline,old,new in changerec.changes:
    linenum = iline+1
    outarr.append('%d old %s'%(linenum,old))
    outarr.append('%d new %s'%(linenum,new))
   for out in outarr:
    f.write(out+'\n')
 print(len(changes),'Change cases written to',fileout)

if __name__=="__main__":
 option = sys.argv[1]
 
 filein = sys.argv[2] # X.txt
 fileout = sys.argv[3] #Xadj.txt
 changes = make_changes(filein,option)
 write_changes(fileout,changes)
