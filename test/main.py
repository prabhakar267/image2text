# -*- coding: utf-8 -*-
# @Author: prabhakar
# @Date:   2016-05-03 20:05:15
# @Last Modified by:   Prabhakar Gupta
# @Last Modified time: 2016-05-03 20:07:04


from PIL import Image
from pytesser.pytesser import *

image_file = 'myimage.tif'
im = image.open(image_file)
text = image_to_string(im)
text = image_file_to_string(image_file)
text = image_file_to_string(image_file, graceful, errors=True)
print "havvy\n"
print text
