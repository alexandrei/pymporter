#!/usr/bin/env python

""" Learning Python. 

The final goal is to have a small script that imports and renames photos according to EXIF data
"""

import sys
import os
import EXIF

__usage = """Specify the input folder!"""
__version = """0.1"""
__extension = ('.jpg', '.jpeg')
__raw_extensions = ('.orf')

def usage():
    print __usage
    
def version():
    print __version

def main(args):
    for root, dirs, files in os.walk(args[0]):
        for file_name in files:
            try:
                f = open(os.path.join(root,file_name), 'rb')
            except IOError:
                print "Failed to open file %s" % os.path.join(root,file_name)
            else:
                print "Opened file %s" % os.path.join(root,file_name)
                tags = EXIF.process_file(f, stop_tag='DateTimeOriginal', details = False)
                try:
                    print tags['EXIF DateTimeOriginal']
                except KeyError:
                    print "Failed to get 'EXIF DateTimeOriginal' for file %s" % os.path.join(root,file_name)
                f.close()
        #if 'CVS' in dirs:
        #    dirs.remove('CVS')
    return 0

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        usage()
        sys.exit(1)
    elif '--version' in sys.argv:
        version()
        sys.exit(0)
    elif '--help' in sys.argv:
        usage()
        sys.exit(0)
    else:
        sys.exit(main(sys.argv[1:]))
