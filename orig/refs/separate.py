#-*- coding:utf-8 -*-
"""orig/refs/separate.py
   10-17-2020

"""
from __future__ import print_function
import codecs,sys,re

def find_first_difference(rec1,rec2):
 n1 = len(rec1)
 n2 = len(rec2)
 n = max(n1,n2)
 for i in range(0,n):
  if (i < n1) and (i < n2):
   if (rec1[i] != rec2[i]):
    return i
   else:
    # continue in loop
    continue
  else:
   return i

def parse_input(filein1):
 with codecs.open(filein1,"r","utf8") as f:
  recs1=[]
  recs2=[]
  for idx,x in enumerate(f):
   #recs1 = [x.rstrip('\r\n') for x in f]
   x = x.rstrip('\r\n')
   if idx == 0:
    header = x
    continue
   m = re.search(r'^([0-9]{5}[+])([AB])(<>.*)$',x)
   if not m:
    print("unexpected format at line,",idx+1)
    print(x.encode('utf-8'))
    exit(1)
   lineid = m.group(1)
   group = m.group(2) #A,B
   text = m.group(3)
   if group == 'A':
    recs1.append((lineid,group,text))
   else:
    recs2.append((lineid,group,text))
 print("idx=",idx)
 print(len(recs1),len(recs2))
 return (header,recs1,recs2)

class Data(object):
 def __init__(self,page1,page2,name):
  self.page1 = page1
  self.page2 = page2
  self.name = name
  self.lines = []

def init_datarecs():
 recs = [
  Data(111,288,'vocabulary'),
  Data(289,292,'explanations'),
  Data(293,294,'abbreviations'),
  Data(297,405,'notes')
 ]
 return recs
def separate(lines,datarecs):
 """ return sublists of lines based on pages """
 page = None
 prevpage = 106
 for idx,line in enumerate(lines):
  # page breaks are on separate lines.
  # format is [Pagexxx+ y] or [Pagexxx-c+ y]  where c is column 'a' or 'b'
  # and y is number of lines in the Page or column
  # assume first line of file is page break [Page107+ 1]
  m = re.search(r'^\[Page([0-9][0-9][0-9])',line)
  if m:
   page = int(m.group(1))
   # many pages have two columns
   #if page != (prevpage + 1):
   # print('Error at page',page,'prevpage=',prevpage)
   # print('idx=',idx,'line=',line)
   # exit(1)
   if page == prevpage:  
    # assume this is 'b' column 
    pass
   else:
    # assume we're either on an 'a' column, or a page break with no columns
    prevpage = prevpage + 1
  found = False
  for rec in datarecs:
   if (rec.page1 <= page) and (page <= rec.page2):
    rec.lines.append(line)
    found = True
    break
  if not found:
   print('skipping page %s at line %s'%(page,line))
 return 

def write_section(datarec):
 fileout = '%s.txt' %(datarec.name)
 with codecs.open(fileout,"w","utf-8") as f:
  for line in datarec.lines:
   f.write(line+'\n')
 print(len(datarec.lines),'lines written to',fileout)

if __name__ == "__main__":
 filein = sys.argv[1]
 #fileout1 = sys.argv[2]
 #fileout2 = sys.argv[3]
 with codecs.open(filein,"r","utf8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 datarecs = init_datarecs()

 # mutate datarecs (last field)
 separate(lines,datarecs)  
 # write each datarecs to a separate file
 for rec in datarecs:
  write_section(rec)
