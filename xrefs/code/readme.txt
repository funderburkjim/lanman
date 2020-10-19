

python reader1.py ../../orig/reader.txt ../reader1.txt
- Remove the digitization sequence number of the first five columns
- Note the Page number from the [Page...+ y] lines
- Keep track of a pageline number.
- for each line that contains `<s>` tag, increment the pageline number,
  and insert the page and line number as 'pppll' (ppp and ll 0 filled).
  
