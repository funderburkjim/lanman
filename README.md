# lanman
Digitization of Lanman Sanskrit Reader

## pdfs
The digitization was made from a scanned image of Lanman's Sanskrit reader.  The pdfs directory has the scans formatted:
* in 2-page style : LSR-sanskritreaderw00lanm.pdf
* and 1-page format : sanskritreaderw00lanm_bw.pdf

## orig0
This contains the original digitization, obtained in 2017 from Thomas Malten.  Malten's staff prepared this digitization with his guidance.   
This directory also contains several preliminary programmatic refactorings. See the readme.txt therein for details of the steps.
* lsr0_works.txt contains the sample texts.
* lsr0_refs.txt contains the rest of the digitization (dictionary, notes).

Note: The material before the Devanagari version of Nala's (Page 1)
is not currently digitized. This includes:
* The preface (pages v-xii)
* Note to the fourth issue (page xiii)
* Contents (pages xv-xvii)
* Introductory Suggestions (xvix-xx)
* Transliterated text of story of nala (compare Devanagari pages 1-4)

## orig
* reader.txt contains  lsr0_works.txt, with SLP1 transcoding of Devanagari to
replace the HK (Harvard-Kyoto) transcoding of the original digitization.
* reader_deva.txt shows the text in Devanagari, so it should be directly
comparable to the Devanagari of the scanned images.
* reader_deva.html is an html form, which uses the web font Sanskrit2003.
* refs/lsr1_refs.txt changes the reference text to modern IAST.  For 
  convenience in further processing, lsr1_refs is separated into 4 files:
  * vocabulary.txt
  * explanations.txt
  * abbreviations.txt
  * notes.txt

