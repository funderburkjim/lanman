"""relabel
 For lanman  reader

"""
import re
import sys,codecs
from roman_int import roman_to_int


class Input(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  self.label = None
  m = re.search(r'^\[Page([0-9]+)',line)
  if m:
   self.type = 'page'
   self.page = int(m.group(1))
   return
  m = re.search(r'^([0-9]+) (.*)$',line)
  if not m: 
   print('Input. Error 1',line)
   exit(1)
  self.oldnum = m.group(1)
  self.text = m.group(2)
  m = re.search(r'<section>(.*?)</section>$',self.text)
  if m:
   self.type = 'section'
   romans = m.group(1)
   roman = re.sub(r'[.].*$','',romans)
   self.sectionnum = roman_to_int(roman) 
  else:
   self.type = 'text'

def read_input(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Input(x) for x in f]
 return recs

def relabel(recs):
 ans = []
 for irec,rec in enumerate(recs):
  if (rec.type != 'page') and (irec == 0):
   print('relabel error 1',rec.type,'\n',rec.line)
   exit(1)
  if rec.type == 'page':
   if False: # True: # debug
    if irec != 0:
     print('relabel chk. page %03d had %02d lines'%(ppp,pageline))
   ppp = rec.page
   pageline = 0
   continue
  if rec.type == 'section':
   rec.label = '%03d%02ds' %(ppp,rec.sectionnum)
  else:
   pageline = pageline + 1
   rec.label = '%03d%02d' %(ppp,pageline)
 print('relabel chk. page %03d had %02d lines'%(ppp,pageline))

def write(recs,fileout):
 with codecs.open(fileout,'w','utf-8') as f:
  nout = 0
  for rec in recs:
   if rec.label != None:
    nout = nout + 1
    out = '%s %s' %(rec.label,rec.text)
    f.write(out + '\n')
 print(nout,'records written to',fileout)

def extra_sections_helper(rec):
 data = {
  '03212': {'label':'03209s','text':'<section>IX.</section>'},
  '03809': {'label':'03815s','text':'<section>XV.</section>'},
  '03822': {'label':'03814as','text':'<section>XIV., continued</section>'},
  '03908': {'label':'03916s','text':'<section>XVI.</section>'},
  '03919': {'label':'03914bs','text':'<section>XIV., concluded</section>'},
 }
 if rec.label not in data:
  return None
 # synthesize an Input record
 rec1 = Input('00000 <section>X.</section>')
 # modify two attributes of rec1
 d = data[rec.label]
 rec1.label = d['label']
 rec1.text  = d['text']
 return rec1

def extra_sections(recs):
 recs1 = []
 n = 0
 for irec,rec in enumerate(recs):
  newrec = extra_sections_helper(rec)
  if newrec != None:
   recs1.append(newrec)
   n = n + 1
  recs1.append(rec)
 print('extra_sections inserts',n,'sections')
 return recs1
if __name__ == "__main__":
 filein = sys.argv[1] # reader0
 fileout = sys.argv[2] # reader1 
 recs = read_input(filein)
 print(len(recs))
 relabel(recs) # generate label attribute
 recs1 = extra_sections(recs)  # insert a few 'extra' sections. See readme
 write(recs1,fileout)
 exit(0)
 print("file %s has %s lines" % (filename,n))
 print("%s headwords written to file %s" % (nout,fileout))
 print("%s headwords contained a colon" % (nb,))
