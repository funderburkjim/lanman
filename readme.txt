
* preliminary -- not used
LSR_A_all.txt and LSR_B_all.txt are in cp1252 encoding.

Generate list of difference:

python diff_cp1252.py LSR_A_all.txt LSR_B_all.txt diff_cp1252.txt 

python diffab_cp1252.py LSR_AB_Corr1.txt diff_AB_Corr1.txt
  15831 differences

python diffab_cp1252.py LSR_AB_Corr2.txt diff_AB_Corr2.txt
  6909  differences

* orig0/LSR_AB_corr5.txt
I think the text in LSR_AB_corr5.txt is the latest version.
mkdir orig0
put LSR_AB_corr5.txt into orig0.
The encoding is cp1252.
File received from Thomas Malten.
Internal dating of file is July 6, 2017.


* orig0/LSR_AB_corr5_utf8.txt
convert to utf-8 encoding
In orig0:
python cp1252_to_utf8.py LSR_AB_corr5.txt  LSR_AB_corr5_utf8.txt

* orig0/diff_AB_Corr5_utf8.txt
For most of the lines, the 'A' version is the same as the 'B' version.
However, there are several (100) lines where the A and B versions differ.
Prepare a file where these differences are easy to see, to facilitate
resolution of the differences.
python diffab_utf8.py LSR_AB_corr5_utf8.txt diff_AB_Corr5_utf8.txt


* orig0/diff_AB_Corr5_utf8_Copy_done.txt
Sampada Savardekar Thomas examined the 100 differences, and resolved.
The result in file 
Corrections by Sampada to the 'NE' lines of diff_AB_Corr5_utf8.txt.

* orig0/lsr0.txt
This takes the 'B' lines from diff_AB_Corr5_utf8_Copy_done.txt,
sligtly simplifies each line.  

python lsr0.py diff_AB_Corr5_utf8_Copy_done.txt lsr0.txt lsr0_pages.txt
Extract the 'B' lines. 
Also, 
a) replace the initial '+B<>' with a space.
b) put the [Pagexxx-y+..z] (page and column separators) on separate lines.

Write all the page break lines to file lsr0_pages.txt

29888 lines adjusted, with 675 page breaks
30563 records written to lsr0.txt
675 records written to lsr0_pages.txt

* orig0/lsr0_works.txt, lsr0_refs.txt

python lsr0_works.py lsr0.txt lsr0_works.txt lsr0_refs.txt

Separate the digitization into the text part and reference part.
text part:  lines 00001 to 02295; pages 1 through 106
reference part: lines 02296 through 29888  (also pages 107 through 405)
Actually, we split lsr0.txt at at line number 2401.

The lines in these two sections are quite different in format. Separating
the parts makes subsequent steps easier.
