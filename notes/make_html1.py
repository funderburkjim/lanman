""" make_html1.py
  Nov 24, 2020  for Lanman notes
"""

import codecs,re,sys
import os

class Abbrev(object):
 d = {}
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
  Abbrev.d[self.abbrv] = self

def init_abbrevs(filein):
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

def init_lines(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines0 = [x.rstrip('\r\n') for x in f]
 # remove initial 5-digit code and space  These not in notes1.txt
 return lines0
 lines = []
 for x in lines0:
  m = re.search(r'^([0-9]+) (.*)$',x)
  if not m:
   # page break line
   lines.append(x)
  else:
   lines.append(m.group(2))
 print(len(lines),"lines read from",filein)
 return lines

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

def init_selections(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Selection(x) for x in f if not x.startswith(';')]
 return recs

def adjust_lines(lines):
 removals = [
 ]
 replaces = [
  ('{%','<i>'), ('%}','</i>'), # italic
  ('{@','<b>'), ('@}','</b>'), # bold

 ]
 subs = [
 ]

 nchg = 0
 for iline,line in enumerate(lines):
  oldline = line
  for regex in removals:
   line = re.sub(regex,'',line)
  for old,new in replaces:
   line = line.replace(old,new)
  for old,new in subs:
   line = re.sub(old,new,line)
  if line != oldline:
   lines[iline] = line
   nchg = nchg + 1
 print('adjust_lines',nchg,'lines changed')

def abbrev_lines(lines):
 """ adjust <ab>X</ab> to <abbr title="Y">X</abbr>
  where Y  = Abbrev.d[X].meaning
 """
 d = Abbrev.d
 def f(m):
  x = m.group(1)
  if x not in d:
   print('abbrev_lines warning. Abbreviation not found',x)
   return x
  y = Abbrev.d[x].meaning
  #ans = '<abbr title="%s" >%s</abbr>' %(y,x)  Default styling is poor
  ans = '<span title="%s" class="abbr">%s</span>' %(y,x)
  return ans
 nchg = 0
 for iline,line in enumerate(lines):
  oldline = line
  newline = re.sub(r'<ab>(.*?)</ab>',f,line)
  if newline != oldline:
   lines[iline] = newline
   nchg = nchg + 1
 print('abbrev_lines',nchg,'lines changed')

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
 anchor = '<a id="rp_%03d"/>' %rpage1
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
 icase = 1
 if not m:
  m = re.search(r'^<p>LINE[S ]+{@([0-9]+)',line) # 4 cases
  icase = 2
  if not m:
   return line
 ipage = int(page)
 ilinenum = int(m.group(1))
 # rpl = reader page line.  reader at label pppll should link here
 anchor = '<a id="rpl_%03d%02d"/>' % (ipage,ilinenum)
 # put tooltip for <p>
 tooltip = "Re page %d, line %s of Reader" %(ipage,ilinenum)
 if icase == 1:
  #line1 = re.sub(r'<p>','<p title="%s">' % tooltip,line)
  line1 = re.sub(r'(<p>{@)([0-9]+)',r'\1<span title="%s">\2</span>' %tooltip,line)
 else:
  line1 = re.sub(r'(<p>LINE[S ]+{@)([0-9]+)',r'\1<span title="%s">\2</span>' %tooltip,line)
 line1 = '%s %s' %(anchor,line1)
 return line1

def make_wg_links(line):
 def f(m):
  section = m.group(1)
  text = m.group(2)
  url = 'https://funderburkjim.github.io/WhitneyGrammar/step1/pages2c.html'
#section_248
  href = "%s#section_%s" % (url,section)
  tooltip = "Whitney Grammar, section %s" %section
  target = "_wglink"
  html = '<a href="%s" title="%s" target=%s">%s</a>' %(href,tooltip,target,text)
  return html
 newline = re.sub(r'<ls n="wg,(.*?)">(.*?)</ls>',f,line)
 return newline

def make_lan_links(line):
 def f(m):
  parts = m.group(1).split(',')
  page = parts[0]
  lnum = parts[1]
  text = m.group(2)
  url = '../reader/index.html'
  ipage = int(page)
  ilnum = int(lnum)
  href = "%s#rpl_%03d%02d" % (url,ipage,ilnum)
  tooltip = "Lanman Reader, Page %s, line %s" %(page,lnum)
  target = "_lanlink"
  html = '<a href="%s" title="%s" target=%s">%s</a>' %(href,tooltip,target,text)
  return html
 newline = re.sub(r'<ls n="lan,(.*?)">(.*?)</ls>',f,line)
 return newline

def init_markup(lines):
 achapter = 0
 rpage = None  # <head>NOTES TO PAGE {@X.@}</heaqd>
 page = None
 for iline,line in enumerate(lines):
  m = re.search(r'^\[Page(.*?)[+] ',line)
  if m:
   page = m.group(1)
   scanurl = "https://sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=lan&page=%s" %page
   target ="_lanscan"
   tooltip = "Link to Lanman Reader Scans"
   scanlink = '<a href="%s" target="%s" title="%s">%s</a>' %(scanurl,target,tooltip,page)
   newline = '<a id="page_%s"></a>Page %s' %(page,scanlink)
   #newline = '<a id="page_%s"></a>Page %s' %(page,page)
   lines[iline] = "<br/>%s<br/>" % newline
   continue
  rpage1,newline = head_pagenote(line)
  if newline != line:
   lines[iline] = newline
   rpage = rpage1
   continue
  newline = head_other(line)
  if newline != line:
   lines[iline] = newline
   continue
  newline = link_rpl(line,rpage)
  if newline != line:
   lines[iline] = newline
   # continue with other markup of paragraph
   line = lines[iline]
  newline = make_wg_links(line)
  if newline != line:
   lines[iline] = newline
   # continue with other markup of paragraph
   line = lines[iline]
  newline = make_lan_links(line)
  if newline != line:
   lines[iline] = newline
   # continue with other markup of paragraph
   line = lines[iline]
    
  # done with this line. no change
  
  continue

def init_markup_selections(lines,selections):
 
 for iline,line in enumerate(lines):
  if 'SELECTION' not in line:
   continue
  selections1 = [x for x in selections if x.selstring in line]
  if len(selections1) == 0:
   continue
  if len(selections1) > 1:
   #print('chk',[x.line for x in selections1])
   selections2 = [x for x in selections1 if ',' in x.selstring]
   assert len(selections2) == 1
   selection = selections2[0]
  else: # only 1
   selection = selections1[0]
  selection.used = selection.used + 1
  anchor = '<a id="selection_%s"/>' % selection.code
  newline = '%s %s' % (anchor,line)
  # also, adjust formating of the select string, where needed
  s = selection.selstring
  newline = re.sub(r' %s'% s,r' <b style="font-size:larger">%s</b>' % s,newline)
  lines[iline] = newline
 # check usage
 n = 0
 for selection in selections:
  if selection.used != 1:
   n = n + 1
   print('WARNING: Selection used',selection.used,'times',selection.line)
 if n > 0:
  print('WARNING:',n,'problems in init_markup_selections')
 else:
  print('init_markup_selections OK')

def init_nav(chapters):
 a = [] 
 a.append('<div id="navbar">')
 a.append('<ul>')
 for linkid,name in chapters:
  x = '<a href="#%s" class="navitem">%s</a>' %(linkid,name)
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
<title>Lanman Reader Notes</title>
<style>

table, th, td {
  border: 1px solid black;
}
/* When there is a navbar
#navbar { 
 position:fixed;
 top: 40px;
 left: 5px;
 width: 300px;
 height: 90%;
 overflow: auto;
}
#text {
position:absolute;
 top: 40px;
 left: 320px;
 right: 5px;
 height: 90%;
 overflow: auto;
}
*/
/* when there is no navbar 
*/
#text {
position:absolute;
 top: 40px;
 left: 20px;
 right: 10px;
 height: 90%;
 overflow: auto;
}
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

.meter {font-weight:bold;}

.abbr {
 /*border-bottom: 1px dotted #000; */
/*
 background-color:rgb(240, 240, 240);
 text-decoration: none;
*/
/* ref; https://stackoverflow.com/questions/10131713/make-bottom-border-closer-to-text */
    text-decoration: none;
    position: relative;
    background-repeat: repeat-x;
    background-image: url(data:image/gif;base64,R0lGODlhAQABAIAAAAAAAAAAACH5BAAAAAAALAAAAAABAAEAAAICTAEAOw==);
    background-position: left 15px bottom 5px;

}
.abbr:hover {
 cursor:pointer;
}
</style>
</head>
<body>

"""

def init_html(navhtmlarr,lines):
 a = []
 a = html_header.splitlines()
 #a.append("<H3 class='header'>Whitney Sanskrit Grammar</H3>")
 a = a + navhtmlarr
 a.append('<div id="text">')
 a = a + lines
 a.append('</div>')
 a.append('</body>')
 a.append('</html>')
 return a

if __name__ == "__main__":
 filein = sys.argv[1]
 fileSelections = sys.argv[2]
 fileabbr = sys.argv[3] # for abbreviation tooltips
 fileout = sys.argv[4]  # 
 lines = init_lines(filein)
 selections = init_selections(fileSelections)
 init_abbrevs(fileabbr)  # we use Abbrev.d
 init_markup(lines)  # modify lines
 init_markup_selections(lines,selections)
 navhtmlarr = [] # init_nav(chapters)
 adjust_lines(lines)
 abbrev_lines(lines)
 htmlarr = init_html(navhtmlarr,lines)

 # print the new lines
 with codecs.open(fileout,"w","utf-8") as f:
  for out in htmlarr:
   f.write(out+'\n')
 print(len(htmlarr),"lines written to",fileout)
