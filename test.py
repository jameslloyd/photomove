#!/usr/bin/python
import re, os
path = "/media/disk1/Photos/manual-sort"
files = os.listdir(path)
pattern = "^[0-9]{4}-[0-1][0-9]-[0-3][0-9]"


for fname in files:
	match = re.match(pattern, fname)
	if match:
		print 'MATCH\t' + fname
		split1 = fname.split(' ')
		split2 = split1[0].split('-')
		path = split2[0] + '/' + split2[1] + '/' + split2[2] + '/'
		print path
		
	else:
		print 'NO \t' + fname 
