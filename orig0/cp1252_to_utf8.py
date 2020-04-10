""" cp1252_to_utf8.py
  Mar 31, 2016
utility program  converts a file encoded in the cp1252 encoding into
   that same file coded in the utf-8 encoding.
All conversion is done using the Python codecs
"""
from __future__ import print_function
import sys,codecs

if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 
 with codecs.open(filein,"r","cp1252") as f:
  x = f.read()
 with codecs.open(fileout,"w","utf-8") as f:
  f.write(x)
 # check?
 print(filein,"(cp1252 encoding)")
 print("converted to")
 print(fileout,"(utf-8 encoding)")
 # try reverse conversion and see if identity
 with codecs.open(fileout,"r","utf-8") as f:
  y = f.read()
 filechk = "temp_"+filein
 with codecs.open(filechk,"w","cp1252") as f:
  f.write(y)
 with codecs.open(filechk,"r","cp1252") as f:
  z = f.read()
 assert z==x

