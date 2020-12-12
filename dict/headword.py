# coding=utf-8
"""
The above coding=utf-8 is required in python2 versions, so the broken-bar
character in reHeadword is properly interpreted. 
See http://www.python.org/dev/peps/pep-0263/
headword.py contains the regular expression for recognizing headwords.
 The first group is key1, the 2nd is key2. The third may be empty or
 a homonym, in format ^n.  
 
"""
#reHeadworda = r'^<P>.*?{#(.*?)#}¦ *{%(.*?)%}' # common, but incomplete
#reHeadword = r'^<P>.*?{#(.*?)#}¦' # believed to be complete
# <HI>{@+   indicates a prefix 'sub-entry' in a verb

reHeadword = r'^[0-9][0-9][0-9][0-9][0-9] <HI>{@([^+].*?)@'

