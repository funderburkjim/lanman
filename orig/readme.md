
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
  * Final form is reader.txt (2401 lines).
* Parts II and III
  * Revise Lanman's version of IAST to currently modern IAST.
  * For details, see the 'refs' directory.
  * Separate these into 4 files:
    * 18033 lines in vocabulary.txt
    *   178 lines in explanations.txt
    *   163 lines in abbreviations.txt
    *  9776 lines in notes.txt

