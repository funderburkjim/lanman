# coding=utf-8
""" adjtxt1.py
  Modifies ben
  See readme.org for explanation.
"""
import sys, re,codecs

def make_txtfun(filein,fileout):
 # slurp txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  inlines = [x.rstrip('\r\n') for x in f]
 # remove {%} lines and {@} lines
 outlines = []
 ndel = 0
 linedels = ['{%}', '{@}']
 for idx,line in enumerate(inlines):
  if line in linedels:
   ndel = ndel + 1
  else:
   outlines.append(line)

 nlines = len(inlines)
 print nlines,"lines from",filein
 print ndel,"lines deleted"
 # write output
 fout = codecs.open(fileout,'w','utf-8')
 for line in outlines:
  fout.write(line + '\n')
 fout.close()
 print len(outlines),"written to",fileout
 return
 # number of chars per page
 pcdata=[]
 curpage=None
 for i,line in enumerate(inlines):
  if line.startswith('[Page'):
   if curpage != None:
    pcdata.append((curpage,charspage))
   curpage = line # the [Page..]
   charspage = 0
  elif curpage != None:
   charspage = charspage + len(line)
 # last page
 pcdata.append((curpage,charspage))
 pcdatafile='adjtxt_pcdata.txt'
 with codecs.open(pcdatafile,'w') as f:
  for (curpage,charspage) in pcdata:
   out = curpage[1:-1]  # skip [,]
   out = out + " " + ("%5d"%charspage)
   f.write(out + '\n')
  print "check output in pcdatafile=",pcdatafile
 # simple statistics
 pcdata1 = sorted(pcdata,key = lambda x : x[1]) # charspage
 print "charspage stats, %s pages" % len(pcdata)
 print "min = ",pcdata1[0][1]
 print "max = ",pcdata1[-1][1]
 m = len(pcdata1) / 2
 print "med = ",pcdata1[m][1]
 #line_len_stats(inlines)
if __name__=="__main__":
 filein = sys.argv[1] # X.txt
 fileout = sys.argv[2] #Xadj.txt
 make_txtfun(filein,fileout)
