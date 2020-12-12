lanman/xrefs/readme.txt

10-18-2020

There are numerous references in the vocabulary and notes. Most of these
references are to specific lines on specific pages of the reader.
Many others are references to specific sections of Whitney's grammar.
There are also references from the notes to the vocabulary, and perhaps
vice-versa.
We want to add markup so that future displays can coordinate all these references.

* code directory contains programs and scripts to generate variations
of the reader, notes, vocabulary files in orig directory

* reader1.txt
  This replaces the digitization line-numbers with page-line references.
python reader1.py ../orig/reader.txt

