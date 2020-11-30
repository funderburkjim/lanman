echo "notes redo.sh BEGIN"
echo "notes0.txt"
python updateByLine.py ../orig/notes.txt manualByLine.txt notes0.txt
echo "notes1.txt"
python extra3_notes.py notes0.txt notes1.txt
echo "index.html"
python make_html1.py notes1.txt index.html
echo "lanlinks.txt"
python lanlinks.py index.html lanlinks.txt

#echo "lanhw0.txt"
#python hw0.py notes0.txt lanhw0.txt
#echo "lanhw1.txt  transcode"
#python hw1.py lanhw0.txt lanhw1.txt 
#echo "lanwithmeta.txt"
#python meta_hw.py notes0.txt.txt lanhw1.txt lanwithmeta.txt
#echo "lan_invert_meta.txt"
#python invert_meta.py lanwithmeta.txt temp_lan_invert_meta.txt
#echo "diff temp_lan.txt temp_lan_invert_meta.txt"
#diff temp_lan.txt temp_lan_invert_meta.txt
#echo "lanwithmeta1.txt"
#python extra1.py lanwithmeta.txt lanwithmeta1.txt #> temp_extra1.txt
#echo "lanwithmeta2.txt"
#python extra2.py lanwithmeta1.txt lanwithmeta2.txt 
#echo "lanwithmeta3.txt"
#python extra3.py lanwithmeta2.txt lanwithmeta3.txt 

echo "redo.sh END"
