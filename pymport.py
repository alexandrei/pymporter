#!/usr/bin/env python

""" Learning Python. 

The final goal is to have a small script that imports and renames photos according to EXIF data
"""

import sys
import EXIF

__usage = """Specify the input folder!"""
__version = """0.1"""

def usage():
	print __usage
	
def version():
	print __version

def main(args):
	if(not len(args)):
		usage()
		return -1
	else:
		return 0

if __name__ == '__main__':
	if '--version' in sys.argv:
		version()
		sys.exit(0)
	elif '--help' in sys.argv:
		usage()
		sys.exit(0)
	else:
	    sys.exit(main(sys.argv[1:]))
