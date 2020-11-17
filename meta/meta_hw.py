# coding=utf-8
""" 
	2020-11-14. Modified for lan. ejf
"""
import sys, re, codecs

def meta_headword_addition(filein,filein1,fileout):
 # slurp txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='U') as f:
    inlines = [x.rstrip('\r\n') for x in f]
 # open output xml file, and write header
 fout = codecs.open(fileout,'w','utf-8')
  
 lines = []
 # read headword lines, and generate output
 f = open(filein1,'r')
 n = 0 # count of lines read
 lnum = 0 # generate record number for xml records constructed
 coveredtill = 0 
 for line in f:
  n = n+1
  if n > 1000000:
   print("debug stopping")
   break
  line = line.strip() # remove starting or ending whitespace
  try:
   #(pagecol,hwslp,linenum12,L) = re.split('[:]',line)
   (pagecol,hwslp,linenum12,hom,key2) = re.split('[:]',line)  
   L = n
  except:
   print("Problem at line %s = %s" %(n,line))
   exit(1)
  (linenum1,linenum2) = re.split(',',linenum12)
  n1 = int(linenum1) - 1
  n2 = int(linenum2) - 1
  datalines = inlines[n1:n2+1]
  if not n1 == coveredtill:
   for line in inlines[coveredtill:n1]:
    #preceding = '\n'.join(inlines[coveredtill:n1])
    #print(preceding)
    fout.write(line + '\n')
  coveredtill = n2+1
  # construct output
  lnum = lnum + 1
  assert lnum == int(L),"L-number mismatch" # for stc
  key1 = hwslp
  head = "<L>%s<pc>%s<k1>%s<k2>%s" % (lnum,pagecol,key1,key2)
  if hom != '':
   head = "%s<h>%s" %(head,hom)
  newlines = [head]+datalines+['<LEND>']
  for newline in newlines:
   fout.write(newline + '\n')
 # write ending lines
 for line in inlines[coveredtill:]:
  line = line.rstrip('\r\n')
  fout.write(line+'\n')
 fout.close()
 
if __name__=="__main__":
 filein = sys.argv[1]   # previous digitization version
 filein1 = sys.argv[2]  # xxxhw2 consistent with previous digitization
 fileout = sys.argv[3]  # output accwithmeta.txt
 meta_headword_addition(filein,filein1,fileout)

