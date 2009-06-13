#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
'''
Small script to copy photo files according to their EXIF data.
 
'''
 
__version__ = '0.1'
__author__ = u'Draghina Alexandru'.encode('utf-8')

import EXIF

f = open("input/P6049984.JPG")
#f = open("input/P6094556.ORF")
tags = EXIF.process_file(f, details=False)
f.close()
for tag in tags.keys():
  if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
    print "%s: %s" % (tag, tags[tag])
