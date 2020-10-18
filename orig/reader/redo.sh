echo "lsr1.txt ..."
python deva_markup.py ../../orig0/lsr0_works.txt lsr1.txt
echo "reader.txt ..."
python slp1.py lsr1.txt reader.txt
echo "reader_deva.txt ..."
python slp1_deva.py reader.txt reader_deva.txt
echo "reader_deva.html ..."
python slp1_deva_html.py reader.txt reader_deva.html
echo "copy reader.txt to parent"
 cp reader.txt ../reader.txt
