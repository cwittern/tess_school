# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
import os, sys, codecs, re
from difflib import *

kanji=Ur'\u3000\u3400-\u4DFF\u4e00-\u9FFF\uF900-\uFAFF\uFE30-\uFE4F\U00020000-\U0002A6DF\U0002A700-\U0002B73F\U0002B740-\U0002B81F\U0002B820-\U0002F7FF'
pua=Ur'\uE000-\uF8FF\U000F0000-\U000FFFFD\U00100000-\U0010FFFD'
ent='\[[^\]]*\]|&[^;]*;|&amp;C[X3-7]-[A-F0-9]+'
#now
kp_re = re.compile(u"(%s|[%s%s])" % (ent, kanji, pua))
ch_re = re.compile(ur'(\[[^\]]*\]|&[^;]*;|&amp;C[X3-7]-[A-F0-9]+|.)')
img_re = re.compile(ur'<i[^>]*>')

#this should be the txt file
base=sys.argv[1]
#
def l_cleanup(line):
    line = re.sub(r' ', '', line)
    #line = re.sub(u'〔[一二三四五六七八九０]+〕', '', line)
    if line.startswith(':'):
        return line
    else:
        return line


s = SequenceMatcher()
s_txt=[]
s_box=[]
for line in codecs.open(base, 'r', 'utf-8'):
    line = l_cleanup(line)
    e=filter(None, re.split("(.)", line[:-1]))
    s_txt.extend(e)
for line in codecs.open("%s.box" % (base[:-4]), 'r', 'utf-8'):
    fields = line.split()
    s_box.extend(fields[0])
s.set_seqs(s_box, s_txt)
print base, s.ratio()
sys.stderr.write("%s %2.4f\n" % (base, s.ratio()))
