# coding=utf-8
""" inverb_meta.py for lan
"""
import sys, re, codecs

# Function to generate the old line from XXXwithmeta.txt.
# Typical lines would be like this in stcwithmeta.txt
"""
<L>64<pc>2,2<k1>akupya<k2>1a-kupya
{@1a-kupya-@}¦ a. v. contre quoi il n'y a pas a11 s'irriter.
<LEND>

"""

def unused_parseheadline(headline):
 """<L>16850<pc>292-3<k1>visarga<k2>visarga<h>1<e>2"""
 headline = headline.rstrip('\r\n')
 splits = re.split('[<]([^>]*)[>]([^<]*)',headline)
 result = {}
 for i in xrange(len(splits)):
  if i % 3 == 1:
   result[splits[i]] = splits[i+1]
 return result

def parseheadline(headline):
 """<L>16850<pc>292-3<k1>visarga<k2>visarga<h>1<e>2"""
 headline = headline.strip()
 splits = re.split('[<]([^>]*)[>]([^<]*)',headline)
        #print splits
 result = {}
 for i in xrange(len(splits)):
  if i % 3 == 1:
   result[splits[i]] = splits[i+1]
 return result
def unused_construct_first_line_(line,metaline):
 """ Example:
  metaline: <L>2<pc>0001<k1>a<k2>a<h>2
      line: 2. ({@a@})¦. Deutestamm der 1. Person, siehe unter aha4m.
  reconstruct: <P>2. ({@a@}). Deutestamm der 1. Person, siehe unter aha4m.

   KEEP the broken bar and insert initial <HI>
 """
 #line = re.sub(u'¦','',line)
 line = '<P>' + line
 return (line + '\n')   # logic requires \n be part of return
 #  we don't use this more complicated code
 metad = parseheadline(metaline)
 (metahead,rest) = re.split(u'¦',line)
 # trick is to get head
 hparts = []
 hparts.append('<H1>')
 hparts.append('000')
 if 'e' in metad:
  e = metad['e']
 else:
  e = ''
 k1 = metad['k1']
 k2 = metad['k2']
 ## It appears that in the original file, key1 = key2, except for accents
 k1a = re.sub(r"[/^()]","",k2)
 k1a = k1a.replace(r'\\','')
 # and questionmark
 #k1a = k1a.replace(r'(?)','')
 k1a = k1a.replace(r'?','')
 #k1a = k1a.replace(r'(!)','')
 k1a = k1a.replace(r'!','')
 
 """
 if ("'" in k2):
  k1a = re.sub(r"[/\\^]","",k2)
 else:
  k1a = k1
 """
 hparts.append('{%s}' %k1a)
 hparts.append('1')
 hparts.append('{%s}' % k2)
 if 'h' in metad:
  hparts.append(e + '^' + metad['h'])
 else:
  hparts.append(e)
 head = ''.join(hparts)
 return head + u'¦' + rest + '\n'

if __name__=="__main__":
 # print parseheadline("<L>16850<pc>292-3<k1>visarga<k2>visarga<h>1<e>2")
 filein = sys.argv[1] # accwithmeta.txt
 fileout = sys.argv[2]  # acc_invert_meta.txt
 fin = codecs.open(filein,'U','utf-8')
 data = fin.readlines()
 fin.close()
 fout = codecs.open(fileout,'w','utf-8')
 recon_head = ''
 idxmeta = None  # index number of prior meta line
 for idx,line in enumerate(data):
  #print line.encode('utf-8')
  output = ''
  line = line.rstrip('\r\n')
  if line.startswith('<LEND>'):
   continue  # generate no output
  if line.startswith('<L>'):
   idxmeta = idx
   continue  # generate no output
  # otherwise, copy the line to output
  output = line + '\n'
  fout.write(output)
 fout.close()
