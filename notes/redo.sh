echo "notes redo.sh BEGIN"
echo "notes0.txt"
python updateByLine.py ../orig/notes.txt manualByLine.txt notes0.txt
echo "notes1.txt"
python extra3_notes.py notes0.txt notes1.txt
echo "notes2.txt"
python extra2_notes.py notes1.txt notes2.txt
echo "notes3.txt"
python extra1_notes.py notes2.txt ../meta/abbrev.txt notes3.txt
echo "index.html"
python make_html1.py notes3.txt selections.txt ../meta/abbrev.txt index.html
echo "lanlinks.txt"
python lanlinks.py index.html lanlinks.txt

echo "redo.sh END"
