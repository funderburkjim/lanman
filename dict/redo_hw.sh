echo "BEGIN redo_hw.sh"
echo "hw0..."
python26 hw0.py ../orig/ben.txt benhw0.txt > benhw0_note.txt
echo "hw1..."
python26 hw1.py benhw0.txt benhw1.txt benhw1_note.txt 
echo "copying benhw1.txt to benhw2.txt"
cp benhw1.txt benhw2.txt
echo "comparing ben headwords and mw headwords..."
echo "SKIPPING THIS COMPARISON!!"
#php check_mw.php benhw2.txt check_mw.txt check_mw_not.txt
echo "DONE redo_hw.sh"
echo "NEXT, sh redo_xml.sh"
