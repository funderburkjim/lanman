echo "check_ea_before"
python check_ea.py ../../orig0/lsr0_refs.txt check_ea_before.txt
echo "check_as_before.txt, as_romanuni1.xml"
python check_as.py ../../orig0/lsr0_refs.txt as_romanuni.xml check_as_before.txt as_romanuni1.xml
echo "lsr1_refs.txt"
python as_iast.py ../../orig0/lsr0_refs.txt as_romanuni2 lsr1_refs.txt
echo "check_as_after.txt"
python check_as.py lsr1_refs.txt as_romanuni2.xml check_as_after.txt temp_as_romanuni2.xml
echo "check_ea_after.txt"
python check_ea.py lsr1_refs.txt check_ea_after.txt
echo "Separating lsr1_refs into sections"
python separate.py lsr1_refs.txt
echo "Moving section files to parent directory"
mv abbreviations.txt ../
mv explanations.txt ../
mv notes.txt ../
mv vocabulary.txt ../

