#!/usr/bin/python
import os, time, datetime, subprocess, shutil, re, string
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
        return ret
    except IOError:
        return False

def get_image_date(fname,format = '/%Y/%m/%d %B %Y'):
    data = get_exif_data(fname)
    if not data:
        return False
    else:
        date = data['DateTimeOriginal']
        pattern = "^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4} [0-9]:[0-9][0-9]:[0-9][0-9]"
	match = re.match(pattern, date)
	if match:
        	date = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S').strftime(format)
        else:
        	print "failed"
        return date
    
def move_file(src,dest):
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)
    destdir = os.path.dirname(dest)
    if os.path.isfile(dest):
        print "Already Exists"
    else:
        if not os.path.isdir(destdir):
           os.makedirs(destdir)
           #print "want to make dir: " + destdir
        shutil.move(src ,dest)

def process_photo(path,rootpathdestination):
    files = os.listdir(path)    
    for fname in files:
        if not fname.startswith(".") or fname.endswith(".jpg") or fname.endswith(".jpeg") or fname.endswith(".mp4") or fname.endswith(".avi"):
            print path + '/' + fname
            date = get_image_date(path + '/' + fname)
            src = path + "/" + fname
            if date is not False:
                dest = rootpathdestination + date + '/' + fname 
        
                print "src = \t" + src
                print "dest = \t" + dest
                move_file(src,dest)
            else:
                #move_file(os.path)
				# cant find exif so try to use date in path name this should pick up the mp4's
				pattern = "^[0-9]{4}-[0-1][0-9]-[0-3][0-9]"
				match = re.match(pattern, fname)
				if match:
					split1 = fname.split(' ')
					split2 = split1[0].split('-')
					foldername = datetime.datetime( int(split2[0]), int(split2[1]), int(split2[2]), 0,0)
					
					regexpath = '/' + split2[0] + '/' + split2[1] + '/' + foldername.strftime('%d %B %Y') + '/'
					regexdest = rootpathdestination + regexpath + fname
					#print 'REGEX DESTINATION = ' + regexdest 
					#print src
					move_file(src,regexdest)
				else:
					print 'OFFENDING FILE = ' + fname
					move_file(src,'/media/disk1/Photos/manual-sort')

            
    
#process_photo("/media/disk6/Dropbox/picplz/jameslloyd","/media/disk1/photos")
process_photo("/media/disk6/Dropbox/Camera Uploads","/media/disk1/Photos")
process_photo("/media/disk6/Dropbox/Camera Uploads from Sarah","/media/disk1/Photos")
