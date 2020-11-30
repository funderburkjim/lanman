""" lanlinks
  Nov 28, 2020  for Lanman notes
"""

import codecs,re,sys
import os

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

def get_lanlinks(lines):
 d = {}
 for line in lines:
  for m in re.finditer(r'<a id="(rpl_.*?)"/>',line):
   x = m.group(1)
   if x not in d:
    d[x] = 0
   d[x] = d[x] + 1
 return d
 
if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]  # 
 lines = init_lines(filein)
 dlinks = get_lanlinks(lines)
 links = sorted(dlinks.keys())

 # print the new lines
 with codecs.open(fileout,"w","utf-8") as f:
  for link in links:
   f.write(link+'\n')
   if dlinks[link] != 1:
    print('link %s occurs %s times' %(link,dlinks[link]))
 print(len(links),"written to",fileout)
