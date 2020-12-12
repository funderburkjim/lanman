""" make_html1.py
  Nov 27, 2020  for Lanman reader
"""

import codecs,re,sys
import os
import transcoder
transcoder.transcoder_set_dir("transcoder");

sections = {}
class ReaderLine(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  m = re.search(r'^([^ ]+) +(.*)$',line)
  if not m:
   # unexpected
   print('ReaderLine Error 1',line)
   exit(1)
  self.label0 = m.group(1)
  self.text = m.group(2)
  if self.label0.endswith('s'):
   self.type = 'section'
   self.anchorid = 'rs_%s'%self.label0  # reader section
  else:
   self.type = 'text'
   self.anchorid = 'rpl_%s'%self.label0  # reader page line
  self.html = None
  self.pageBreak_html = ''
  self.note_links = []
  self.dict_links = []
  self.note_section_links = []

 def get_anchor_html(self):
  html = '<a id="%s"/>' % self.anchorid
  return html

 def line_label_html(self):
  #temp = '&nbsp;&nbsp'
  temp = ''
  if self.type == 'section':
   return temp
  m = re.search(r'^[0-9][0-9][0-9]([0-9][0-9])',self.label0)
  iline = int(m.group(1))
  if (iline % 5) != 0:
   return temp
  if iline < 10:
   #return #'&nbsp;%s' % iline
   return '%s' % iline
  else:
   return '%s' % iline

 def page_break_html(self):
  m = re.search(r'^([0-9][0-9][0-9])01',self.label0)
  if not m:
   return False
  page = m.group(1)
  if page == '001':
   if not self.label0.endswith('s'):
    return False
  a = r'rp_%s'%page
  anchor = r'<a id="%s"/>' % a
  ipage = int(page)
  html = "%s <H1>Page %d</H1>" %(anchor,ipage)
  self.pageBreak_html = html
  return True

def init_lines(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines0 = [x for x in f]
 # remove initial 5-digit code and space
 recs = [ReaderLine(x) for x in lines0]
 print(len(recs),"lines read from",filein)
 return recs

def adjust_recs(recs):
 removals = [
  r'</lg>', r'</l>', r'</section>',
  r'<lg>', r'<l>', r'<section>',

 ]
 replaces = [
  #('{<lg','<i>'), ('%}','</i>'), # italic
  #('{@','<b>'), ('@}','</b>'), # bold
 ]
 subs = [
  #('<(.*?)>',r'[TAG_\1]')
 ]

 nchg = 0
 for irec,rec in enumerate(recs):
  line = rec.text
  oldline = line
  for regex in removals:
   line = re.sub(regex,'',line)
  for old,new in replaces:
   line = line.replace(old,new)
  for old,new in subs:
   line = re.sub(old,new,line)
  if line != oldline:
   rec.text = line
   nchg = nchg + 1
   #print(rec.text)
   #print(recs[irec].text)
   #print()
  #if irec > 5:
  # exit(1)
 print('adjust_recs',nchg,'recs with text changed')

def head_selection(line):
 ## 5 such major sections
 starts = [
  '<head>SELECTION I.</head>',
  '<head>SELECTIONS II.-XXI.</head>',
  '<head>SELECTIONS XXII.-XXVII.</head>',
  '<head>SELECTION XXVIII.</head>',
  '<head>SELECTIONS XXXI.-LXXV.</head>',
 ]
 for start in starts:
  if line.startswith('start'):
   line1 = re.sub('head','H1')
   return line1
 return line

def head_pagenote(line):
 ## 
 m = re.search(r'<head>NOTES TO PAGE {@(.*?)[.]@}</head>',line)
 if not m:
  return None,line
 rpage = m.group(1)
 line1 = re.sub('head','H2',line)
 #line1 = line1.replace('{@','')
 #line1 = line1.replace('@}','')
 # add page_xxx anchor
 rpage1 = int(rpage)
 anchor = '<a id="rp_%03d"/></a>' %rpage1
 line1 = '%s %s' %(anchor,line1)
 return rpage,line1

def head_other(line):
 ## 
 if not line.startswith('<head>'):
  return line
 line1 = re.sub('head','H2',line)
 return line1

def link_rpl(line,page):
 m = re.search(r'^<p>{@([0-9]+)',line)
 if not m:
  return line
 ipage = int(page)
 ilinenum = int(m.group(1))
 # rpl = reader page line.  reader at label pppll should link here
 anchor = '<a id="rpl_%03d%02d"/></a>' % (ipage,ilinenum)
 # put tooltip for <p>
 tooltip = "Re page %d, line %s of Reader" %(ipage,ilinenum)
 line1 = re.sub(r'<p>','<p title="%s">' % tooltip,line)
 line1 = '%s %s' %(anchor,line1)
 return line1

def section_name(text):
 # Later get better section names from SELECTION in notes
 return text

def init_markup(recs):
 achapter = 0
 rpage = None  # <head>NOTES TO PAGE {@X.@}</heaqd>
 page = None
 for irec,rec in enumerate(recs):
  linelabel = rec.line_label_html()
  anchor = rec.get_anchor_html()
  if rec.type == 'section':
   section = section_name(rec.text)
   rec.html = '%s %s<h2>SECTION %s</H2>' % (anchor,linelabel,section)
  else:
   #rec.html = '%s %s %s<br/>' % (anchor,linelabel,rec.text)
   rec.html = '%s %s %s' % (anchor,linelabel,rec.text)
  rec.html = rec.html.replace('<head>','<span class="head">')
  rec.html = rec.html.replace('</head>','</span>')

def init_nav(chapters):
 a = [] 
 a.append('<div id="navbar">')
 a.append('<ul>')
 for c in chapters:
  #anchorid,text,selection,title,code = chapter # see init_chapters
  name = "%s %s" %(c.text,c.title)
  x = '<a href="#%s" class="navitem">%s</a>' %(c.anchorid,name)
  y = '<li>%s</li>' %x
  a.append(y)
 a.append('</ul>')
 a.append('</div>')
 return a

html_header = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Lanman Reader Texts</title>
<style>
.head {
 font-weight: bold;
 font-size: larger;
 text-align: center;
}
table, th, td {
  border: 1px solid black;
}
/* When there is a navbar */
#navbar { 
 position:fixed;
 top: 40px;
 left: 5px;
 width: 300px;
 max-height: 600px;
 overflow: auto;
 border: 1px solid black;
}
#text {
position:absolute;
 top: 40px;
 left: 320px;
 right: 5px;
 /*height: 90%;*/
 max-height: 600px;
 overflow: auto;
 border: 1px solid black;
}

/* when there is no navbar 

#text {
position:absolute;
 top: 40px;
 left: 20px;
 right: 10px;
 height: 90%;
 overflow: auto;
}
*/
.header {
 font-variant:small-caps;
 position:fixed;
 margin-top:0px;
 top:5px;
 left:5px;
 width: 100%;
}
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  font-size: 14px;
  overflow-x: auto;
  line-height: 1.5;
}
li a {
  display: block;
  font-family: sans-serif;
  text-decoration: none;
  color: black;
  width:380px;
}
p {
 max-width:600px;
 text-align:justify;
 margin-right:10px;
}

</style>
</head>
<body>

"""

def init_html(navhtmlarr,recs,tranout):
 a = []
 a = html_header.splitlines()
 #a.append("<H3 class='header'>Whitney's Sanskrit Grammar</H3>")
 a = a + navhtmlarr
 a.append('<div id="text">')
 transcode = transcoder.transcoder_processElements
 tranin = 'slp1'
 tableflag = False
 for rec in recs:
  if rec.page_break_html():
   if tableflag:
    a.append("</table>")
   a.append(rec.pageBreak_html)
   tableflag = True
   a.append("<table>")
  html1 = transcode(rec.html,tranin,tranout,'s')
  note_linkhtml = " ".join(rec.note_links)
  if rec.type == 'section':
   note_sectionhtml = " ".join(rec.note_section_links)
  else:
   note_sectionhtml = ""
  dict_linkhtml = " ".join(rec.dict_links)
  dict_linkhtml1 = transcode(dict_linkhtml,tranin,tranout,'s')
  
  linkhtml = "%s %s %s" %(note_linkhtml,note_sectionhtml,dict_linkhtml1)
  row = "<tr><td>%s</td><td>%s</td></tr>" %(html1,linkhtml)
  a.append(row)
  #a.append(html1)
  #a = a + lines
 a.append("</table>")
 a.append('</div>')
 a.append('</body>')
 a.append('</html>')
 return a

def init_note_links(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines0 = [x.rstrip('\r\n') for x in f]
 links = set(lines0)
 return links

def init_dict_links(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines0 = [x.rstrip('\r\n') for x in f if not x.startswith(';')]
 links = set(lines0)
 return links

def make_note_link(link):
 m = re.search(r'^rpl_([0-9][0-9][0-9])([0-9][0-9])$',link)
 if m:
  url = "../notes/index.html"
  ipage = int(m.group(1))
  ilnum = int(m.group(2))
  tooltip = "Note on Page %d, line %d" %(ipage,ilnum)
  target = "_lannotes"
  href = "%s#%s" %(url,link)
  html = '<a href="%s" title="%s" target="%s">Note</a>' %(href,tooltip,target)
  return html
 return None

def add_note_links(recs,links):
 #print('add_note_links known links=',links)

 for rec in recs:
  m = re.search(r'<a id="(.*?)"/>',rec.html)
  if not m:
   continue
  link = m.group(1)
  if link in links:
   linkhtml = make_note_link(link)
   if linkhtml != None:
    rec.note_links.append(linkhtml)
  #else:
  # print('note link not found',link)

def make_dict_links(hws,source):
 transcode = transcoder.transcoder_processString
 links = []
 #url = "https://www.sanskrit-lexicon.uni-koeln.de/simple/lan"
 #url = "http://localhost/cologne/simple/lan"  # for testing
 if source == "cologne":
  baseurl = "https://www.sanskrit-lexicon.uni-koeln.de/scans"
 elif source == "xampp":
 # for debugging use local display
  baseurl = "http://localhost/cologne/"
 else: 
  print("make_dict_links: Invalid source",source)
  exit(1)
 url = "%s/csl-apidev/sample/list-0.2.php?dict=lan&input=hk&output=deva&key=" % baseurl

 tooltip = "see Lanman Dictionary" 
 target = "_landict"
 for hw in hws:
  # sometimes, slp1 does not work with simple
  hw1 = transcode(hw,'slp1','hk')  
  #href = "%s/%s/deva" %(url,hw1)
  href = "%s%s" %(url,hw1)
  # %E0%A4%B5%E0%A5%80%E0%A4%B0%E0%A4%B8%E0%A5%87%E0%A4%A8%E0%A4%B8%E0%A5%81%E0%A4%A4
  #href = "%s/<s>%s</s>" %(url,hw)
  html = '<a href="%s" title="%s" target="%s"><s>%s</s></a>' %(href,tooltip,target,hw)
  links.append(html)
 return links

def add_dict_links(recs,links,source):
 # x in links is of form rpl_xxxyy_hw
 d = {}
 for x in links:
  m = re.search(r'^(rpl_.*?)_(.*?)$',x)
  rpl = m.group(1)
  hw = m.group(2)
  if rpl not in d:
   d[rpl] = []
  if hw not in d[rpl]:
   d[rpl].append(hw)

 for rec in recs:
  m = re.search(r'<a id="(.*?)"/>',rec.html)
  if not m:
   continue
  link = m.group(1)
  if link in d:
   hws = d[link]
   rec.dict_links = make_dict_links(hws,source)

class Selection(object):
 d = {}
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  parts = line.split(':')
  if len(parts) != 3:
   print('Selection ERROR',line)
   exit(1)
  self.code,self.selstring,self.title = parts
  self.used = 0
  Selection.d[self.selstring] = self
  # matchstring
  s = re.sub(r'SELECTIONS? ','',self.selstring)
  if s.startswith('XIV.,'):
   self.matchstring = s
  elif s == 'II.-XXI.':
   self.matchstring = 'II.'
  elif s == 'XXII.-XXVII.':
   self.matchstring = 'XXII.'
  elif s == 'XXXI.-LXXV.':
   self.matchstring = 'XXXI.'
  elif self.code.endswith(('a','b')):
   self.matchstring = s
  elif self.code == '29':
   self.matchstring = 'XXIX.'
  else:
   self.matchstring = s
  #if 'XIV.' in self.matchstring:
  # print('Selection: sel=',self.selstring,' ; match=',self.matchstring)
  self.section = None

def init_selections(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Selection(x) for x in f if not x.startswith(';')]
 return recs

def get_section_selections(section,selections):
 ans = []
 section1 = re.sub(r'[.][^,].*$','.',section)
 #section1 = section
 for x in selections:
  if section.startswith('XIV.'):
   if section == x.matchstring:
    ans.append(x)
  elif section1 == x.matchstring:
   ans.append(x)
 if False: #True: # len(ans) != 1:
  temp = [x.selstring for x in ans]
  print('section',section,' <-> selection',temp)
 return ans

def make_section_link(selection):
 link = 'selection_%s'%selection.code
 url = "../notes/index.html"
 tooltip = 'Note on %s' %selection.selstring
 target = "_lannotes"
 href = "%s#%s" %(url,link)
 html = '<a href="%s" title="%s" target="%s">Note</a>' %(href,tooltip,target)
 return html

def add_note_section_links(recs,selections):
 for rec in recs:
  if rec.type != 'section':
   continue
  section = rec.text
  matches = get_section_selections(section,selections)
  for selection in matches:
   rec.note_section_links.append(make_section_link(selection))

def add_note_section_links(recs,selections):
 for rec in recs:
  if rec.type != 'section':
   continue
  section = rec.text
  matches = get_section_selections(section,selections)
  for selection in matches:
   rec.note_section_links.append(make_section_link(selection))

def pre_init_chapters(recs,selections):
 ans = []
 for rec in recs:
  if rec.type != 'section':
   continue
  section = rec.text
  matches = get_section_selections(section,selections)
  nmatches = len(matches)
  for i,selection in enumerate(matches):
   #rec.note_section_links.append(make_section_link(selection))
   out = "%s:%s~ %s:%s:%s" %(rec.anchorid,rec.text,selection.code,selection.matchstring,selection.title)
   flag = (i == 0) and (nmatches == 2)
   if flag:
    out = "%s (1)" % out
   print(out)
   ansitem = (rec.anchorid,rec.text,selection.matchstring,selection.title,flag)
   ans.append(ansitem)
 return ans

class Chapter(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  x,y = line.split('~ ')
  self.anchorid,self.text = x.split(':')
  yparts = y.split(':')
  self.code,self.matchstring,self.title = yparts[0],yparts[1],yparts[2]
  if len(yparts) == 4:
   self.major = True
  else:
   self.major = False

def init_chapters(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Chapter(x) for x in f if not x.startswith(';')]
 return recs

if __name__ == "__main__":
 tranout = sys.argv[1]
 filein = sys.argv[2]
 filenotelinks = sys.argv[3]   # links from reader to notes
 filedictlinks = sys.argv[4] # links from reader to dictionary
 fileselections = sys.argv[5] # selections in notes
 fileNavbar = sys.argv[6]
 fileout = sys.argv[7]  # 
 note_links = init_note_links(filenotelinks) # a set
 dict_links = init_dict_links(filedictlinks) # a set
 selections = init_selections(fileselections)

 recs = init_lines(filein)  # records corresponding to each line
 adjust_recs(recs)
 init_markup(recs)  # modify recs
 add_note_links(recs,note_links)
 source = "xampp" 
 source = "cologne"
 add_dict_links(recs,dict_links,source)
 add_note_section_links(recs,selections)
 #chapters = init_chapters(recs,selections)
 chapters = init_chapters(fileNavbar)
 navhtmlarr = init_nav(chapters)
 #exit(1)
 #chapters = []
 #navhtmlarr = [] # init_nav(chapters)
 htmlarr = init_html(navhtmlarr,recs,tranout)

 # print the new lines
 with codecs.open(fileout,"w","utf-8") as f:
  for out in htmlarr:
   f.write(out+'\n')
 print(len(htmlarr),"lines written to",fileout)
