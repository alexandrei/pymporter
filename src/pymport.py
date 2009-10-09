#!/usr/bin/env python

""" Learning Python.

The final goal is to have a small script that imports and renames photos according to EXIF data
"""

import sys
import os
import logging
import re
import EXIF

from datetime import datetime, timedelta

LEVELS = {
  'debug': logging.DEBUG,
  'info' : logging.INFO,
  'error': logging.ERROR
  }

__logfile = "pymport.log"
g_extensions = ('.jpg', '.jpeg')
g_raw_extensions = ('.orf')
g_tags = ["Image DateTime", "EXIF DateTimeOriginal", "DateTime"]
__groups_time_delta = timedelta(hours = 6)

class ConverterApp():
    from_root = ""
    to_root = ""
    jpeg_list = []
    raw_list = []
    group = []
    
    def __init__(self, from_root = None, to_root = None):
        self.from_root = from_root
        self.to_root = to_root
        
    def get_files(self):
        for root, dirs, files in os.walk(self.from_root):
            for file_name in files:
                file_name_lower = file_name.lower()
                if file_name_lower.endswith(g_extensions):  
                    self.jpeg_list.append(JpegFile(os.path.join(root,file_name)))
    
                if file_name_lower.endswith(g_raw_extensions):
                        self.raw_list.append(RawFile(os.path.join(root, file_name)))
                        
    def read_meta(self):
        for jpeg in self.jpeg_list:
            jpeg.get_exif_data()
                        
    def match_raw(self):
        for jpeg in self.jpeg_list:
            jpeg_path = os.path.splitext(jpeg.path)
            jpeg_path = jpeg_path[0].lower()
            for raw in self.raw_list:
                raw_path = os.path.splitext(raw.path)
                raw_path = raw_path[0].lower()
                
                if jpeg_path == raw_path:
                    jpeg.set_raw(raw)
                    self.raw_list.remove(raw)
        

class BaseFile:
    name = ""
    extension = ""
    path = ""
    
    def __init__(self, filepath = None):
        self.path = filepath
        self._get_extension()
        self._get_name()
        
    def _get_extension(self):
        self.extension = os.path.splitext(self.path)[1] #path has to be a file path, not a dir path!
    
    def _get_name(self):
        self.name = os.path.split(self.path)[1] 

class JpegFile(BaseFile):
    _has_raw = None
    _has_group = None
    _iso_time = ""
    
    def __init__(self, filepath = None):
        BaseFile.__init__(self, filepath)
        
    def set_raw(self, raw_file = None):
        self._has_raw = raw_file
        
    def set_group(self, group = None):
        self._has_group = group
        
    def get_exif_data(self):
        try:
            f = open(self.path, 'rb')
        except IOError:
            print "Failed to open file %s" % self.path
        else:
            try:
                tags = EXIF.process_file(f, details = False)
                for tag in g_tags:
                    try:
                        dt_value = str(tags[tag])
                        break
                    except:
                        continue
                if dt_value:
                    self._iso_time = datetime.strptime(dt_value, "%Y:%m:%d %H:%M:%S")

            finally:
                f.close()
    
class RawFile(BaseFile):
    def __init__(self, filepath = None):
        BaseFile.__init__(self, filepath)
        
class FilesGroup(list):
    name = ""
    start_time = ""
    is_locked = False

def create_groups(list, offset):
    files = list.getiterator("file")
    groups = Element("groups")
    list.append(groups)
    default_group = Element("group", {"name":"default"})
    groups.append(default_group)

    for ofile in files:
        of_ctime = ofile.find("exif").get("DateTime")
        of_iso_time = datetime.strptime(of_ctime, "%Y:%m:%d %H:%M:%S")

        current_group = Element("group", {"time":of_ctime})
        other_files_in_group = 0
        current_group.append(copy.deepcopy(ofile))

        for file in files:
            if file != ofile:
                ctime = file.find("exif").get("DateTime")
                iso_time = datetime.strptime(ctime, "%Y:%m:%d %H:%M:%S")
                if (iso_time - of_iso_time) < offset:
                    other_files_in_group += 1
                    current_group.append(copy.deepcopy(file))

        if other_files_in_group > 0:
            #add the current group to the groups list, and remove the ofile
            groups.append(current_group)
            list.remove(ofile)
        else:
            current_group = None
            default_group.append(copy.deepcopy(ofile))
            list.remove(ofile)

def add_output_date_time(list):
    files = list.getiterator("file")

    for file in files:
        output = Element("output")
        file.append(output)

        path = file.find("input").get("path")
        path = os.path.split(path)[0]
        ctime = file.find("exif").get("DateTime")

        datestr = ctime.split(' ')
        dd = datestr[0] #date
        dt = datestr[1] #time

        ctime = ctime.replace(':', '')
        ctime = re.sub('[^\d]+', '_', ctime)

        #year
        y = dd.split(':')[0]

        #month
        if len(dd.split(':')[1]) < 2:
          m = str('0') + dd.split(':')[1]
        else:
          m = dd.split(':')[1]

        #day
        if len(dd.split(':')[2]) < 2:
          d = str('0') + dd.split(':')[2]
        else:
          d = dd.split(':')[2]

        hr = dt.split(':')[0] #hour
        mi = dt.split(':')[1] #minutes
        se = dt.split(':')[1] #seconds

        output.set("datetime", ctime)
        output.set("year", y)
        output.set("month", m)
        output.set("day", d)
        output.set("hour", hr)
        output.set("minute", mi)
        output.set("second", se)

def main(args):
    
    #setup logging
    #===========================================================================
    # logging.basicConfig(
    #  filename=__logfile,
    #  level = logging.DEBUG,
    #  )
    # 
    # console = logging.StreamHandler()
    # console.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(messages)s')
    # console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)
    # 
    # logging.info('info message')
    # logging.error('error message')
    # logging.debug('debug message')
    #===========================================================================
    
    capp = ConverterApp("../input", "../output")
    capp.get_files()
    capp.read_meta()
    capp.match_raw()
 
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
