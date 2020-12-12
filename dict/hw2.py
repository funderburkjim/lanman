"""hw2.py  ejf 2014-03-24
 Read  benhw1.txt, whose lines were created with:
 out = "%s:%s:%s,%s" %(page,hw,l1,l2)

 convert key1 hw to slp1, using transcoder
 

"""
import re
import transcoder
import sys,codecs
transcoder.transcoder_set_dir("");
filename=sys.argv[1] 
fileout =sys.argv[2] 
f = codecs.open(filename,encoding='utf-8',mode='r')
fout = codecs.open(fileout,'w','utf-8')
n = 0
nout = 0 # number of headword lines written to output
asdict = {}
for line in f:
 n = n+1
 line = line.strip() # remove starting or ending whitespace
 (pagecol,hw0,line12) = re.split(':',line)
 hw = hw0
 lnums = re.findall("[a-z][0-9]+",hw)
 for letnum in lnums:
  if letnum not in asdict:
   asdict[letnum]=0
  v = asdict[letnum]+1
  asdict[letnum]=v

 #if (hw == 'titau7'):
 # hwslp = 'titau'
 #elif (hw == 'prau1ga'):
 # hwslp = 'prauga'
 #else:
 if True:
  if re.search(r'MM',hw):   # no instances in benhw1.txt
   hw1 = re.sub(r'MM','M',hw)
   out = "Change MM to M: %s => %s" %(hw,hw1)
   print out.encode('utf-8')
   hw1=hw
  hwslp = transcoder.transcoder_processString(hw,'hk','slp1')
 out = "%s:%s:%s" %(pagecol,hwslp,line12)
 fout.write("%s\n" % out);
 nout = nout + 1
 # check validity of hwslp
 if re.search("[^a-zA-Z'| ]",hwslp):
  hwslp0 = hwslp
  hwslp = re.sub(r'[0-9]','',hwslp)
  out = "slp problem: %s => slp='%s' changed to %s" % (line,hwslp0,hwslp)
  print out.encode('utf-8')
# for debugging
f.close()
fout.close()
print "file %s has %s lines" % (filename,n)
print "%s headwords written to file %s" % (nout,fileout)
for k,v in asdict.iteritems():
 print "code %s occurs %s times" % (k,v)

