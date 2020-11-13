echo "temp_lsr0_refs"
cp ../../orig0/lsr0_refs.txt temp_lsr0_refs.txt
echo "check_ea_before"
python check_ea.py temp_lsr0_refs.txt check_ea_before.txt
echo "check_as_before.txt, as_romanuni1.xml"
python check_as.py temp_lsr0_refs.txt as_romanuni.xml check_as_before.txt as_romanuni1.xml
echo "lsr1_refs.txt"
python as_iast.py temp_lsr0_refs.txt as_romanuni2 lsr1_refs.txt
echo "check_as_after.txt"
python check_as.py lsr1_refs.txt as_romanuni2.xml check_as_after.txt temp_as_romanuni2.xml
echo "check_ea_after.txt"
python check_ea.py lsr1_refs.txt check_ea_after.txt

echo "temp_lsr1a_refs.txt"
python ../../meta/updateByLine.py lsr1_refs.txt manualByLine.txt temp_lsr1a_refs.txt
echo "temp_lsr1b_refs.txt"
python close_bold.py bold temp_lsr1a_refs.txt manualByLine_bold.txt
python ../../meta/updateByLine.py temp_lsr1a_refs.txt manualByLine_bold.txt temp_lsr1b_refs.txt
echo "lsr2_refs.txt"
python close_bold.py italic temp_lsr1b_refs.txt manualByLine_italic.txt
python ../../meta/updateByLine.py temp_lsr1b_refs.txt manualByLine_italic.txt lsr2_refs.txt

echo "Separating lsr2_refs into sections"
python separate.py lsr2_refs.txt
echo "Moving section files to parent directory"
mv abbreviations.txt ../
mv explanations.txt ../
mv notes.txt ../
mv vocabulary.txt ../

