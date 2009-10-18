#!/usr/bin/env python

""" Learning Python.

The final goal is to have a small script that imports and renames photos according to EXIF data
"""

import sys
import os
import logging
import copy
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

c_bucket_group_enabled = False
c_bucket_group_name = "Bucket"
c_bucket_group_min_count = 5

class ConverterApp():
    from_root = ""
    to_root = ""
    jpeg_list = []
    raw_list = []
    groups = []
    
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
                                         
    def regroup(self, time_offset):
        #create list of files to be used for regrouping
        regroup_files_list = []
        
        if len(self.groups) == 0:
            regroup_files_list = copy.copy(self.jpeg_list) #on first 'regroup', we start with a copy of jpeg_list, so that we do not change it further on
            
        else:
            i = 0
            while True:
                try:
                    group = self.groups[i]
                except IndexError:
                    break
                
                if group.is_locked == False:
                    regroup_files_list.extend(group)                    
                    self.groups.remove(group)
                    continue
                else:
                    i += 1
                    
        bucket_group = FilesGroup()
        bucket_group.name = c_bucket_group_name
        
        while len(regroup_files_list) > 0:
            file_a = regroup_files_list[0]
            regroup_files_list.remove(file_a)
            
            temp_group = FilesGroup()
            temp_group.start_time = file_a._iso_time
            temp_group.add(file_a)

            #manually manage the list index when iterating for file_b, because we're removing files
            i = 0
            
            while True:
                try:
                    file_b = regroup_files_list[i]
                except IndexError:
                    break
                
                timediff = file_a._iso_time - file_b._iso_time              
                if timediff.days < 0 or timediff.seconds < 0:
                    timediff = file_b._iso_time - file_a._iso_time
                
                if timediff < time_offset:
                    temp_group.add(file_b)
                    regroup_files_list.remove(file_b)
                    continue # :D we reuse the old position, because all elements shifted to the left
                    
                else:
                    i += 1 #the index is increased normally

            self.groups.append(temp_group)

            #move files to bucket
            if c_bucket_group_enabled == True:                    
                if len(temp_group) < c_bucket_group_min_count:
                    for file in temp_group:
                        bucket_group.add(file)
                        temp_group.remove(file)    
                else:
                    self.groups.append(temp_group)      
                         
        if len(bucket_group) > 0:
            self.groups.append(bucket_group)
        

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
    
    def len(self):
        return len(self)
    
    def add(self, *args):
        self.extend(args)
        return None

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
    
    ##create some fake groups
    
#    g1 = FilesGroup()
#    g1.name = "Group 1"
#    g1.add(capp.jpeg_list[0])
#    g1.add(capp.jpeg_list[1])
#    
#    g2 = FilesGroup()
#    g2.name = "Group 2"
#    g2.is_locked = True
#    g2.add(capp.jpeg_list[2])
#    g2.add(capp.jpeg_list[3])
#    
#    g3 = FilesGroup()
#    g3.name = "Group 3"
#    g3.add(capp.jpeg_list[4])
#    g3.add(capp.jpeg_list[5])
#    
#    capp.groups.append(g1)
#    capp.groups.append(g2)
#    capp.groups.append(g3)
    
    capp.regroup(timedelta(minutes = 10))
    print ("with 15 minutes offset we have %d groups" % len(capp.groups))
    
    for group in capp.groups:
        print "\tgroup %s has %d files" % (group.name, len(group))
        for file in group:
            print "\t\t", file.name, file._iso_time
    
    print "\n \n"
#    
#    capp.regroup(timedelta(hours = 2))
#    print ("with 2 hours offset we have %d groups" % len(capp.groups))
#    
#    for group in capp.groups:
#        print "\tgroup %s has %d files" % (group.name, len(group))
#        for file in group:
#            print "\t\t", file.name, file._iso_time
#            
#    print "\n \n"
#    
    capp.regroup(timedelta(days = 7))
    print ("with 7 days offset we have %d groups" % len(capp.groups))
    
    for group in capp.groups:
        print "\tgroup %s has %d files" % (group.name, len(group))
        for file in group:
            print "\t\t", file.name, file._iso_time
 
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
