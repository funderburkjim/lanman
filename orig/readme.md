
## lanman/orig
Transcoding of lanman/orig0.
The author divides the text into 3 parts:
* Part I [Pages 1-106] : The reader   
  * There are 75 stories (I to LXXV) drawn from 8 texts (A to H)
* Part II [Pages 111 to 405]: 
  * [Pages 111 to 288] Vocabulary
  * [Pages 289 to 292] Explanations
  * [Pages 293 to 294] List of abbreviations
* Part III [Pages 297 to 405] : Notes

For the purpose of transcoding,
* Part I is in Devanagari; the original digitization uses the
  Harvard-Kyoto transliteration, with a few enhancements.
* Parts II and III use Lanman's version of IAST for Sanskrit words.

In this section, we modify the original transcoding as follows:
* Part I (reader)
  * add `<s>X</s>` markup to identify original Devanagari text
  * change the transliteration for X from HK to SLP1
  * For details, see the 'reader' subdirectory
  * Final form is reader.txt.
* Parts II and III
  * Revise Lanman's version of IAST to currently modern IAST.
  * For details, see the 'refs' directory.
  * Final form is refs.txt

The end results are:
* reader.txt
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


* lsr2.txt
python slp1.py lsr1.txt lsr2.txt


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

   
* lsr2_deva.txt
Transcode the slp1 text to Devanagari.  This might facilitate comparison
to the Devanagari of scans.

python slp1_deva.py lsr2.txt lsr2_deva.txt

There are problems in lsr2_deva.txt when viewed with text editors.
Better solution is shown next.

* lsr2_deva.html

python slp1_deva_html.py lsr2.txt lsr2_deva.html

The sanskrit2003.ttf font is used as a web font.  This html file 
seems a good solution, being very close to the Lanman pdf.
See https://github.com/funderburkjim/lanman/issues/5.

