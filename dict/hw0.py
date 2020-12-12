"""hw0.py  ejf  2014-03-24
 For lanman
 Output all major headwords, along with the page on which the headword appear.
 Also, output the line numbers in inm.txt that pertain to the headword.
 - Page numbers are like [PagePPP-C] 
   PPP is a 3-digit page number
   C is a 1-digit column number (a or b)
 The output is written as 
   page:headword:line1,line2
"""
import re
import sys,codecs
filename=sys.argv[1] # 
fileout =sys.argv[2] #  
f = codecs.open(filename,encoding='utf-8',mode='r')
fout = codecs.open(fileout,'w','utf-8')

n = 0
nb = 0 # number of left brackets
nout = 0 # number of headword lines written to output
rePage = re.compile(r"\[Page(.*?)]")
import headword
reHeadword0 = headword.reHeadword
reHeadword = re.compile(reHeadword0)
l0=0 # first line number for a headword
nhw=0 # same as n, but stops when the 'end' string is found
#first line of file, not processed (NOTE: IS PROCESSED FOR VEI)
firststring=r'[Page111-a+ 38]'
firstfound=False
page = "111-a"
endstring=r'[Page1128]'  #not really needed. file is read to end
endfound=False
isFirst = False
# collect the output lines into an array.
# Adjust this array (null operation for PD!), 
# and then output the adjusted array
outlines = []
for line in f:
 n = n+1
 line = line.rstrip()
 if (line.find(endstring) >= 0): 
  print("found endstring at n = %s" % n)
  endfound=True
 nhw = nhw + 1
 if (line.find(firststring) >= 0) and (not firstfound):
  firstfound=True
  # If  True, DO process this line (to get line number)
  isFirst = False
  print("found firststring")
  continue
 # the placement of m=.. before if(not firstfound) is important detail
 m = reHeadword.search(line)
 #print "chk0: %s" %line
 #exit(1)
 #if m:
 # print "chk1: %s" %line

 if (not firstfound):
  out = "skip line %s: %s" %(n,line)
  print(out.encode('utf-8'))
  continue
 if m and (not isFirst):
  # found next headword
  if (l0 != 0):
   # output the prior word
   l1 = l0
   l2 = nhw - 1
   out = "%s:%s:%s,%s" %(page0,hw0,l1,l2)
   #print('chk1',out)
   outlines.append(out)
   #fout.write("%s\n" %(out,))
   nout = nout + 1
  # the base headword. This program outputs this
  hw0 = m.group(1) 
  # update page0,  l0 
  page0 = page
  l0=nhw
  if re.search(":",hw0):
   out = "Removing from ':' to end at line %s: %s" % (n,hw0)
   print(out.encode('utf-8'))
   nb = nb + 1
   hw0 = re.sub(':.*$','',hw0)
 # step 3, search for page
 isFirst = False # required for first word handling
 pages = rePage.findall(line)
 if len(pages) > 0:
  pagelast = pages[-1]
  #m = re.match(r'^([0-9]+a?)[.]([1-3])',pagelast)
  m = re.match(r'^([0-9]+)-([ab])',pagelast) # for ben
  if m:
   pagenum = m.group(1)
   col = m.group(2)
   if (len(pagenum)!=3):
    out = "ERROR: Unexpected page number: %s" % m.group(1)
    print( out.encode('utf-8'))
    exit(1)
   page = "%s-%s" % (pagenum,col)
 if endfound:
  break
# we must now prepare the last headword
l1 = l0
l2 = nhw
out = "%s:%s:%s,%s" %(page0,hw0,l1,l2)
outlines.append(out)
nout = nout + 1
#---------Adjust outlines.  This logic is skipped for ben

# remove non-dictionary end-of-volume lines
outlines1 = []
for i in range(0,nout):
 j = i + 1
 if False:  #Skip this logic
  if (3844 <= j) and (j <= 3906):
   continue
  if (1875 <= j) and (j <= 1884):
   continue
 outlines1.append(outlines[i])

#---------Output adjusted lines
nout = 0
for out in outlines1:
 fout.write("%s\n" %(out,))
 nout = nout + 1
f.close();
fout.close();
print("file %s has %s lines" % (filename,n))
print("%s headwords written to file %s" % (nout,fileout))
print("%s headwords contained a colon" % (nb,))
