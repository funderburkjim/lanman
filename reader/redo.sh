echo "lanman/reader redo.sh BEGIN"
echo "reader0.txt"
python updateByLine.py ../orig/reader.txt manualByLine.txt reader0.txt
echo "reader1.txt"
python relabel.py reader0.txt reader1.txt
echo "index.html"
python make_html1.py deva reader1.txt ../notes/lanlinks.txt ../meta/lanlinks.txt index.html
echo "lanman/reader/redo.sh END"
