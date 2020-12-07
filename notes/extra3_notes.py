# coding=utf-8
""" extra3_notes.py
    See readme for discussion
"""
import sys,re,codecs
linenums_noadjust = set([
 66, 136, 143, 145, 146, 147, 
 158, 162, 194, 196, 199, 202, 215, 217,
 237, 374,  375, 480, 525, 652, 998, 1242,
 1258, 1259, 1266, 1268, 1269, 1276, 1287,
 1289, 1305, 1312, 1317, 1318, 1320, 1325, 1327,
 1343, 1407, 1428, 1435, 1442, 1492, 1554, 1558,
 8996,8997,8998, 8999,
 9675, 9676, 9679, 9688, 9716, 9723, 9731, 9756, 9762,
 9766, 9767, 9768, 9769, 9773,
 1664, 1696, 1720, 1830, 1868, 2004, 2011, 2020, 2222, 2240, 
 2246, 2284, 2286, 2291, 2351, 2400, 2431, 2432, 2436, 2472, 
 2498, 2587, 2592, 2629, 2724, 2727, 2729, 2730, 2759, 2761, 
 2766, 2823, 2824, 2828, 2888, 2889, 2893, 2920, 2924, 2936, 
 2937, 2941, 2946, 3038, 3190, 3193, 3263, 3268, 3276, 3286, 
 3297, 3348, 3372, 3393, 3478, 3512, 3551, 3558, 3590, 3615, 
 3631, 3641, 3647, 3666, 3847, 3853, 3858, 4017, 4060, 4092, 
 4239, 4359, 4373, 4374, 4385, 4395, 4433, 4500, 4515, 4543, 
 4578, 4591, 4854, 4917, 4969, 5507, 5542, 5609, 5929, 5933, 
 6110, 6232, 6415, 6599, 6640, 6779, 6885, 6906, 7072, 7253, 
 7321, 7417, 7475, 7646, 7742, 7762, 8113, 8314, 8856, 8907, 
 9047, 9070, 9116, 9398, 9661, 

 2348, 2356, 2398, 2401, 2578, 2624, 2625, 2627, 2722, 2728,
 2814, 2821, 2829, 2983, 3037, 3046, 3092, 3093, 3094, 3095,
 3144, 3287, 3290, 3294, 3335, 3345, 3384, 3385, 3387, 3510,
 3572, 3577, 3583, 3588, 3626, 3643, 3856, 3874, 4006, 4022,
 4041, 4046, 4067, 4087, 4090, 4101, 4090, 4168, 4405, 4438,
 4546, 4601, 2821, 2829, 2676, 2348, 2728, 2356, 2401, 2398,
 2624, 3037, 3046, 3092, 3387, 3093, 3094, 3095, 3144, 3287,
 3290, 3384, 3385, 3572, 3510, 3626, 1797, 2578, 4041, 4067, 
 4405, 4492, 4546, 4601, 4916, 5098, 5100, 5146, 5187, 5419,
 5439, 4168, 5465, 5627, 5823, 5844, 5902, 5934, 6060, 6161,
 6222, 6585, 6957, 7001, 7018, 7044, 7046, 7151, 7463, 7509,
 7581, 8121, 7641, 7652, 7793, 7842, 8123, 8176, 8265, 8301,
 8365, 8571, 8668, 8939, 8939, 9185, 9315, 
4022, 4046, 4111, 4343, 5464, 8120, 8307, 8913, 8972, 9624, 
3335, 3384, 3345, 7045, 7393, 8356, 8661, 8942, 2625, 2722, 
4087, 4113, 4342, 4427, 7167, 7647, 8971, 9356, 9412, 5171, 
7658, 7951, 8116, 8143, 8903, 9212, 9213, 9357, 9395, 5545, 
5869, 5880, 6017, 6499, 6958, 6998, 7043, 7118, 7674, 7766, 
7874, 8149, 5612, 8294, 8353, 8391, 2814, 7856, 8405, 8475, 
2627, 2983, 7471, 3294, 4006, 6012, 6820, 7016, 8017, 8292, 
8439, 9413, 3572, 3577, 3583, 3588, 3643, 4101, 1729, 1779, 
3874, 7885, 8272, 4968, 6753, 7155, 7629, 8662, 8797, 9156, 
9403, 9529, 9575, 9610, 9645, 9660, 9668, 9383, 
2283,
 ])
def adjust_page_line_helper(line):
 parts = re.split(r'([0-9]+\^[0-9]+\^)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^([0-9]+)\^([0-9]+)\^$',part)
  if m:
   pagenum = int(m.group(1))
   if pagenum <= 106:
    newpart = '<ls n="lan,%s,%s">%s</ls>' %(m.group(1),m.group(2),part)
    newparts.append(newpart)
   else:
    newparts.append(part)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_page_line(lines):
 """ X^Y^  (X and Y digit-sequences) ->
   <ls n="lan,X,Y">X^Y</ls>
   X <= 106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = adjust_page_line_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
 print(nadj,"cases changed in 'adjust_page_line'")

def adjust_page_lines_helper(line):
 parts = re.split(r'([0-9]+\^[0-9]+[, ]+[0-9, ]+\^)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^([0-9]+)\^([0-9]+[, ]+[0-9, ]+)\^$',part)
  if m:
   pagenum = int(m.group(1))
   if pagenum <= 106:
    newpart = '<ls n="lan,%s,%s">%s</ls>' %(m.group(1),m.group(2),part)
    newparts.append(newpart)
   else:
    newparts.append(part)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_page_lines(lines):
 """ X^Y^  (X and Y digit-sequences) ->
   <ls n="lan,X,Y">X^Y</ls>
   X <= 106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = adjust_page_lines_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: #True:
    print('; Case %s adjust_page_lines' % nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_page_lines'")

def adjust_whitney_sup_helper(line):
 parts = re.split(r'([0-9]+\^[0-9]+\^)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^([0-9]+)\^([0-9]+)\^$',part)
  if m:
   section = int(m.group(1))
   if section > 106:
    newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),part)
    newparts.append(newpart)
   else:
    newparts.append(part)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_sup(lines):
 """ X^Y^  (X and Y digit-sequences) ->
   <ls n="wg,X">X^Y</ls>
   X>106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = adjust_whitney_sup_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
 print(nadj,"cases changed in 'adjust_whitney_sup'")

def adjust_whitney_az_helper(line):
 parts = re.split(r'([0-9][0-9][0-9]+[a-z])',line)
 newparts = []
 for part in parts:
  m = re.search(r'^([0-9][0-9][0-9]+)([a-z])$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),part)
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_az(lines):
 """ X^Y^  (X and Y digit-sequences) ->
   <ls n="wg,X">X^Y</ls>
   X>106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = adjust_whitney_az_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: #True: 
    print('; Case %s adjust_page_lines' % nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))
 print(nadj,"cases changed in 'adjust_whitney_az'")

def adjust_whitney_4_period_helper(line):
 parts = re.split(r'(1[0-9][0-9][0-9][.,\]])',line)
 newparts = []
 for part in parts:
  m = re.search(r'^(1[0-9][0-9][0-9])([.,\]])$',part)
  if m:
   isection = int(m.group(1))
   if (isection >1316):
    m = None
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),part)
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_4_period(lines):
 """ X.  X a 4-digit sequence, then a period or comma or right square bracket->
   <ls n="wg,X">X.</ls>
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = adjust_whitney_4_period_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: #True:
    print('; Case %s whitney_4_period' % nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))
 print(nadj,"cases changed in 'adjust_whitney_4_period'")

def adjust_whitney_3_period_helper(line):
 parts = re.split(r'([^0-9][0-9][0-9][0-9][.,\]])|(<ls.*?</ls>)',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  m = re.search(r'^(.)([0-9][0-9][0-9])([.,\]])$',part)
  if m:
   newpart = '%s<ls n="wg,%s">%s</ls>' %(m.group(1),m.group(2),part[1:])
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_3_period(lines):
 """ X.  X a 4-digit sequence, then a period or comma or right square bracket->
   <ls n="wg,X">X.</ls>
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = adjust_whitney_3_period_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: #True:  
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_whitney_3_period'")

def adjust_whitney_3a_helper(line):
 parts = re.split(r'([\[ ][0-9][0-9][0-9]+)|(<ls.*?</ls>)',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  m = re.search(r'^([\[ ])([0-9][0-9][0-9]+)$',part)
  if m:
   newpart = '%s<ls n="wg,%s">%s</ls>' %(m.group(1),m.group(2),m.group(2))
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_3a(lines):
 """ ZX  where Z is space or [
    and X is a sequence of 3 or more digits
   Z<ls n="wg,X">X</ls>
  We exclude 3 known lines 
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  if (iline+1) in [9834, 11588, 15668]:
   # transform not applicable: not a whitney reference
   continue
  newline = adjust_whitney_3a_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False:
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_whitney_3a'")

def adjust_whitney_3b_helper(line):
 parts = re.split(r'(^[0-9][0-9][0-9]+)',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  m = re.search(r'^([0-9][0-9][0-9]+)$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),m.group(1))
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_3b(lines):
 """ X at beginning of line, where 
   X is a sequence of 3 or more digits
   Z<ls n="wg,X">X</ls>
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  #if (iline+1) in [9834, 11588, 15668]:
   # transform not applicable: not a whitney reference
   continue
  newline = adjust_whitney_3b_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: #True: 
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_whitney_3b'")

def adjust_whitney_2b_helper(line):
 parts = re.split(r'(^[0-9][0-9]+)',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  m = re.search(r'^([0-9][0-9]+)$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(1),m.group(1))
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_2b(lines):
 """ X at beginning of line, where 
   X is a sequence of 2 or more digits
   but only for a particular set of lines
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  if (iline+1) not in [38,5213, 12054, 17320, 17693]:
   # transform not applicable: not a whitney reference
   continue
  newline = adjust_whitney_2b_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if True: 
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))

 print(nadj,"cases changed in 'adjust_whitney_2b'")

def adjust_sup(lines):
 """ ^X^ -> <sup>X</sup>
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = re.sub(r'\^(.*?)\^',r'<sup>\1</sup>',oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: 
    print('; case %s'%nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))
 print(nadj,"cases changed in 'adjust_sup'")

def adjust_whitney_Whitney_helper(line):
 parts = re.split(r'(Whitney,? +[0-9]+[a-z]?)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^(Whitney,? +)([0-9]+)([a-z]?)$',part)
  if m:
   newpart = '<ls n="wg,%s">%s</ls>' %(m.group(2),part)
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_Whitney(lines):
 """ Whitney XY -> 
   <ls n="wg,X">Whitney XY</ls>
   X>106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = adjust_whitney_Whitney_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: #True: 
    print('; Case %s adjust_whitney_Whitney' % nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))
 print(nadj,"cases changed in 'adjust_whitney_Whitney'")

def adjust_whitney_see_helper(line):
 # see X or {%see%} X
 parts = re.split(r'({?%?see%?}? +[0-9]+[a-z]?)',line)
 newparts = []
 for part in parts:
  m = re.search(r'^({?%?see%?}? +)([0-9]+)([a-z]?)$',part)
  if m:
   newpart = '%s<ls n="wg,%s">%s%s</ls>' %(m.group(1),m.group(2),m.group(2),m.group(3))
   newparts.append(newpart)
  else:
   newparts.append(part)
 newline = ''.join(newparts)
 return newline

def adjust_whitney_see(lines):
 """ Whitney XY -> 
   <ls n="wg,X">Whitney XY</ls>
   X>106
 """
 nadj = 0
 for iline,oldline in enumerate(lines):
  if iline+1 in linenums_noadjust:
   continue
  newline = adjust_whitney_see_helper(oldline)
  if newline != oldline:
   nadj = nadj + 1
   lines[iline] = newline
   if False: #True:
    print('; Case %s whitney_see' % nadj)
    print('%s old %s' %(iline+1,oldline))
    print('%s new %s' %(iline+1,newline))
 print(nadj,"cases changed in 'adjust_whitney_see'")

def init_lines(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines0 = [x.rstrip('\r\n') for x in f]
 # remove initial 5-digit code and space
 lines = []
 labels = []
 for x in lines0:
  m = re.search(r'^([0-9]+) (.*)$',x)
  if not m:
   label = ''
   y = x
  else:
   label = m.group(1)
   y = m.group(2)
  lines.append(y)
  labels.append(label)
 print(len(lines),"lines read from",filein)
 return labels,lines

if __name__=="__main__":
 filein = sys.argv[1]  # xxxwithmeta1.txt
 fileout = sys.argv[2] # xxxwithmeta2.txt
 #with codecs.open(filein,"r","utf-8") as f:
 labels,inlines = init_lines(filein)
 # inlines = [x.rstrip('\r\n') for x in f]
 print(len(inlines),"lines read from",filein)
 outlines = inlines
 adjust_page_line(outlines)
 adjust_page_lines(outlines)
 adjust_whitney_sup(outlines)
 adjust_whitney_az(outlines)
 adjust_whitney_Whitney(outlines)
 adjust_whitney_see(outlines)
 adjust_whitney_4_period(outlines)
 adjust_whitney_3_period(outlines)
 #adjust_whitney_3a(outlines)
 #adjust_whitney_3b(outlines)
 #adjust_whitney_2b(outlines)
 adjust_sup(outlines)
 with codecs.open(fileout,"w","utf-8") as fout:
  for line in outlines:
   fout.write(line+'\n')
 print(len(outlines),"lines written to",fileout)
