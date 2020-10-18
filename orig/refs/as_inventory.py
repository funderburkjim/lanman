# coding=utf-8
""" as_inventory.py
"""
import sys,re,codecs
#import transcoder
#transcoder.transcoder_set_dir("");
if __name__=="__main__":
 filein = sys.argv[1]  # xxxwithmeta1.txt
 fileout = sys.argv[2] # xxxwithmeta2.txt
 with codecs.open(filein,"r","utf-8") as f:
  inlines = [x.rstrip('\r\n') for x in f]
  print len(inlines),"lines read from",filein
 outlines = inlines
 as_iast(outlines) # modifies outlines
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print len(outlines),"lines written to",fileout
