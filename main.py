# -*- coding: utf-8 -*-
# @Author: prabhakar
# @Date:   2016-05-03 20:05:15
# @Last Modified by:   Prabhakar Gupta
# @Last Modified time: 2016-05-06 15:58:55

from PIL import Image
from pytesser.pytesser import *
import sys
import os, os.path


valid_images = [".jpg",".gif",".png",".tga",".tif",".bmp"]


# path = "/home/prabhakar/Pictures/Wallpapers"
# image_file_name = sys.argv[1]
# 

path = sys.argv[1]
directory_path = path + '/converted-text/'

if not os.path.exists(directory_path):
    os.makedirs(directory_path)

count = 1
for f in os.listdir(path):
	ext = os.path.splitext(f)[1]
	if ext.lower() not in valid_images:
		continue
	else :
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
		if count == 1:
			print str(count) + ' file completed'
		else:
			print str(count) + ' files completed'
		print '----------------'
		
		count += 1
				# print text

