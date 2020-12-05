echo "notes redo.sh BEGIN"
echo "notes0.txt"
python updateByLine.py ../orig/notes.txt manualByLine.txt notes0.txt
echo "notes1.txt"
python extra3_notes.py notes0.txt notes1.txt
echo "index.html"
python make_html1.py notes1.txt selections.txt index.html
echo "lanlinks.txt"
python lanlinks.py index.html lanlinks.txt

echo "redo.sh END"
