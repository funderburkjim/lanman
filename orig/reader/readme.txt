
* lsr1.txt
Add markup to lsr0_works.txt to delineate Sanskrit transcoding.
python deva_markup.py ../orig0/lsr0_works.txt lsr1.txt

Each line of lsr0_works consists of 
either a page break
[Pagexxx...]
or text
- a 5-digit line number 
- a space
- data

The data consists of markup.
Some markup identifies a section, and is of form <head>{#X#}</head>
This is changed to <section>X</section>
Other lines have various xml-style markup (all possibilities not yet
identified). However, it is believed that all the text-contents of these
represent Devanagari text in the printed edition.
The text content of these other elements is of the form, for some tag '<e>',
<e>X</e> where X is HK transliteration of Devanagari.  
For ease in further processing, we change this to <e><s>X</s></e>.
(We know that there is no other use in lsr0_works of the '<s>' markup element.)

There are a few instances where text is NOT included in an xml element, for
example 'anyacca | ' in line 556:
00556 anyacca | <lg><l>upakAriNi vizrabdhe zuddhamatau yaH samAcarati pApam |</l>
Such text is also put into '<s>..</s>' markup:
00556 <s>anyacca | </s><lg><l><s>upakAriNi vizrabdhe zuddhamatau yaH samAcarati pApam |</s></l>


* reader.txt
python slp1.py lsr1.txt reader.txt


Here, we change <s>X</s> to <s>Y</s> where Y is the slp1 transcoding 
corresponding to the HK encoding X.

The transcoder file used for transcoding the HK of lsr1 to SLP1 is
 lsr_slp1.xml

Peculiarities of the HK encoding:
1. danda is represented in this HK encoding by ascii vertical line  '|'.
   This is changed to the period '.' in SLP1
2. 'n~' is used in hk for palatal nasal (usual is 'J'). 
   This 'n~' is transcoded the usual slp1 'Y'.
3. In the Rig-Veda selections, accents are represented idiosyncratically.
   The printed representation of Devanagari accents is, to me at least,
   confusing. My best understanding is represented in
   https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc1/help/accents.html

   In lsr1.txt, there are two symbols used for Devanagari Vedic
   accents. In both the lsr1 HK encoding and in SLP1 encoding, the
   accent symbol follows a vowel.  Here is how these two accent symbols
   are transcoded in SLP1 (and Devanagari).
   †  udAtta  SLP1='/'   Unicode code point \u0951, DEVANAGARI STRESS SIGN UDATTA.
   _  anudAtta SLP='\'   Unicode code point \u0952, DEVANAGARI STRESS SIGN ANUDATTA.
   There are no instances of a 'svarita' accent in lsr1.txt, AFAIK.

   
* reader_deva.txt
Transcode the slp1 text to Devanagari.  This might facilitate comparison
to the Devanagari of scans.

python slp1_deva.py reader.txt reader_deva.txt

There are problems in reader_deva.txt when viewed with text editors.
Better solution is shown next.

* reader_deva.html

python slp1_deva_html.py reader.txt reader_deva.html

The sanskrit2003.ttf font is used as a web font.  This html file 
seems a good solution, being very close to the Lanman pdf.
See https://github.com/funderburkjim/lanman/issues/5.

* ../reader.txt
  This is a copy of reader.txt in the parent directory.
 cp reader.txt ../reader.txt
