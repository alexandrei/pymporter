#!/usr/bin/env python

""" Learning Python. 

The final goal is to have a small script that imports and renames photos according to EXIF data
"""

import sys
import os
import EXIF
from xml.etree.ElementTree import ElementTree, Element

__usage = """Specify the input folder!"""
__version = """0.2"""
__extensions = ('.jpg', '.jpeg')
__raw_extensions = ('.orf')

def usage():
    print __usage
    
def version():
    print __version

def main(args):
    process = Element("process")
    jpeg_list = SubElement(process, "jpeg")
    raw_list = SubElement(process, "raw")
    #ElementTree(output).write(output_file)
    for root, dirs, files in os.walk(args[0]):
        for file_name in files:
            file_name_lower = file_name.lower()
            if file_name_lower.endswith(__extensions):
                input_details = Element("input")
                SubElement(input_details,"path",os.path.join(root,file_name))
                SubElement(input_details,"name",file_name)
                
                output_details = Element("output")
                
                file_details = Element("file")
                file_details.append(input_details)
                file_details.append(output_details)
                
                jpeg_list.append(file_details)
                
            if file_name_lower.endswith(__raw_extensions):
                file_details = Element("file")               
                SubElement(file_details,"path",os.path.join(root,file_name))
                SubElement(file_details,"name",file_name)
                
                raw_list.append(file_details)
                
                #try:
                #    f = open(os.path.join(root,file_name), 'rb')
                #except IOError:
                #    print "Failed to open file %s" % os.path.join(root,file_name)
                #else:
                #    print "Opened file %s" % os.path.join(root,file_name)
                #    tags = EXIF.process_file(f, stop_tag='DateTimeOriginal', details = False)
                #    try:
                #        print tags['EXIF DateTimeOriginal']
                #    except KeyError:
                #        print "Failed to get 'EXIF DateTimeOriginal' for file %s" % os.path.join(root,file_name)
                #    f.close()
            #else:
            #    print "Skip file %s" % os.path.join(root,file_name)
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
