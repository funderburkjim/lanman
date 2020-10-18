conversion from AS to IAST for Lanman refs.
June 4, 2020 begin.
Begin with orig0/lsr0_refs.txt

* check_ea   Extended ASCII inventory at start
python check_ea.py ../../orig0/lsr0_refs.txt check_ea_before.txt

* inventory of 'as'
python check_as.py ../../orig0/lsr0_refs.txt as_romanuni.xml check_as_before.txt as_romanuni1.xml

check_as_before.txt shows all 100 
 - AS codes (letter-number)
 - the corresponding Unicode transcoding of the the AS code
   Note that some AS codes are NOT transcoded: 
    
Note:  as_romanuni.xml started as a transcoder file from mw72.
check_as.py was run several times, and check_as_before.txt was examined in
the context of lsr0_refs.txt.   Based on this, several changes were made
to as_romanuni.xml. Finally, it was judged that the transcoding conversions
of as_romanuni.xml included all the required ones.
as_romanuni.xml includes numerous transcodings that are not used for
transcoding of lsr0_refs.txt.   The transcodings that ARE used are
written out to as_romanuni1.xml.

* as_romanuni2.xml  Adjusted transcodings 
as_romanuni2.xml starts as a copy of as_romanuni1.xml.
It is then modified manually, to deal with false positives and various
other transcoding details.
This applies all the as to unicode transcodings.

* Notes on  as_romanuni2
B1 and B2 appear 4 times.  Cross references to dictionary?
E4 É  once. Abbreviation of French name Émile
I1 Ī once THE STORY OF NALA AND DAMAYANTI1
a111 ā̀  once:  a with macron and grave accent
a12 ā2 2 times:  xref (mātrā2 2nd sense of mātrā)
a13 ā3  4 times; 2 are xref; 2 are pronunciation guides
a14 ā́  many times; a with macron and acute accent.
a15 ā5 once. xref
a16 ā6 once. xref
a17 ā7 once. xref
a2 a2 20. xref
a3 a3 16. xref
a4 á 4300.  Most are a with-acute.  Some are cross-references
a42 á2 4. a-acute xref.
a5 a5 6.  a xref
a6 a6 6.  a xref
a7 ä 22.  German a-umlaut
c1 c1 1.  Subsection. Should be capitalized
c2 c2 1.  Subsection. Should be capitalized
c3 c3 3.  c + xref
d2 ḍ 221. Retroflex d of Sanskrit.
          However, some are cross-refs. e.g. ({@avidat, £2vid2@}).
d3 d3 3.  xref
d4 d4 3.  xref
d5 d5 1.  xref
e1 ē 3.  Latin
e10 ê 1. French
e11 è 3. One Lithuanian, 2 Sanskrit
e2 e2 1. xref to Whitney?
e4 é 502. Sanskrit, French?
e5 ē 76. Latin and other languages
e7 ë 5. German and other languages
e74 ë́ 1. Lithuanian
h1 h1 1. xref
h2 ḥ 108. visarga
h3 h3 2. xref
h4 h4 1. xref
h5 h5 1. xref
i1 ī 1514. Sanskrit
i10 î 2. Arabic
i11 ì 1. i+grave Lithuanian
i111 ī̀ 3. i+macron+grave  Sanskrit
i14 ī́ 184. i + macron + acute. Sanskrit
i2 i2 8. xref
i3 i3 1. xref
i4 í 591. Sanskrit
i5 i5 3. xref
i7 ï 2. Sanskrit diphthong
j2 j2 2. xref
j3 j3 1. xref
j5 j5 3. xref
l2 ḷ 13. kl2p
l6 ḻ 31. (l with macron under)  represents  SLP1 'L'. Extension of IAST
m1 m1 1. xref
m2 m2 3. 2 are xref; one is Sam2hita1 (m-dot-under).  
         31 instances Sam3hita1 (m with dot above)
         Standard IAST is m-dot-under (anusvara)
m3 ṁ 379. Should change to m2 (standard anusvara)
m4 m4 4. xref
n2 ṇ 961. 
n3 ṅ 241. 
n4 n4 1. xref
n5 ñ 539. 
o10 ô 4. French
o11 ò 2. Sanskrit
o3 o3 1. xref
o4 ó 230. Sanskrit (and French?)
o42 ó2 1. xref
o5 ō 97. Latin
o7 ö 34. German, Norse
r2 ṛ 1577. 
r22 ṛ2 1. xref
r23 ṛ3 2. xref
r24 ṛ́ 192. r-dotunder-acute
r25 ṛ5 1. xref
r26 ṛ6 1. xref
r28 ṛ8 1. xref
r29 ṛ9 1. xref
r3 r3 3. xref
r9 ṝ 3. 
s2 ṣ 2177. 
s22 ṣ2 1. xref
s3 s3 7. xref
s4 s4 3. xref
t2 ṭ 635. 
t3 t3 1. xref
t4 t4 1. xref
t5 t5 1. xref
t7 t7 1. xref
u1 ū 761. 
u11 ù 2. 
u14 ū́ 123. 
u2 u2 4. xref
u3 u3 3. xref
u4 ú 508. 
u42 ú2 1. xref
u7 ü 109. German and ?
y1 ȳ 2. AS


l6  (l with macron under)  represents  SLP1 'L'.  See in dictionary 
page 130 under headword Iq.

l2  is l with under-dot  (kl2pta)
m3 (m with dot above) is anusvAra

* revisions in as_romanuni2.xml
For details see bottom of file.
m3 -> ṃ  
£ -> √
ç -> ś
Ç -> Ś

* lsr1_refs.txt
python as_iast.py ../../orig0/lsr0_refs.txt as_romanuni2 lsr1_refs.txt

* check 'as' codes after conversion
python check_as.py lsr1_refs.txt as_romanuni2.xml check_as_after.txt temp_as_romanuni2.xml
* check_ea_after   Extended ASCII inventory after conversion
python check_ea.py lsr1_refs.txt check_ea_after.txt

Differe
There are 37 cases in check_as_after.txt.
Most of these cases are like:
21925 ca ucyate,@} explained under {@ya2.@}</p>
'ya2' is a reference to the dictionary headword 'ya', and in particular to
the 2nd sense of 'ya'

* misc. corrections (Not yet done)
maybe 1aks2a4 -> 1 aks2a4  line 2334
line 19638  c1 -> C1
line 19650  c2 -> C2
m3 ṁ 379. Should change to m2 (standard anusvara)

* dict.txt, explanation.txt, abbreviation.txt, notes.txt
Separate lsr1_refs.txt into these subsections.
python separate.py lsr1_refs.txt 
This generates 4 files, which are moved to parent directory:
18033 lines written to vocabulary.txt
178 lines written to explanations.txt
163 lines written to abbreviations.txt
9776 lines written to notes.txt
