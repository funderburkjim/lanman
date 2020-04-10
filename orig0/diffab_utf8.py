"""diffab_utf8.py
   03-22-2020
   07-05-2017
   ejf
   Simple Python program to analyze an 'AB' file from Malten/
  Usage:
  python diffab_utf8.py <file1> <file2> fileout [mdiff]
  mdiff is optional maximum number of differences to print.
    Default value is 1000000

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

if __name__ == "__main__":
 filein1 = sys.argv[1]
 fileout = sys.argv[2]
 try:
  mdiff = int(sys.argv[3])
 except:
  mdiff = 1000000
 (header,recs1,recs2) = parse_input(filein1)
 #with codecs.open(filein2,"r","utf8") as f:
 # recs2 = [x.rstrip('\r\n') for x in f]
 # check for same number of lines
 nrecs1 = len(recs1)
 nrecs2 = len(recs2)
 if nrecs1 != nrecs2:
  print("ERROR: different number of lines in groups A,B")
  print(nrecs1,"lines in A")
  print(nrecs2,"lines in B")
  exit(1)
 #print "Both files have",nrecs1,"lines"
 ndiff = 0
 f = codecs.open(fileout,"w","utf8")
 for i,rec1 in enumerate(recs1):
  rec2 = recs2[i]
  (lineid1,group1,text1) = rec1
  (lineid2,group2,text2) = rec2
  if lineid1 != lineid2:
   print("lineid error",lineid1,lineid2)
   exit(1)
  if text1 == text2:
   code = 'EQ '
  else:
   code = 'NE '
  outarr = []
  out1 = '   ' +lineid1 + group1 + text1
  out2 = code +lineid2 + group2 + text2
  outarr.append(out1)
  outarr.append(out2)
   
  if text1 != text2:
   ndiff = ndiff + 1
   #outarr = []
   #outarr.append('difference # %s at line %s' % (ndiff,i+1))
   #outarr.append('%s: %s' % (filein1,rec1))
   #outarr.append('%s: %s' % (filein2,rec2))
   iposfirstdiff = find_first_difference(text1,text2)
   #s = (' '*len(filein1)) + '  ' + (' '*iposfirstdiff ) + '*'
   s = (' '*(len(code)+len(lineid1)+ len(group1))) + (' '*iposfirstdiff ) + '*'
   outarr.append(s)
   outarr.append('')
  for out in outarr:
   f.write(out+'\n')
  if mdiff<=ndiff:
   print("breaking after",mdiff,"differences")
   break
 f.close()
 # post loop
 if ndiff == 0:
  print("Files are the same")
 else:
  print("Files are different. # ndifferences =",ndiff)

