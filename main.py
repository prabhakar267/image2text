# -*- coding: utf-8 -*-
# @Author: prabhakar
# @Date:   2016-05-03 20:05:15
# @Last Modified by:   Prabhakar Gupta
# @Last Modified time: 2016-05-08 23:55:01

from PIL import Image
from pytesser.pytesser import *
import sys
import os, os.path


valid_images = [".jpg",".gif",".png",".tga",".tif",".bmp"]

def create_directory(path):
	if not os.path.exists(path):
	    os.makedirs(path)


def check_path(path):
	if os.path.exists(path):
		return True
	else:
		return False


path = sys.argv[1]

if check_path(path):
	directory_path = path + '/converted-text/'

	count = 0
	other_files = 0

	for f in os.listdir(path):
		ext = os.path.splitext(f)[1]
		if ext.lower() not in valid_images:
			other_files += 1
			continue
		else :

			if count == 0:
				create_directory(directory_path)

			count += 1
			image_file_name = path + '/' + f
			
			im = Image.open(image_file_name)
			text = image_to_string(im)
			text = image_file_to_string(image_file_name)
			text = image_file_to_string(image_file_name, graceful_errors=True)
			
			filename = os.path.splitext(f)[0]
			filename = ''.join(e for e in filename if e.isalnum() or e == '-')
			text_file_path = directory_path + filename + '.txt'
			
			text_file = open(text_file_path, "w+")
			text_file.write("%s" % text)
			text_file.close()

			print '----------------'
			print str(count) + (" file" if count == 1 else " files") + " completed"
			print '----------------'

	if count + other_files == 0:
		print "No files found at your given location"
	else :
		print str(count) + " / " + str(count + other_files) + " files converted"

else :
	print "No directory found at " + format(path)