#!/usr/bin/env python

""" Learning Python. 

The final goal is to have a small script that imports and renames photos according to EXIF data
"""

import sys
import os
import EXIF
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump

__usage = """Specify the input folder!"""
__version = """0.2"""
__extensions = ('.jpg', '.jpeg')
__raw_extensions = ('.orf')

def usage():
    print __usage
    
def version():
    print __version
    
def print_input_list(tree):
    dump(tree)
    
def get_exif_data(list):
    files = list.getiterator("file")
    for file in files:
        input = file.find("input")
        file_exif = SubElement(file, "exif")
        try:
            f = open(input.get("path"), 'rb')
        except IOError:
            print "Failed to open file %s" % input.get("path")
        else:
            print "Opened file %s" % input.get("path")
            tags = EXIF.process_file(f, stop_tag='DateTimeOriginal', details = False)
            try:
                print tags['EXIF DateTimeOriginal']
                file_exif.set("DateTimeOriginal", str(tags['EXIF DateTimeOriginal']))
            except KeyError:
                print "Failed to get 'EXIF DateTimeOriginal' for file %s" % input.get("path")
            f.close()
        

def main(args):
    process = Element("process")
    jpeg_list = SubElement(process, "jpeg")
    raw_list = SubElement(process, "raw")
    #ElementTree(output).write(output_file)
    for root, dirs, files in os.walk(args[0]):
        for file_name in files:
            file_name_lower = file_name.lower()
            if file_name_lower.endswith(__extensions):
                input_details = Element("input", {"path":os.path.join(root,file_name), "name":file_name})
                
                file_details = Element("file")
                file_details.append(input_details)
                
                jpeg_list.append(file_details)
                
            if file_name_lower.endswith(__raw_extensions):
                file_details = Element("file", {"path": os.path.join(root,file_name), "name":file_name})
                
                raw_list.append(file_details)
                
    get_exif_data(jpeg_list)
    print_input_list(process)
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
