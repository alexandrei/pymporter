#!/usr/bin/env python

""" Learning Python. 

The final goal is to have a small script that imports and renames photos according to EXIF data
"""

import sys
import os
import copy
import EXIF
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump

__usage = """Specify the input folder!"""
__version = """0.3"""
__extensions = ('.jpg', '.jpeg')
__raw_extensions = ('.orf')
__tags = ["Image DateTime", "EXIF DateTimeOriginal", "DateTime"]

def usage():
    print __usage
    
def version():
    print __version
    
def print_input_list(tree):
    dump(tree)
    
def build_output_names(list):
    pass

def sort_jpeg_list(list):
    data = []
    for elem in list:
        key = elem.find("input").get("path")
        data.append((key, elem))
        
    data.sort()

    list[:] = [item[-1] for item in data]
    

    
def match_raw_files(raw_list, jpeg_list):
    jpegs = jpeg_list.getiterator("file")
    raws = raw_list.getiterator("raw")
    
    if (len(jpegs) > 0) and (len(raws) > 0):
        for jpeg in jpegs:
            for raw in raws:
                jpeg_path = jpeg.find("input").get("path")
                if jpeg_path is not None:
                    jpeg_path = os.path.splitext(jpeg_path)
                    jpeg_path = jpeg_path[0].lower()
                    
                raw_path = raw.get("path")
                if raw_path is not None:
                    raw_path = os.path.splitext(raw_path)
                    raw_path = raw_path[0].lower()
                
                if jpeg_path == raw_path:
                    jpeg.append(copy.deepcopy(raw))
                    raw_list.remove(raw)
                    continue
    
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
            try:
                tags = EXIF.process_file(f, details = False)
                for tag in __tags:
                    try:
                        dt_value = str(tags[tag])
                        break
                    except:
                        continue
                if dt_value:
                    file_exif.set("DateTime", dt_value)
                    
            finally:
                f.close()
        

def main(args):
    process = Element("process")
    jpeg_list = SubElement(process, "jpeg")
    raw_list = SubElement(process, "raw")
    
    for root, dirs, files in os.walk(args[0]):
        for file_name in files:
            file_name_lower = file_name.lower()
            if file_name_lower.endswith(__extensions):
                input_details = Element("input", {"path":os.path.join(root,file_name), "name":file_name})
                
                file_details = Element("file")
                file_details.append(input_details)
                
                jpeg_list.append(file_details)
                
            if file_name_lower.endswith(__raw_extensions):
                file_details = Element("raw", {"path": os.path.join(root,file_name), "name":file_name})
                
                raw_list.append(file_details)
                
    get_exif_data(jpeg_list)
    
    match_raw_files(raw_list, jpeg_list)
    
    sort_jpeg_list(jpeg_list)
    
    print_input_list(process)
    
    #ElementTree(output).write(output_file)
    
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
