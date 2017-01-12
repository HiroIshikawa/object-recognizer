import os
import shutil

from glob import glob, iglob
from sys import argv

import time

# Preprpcessing (TO Develope)
# - Cropping 
# - Sizing 
# - Grayscaling



# Clearning previous training stack
# ../classifier
shutil.rmtree('../classifier')
os.system('mkdir ../classifier')
# ../samples/*.vec
shutil.rmtree('../samples')
os.system('mkdir ../samples')
# ../samples.vec
try:
    os.remove('../samples.vec')
except OSError:
    pass

""" 
Training Configurations
- Dimention size of samples train, -w -h
- Z-dimension angle (related to rotation level), -maxzangle 2.0 
- Number of samples to generate
"""

sample_w = argv[1]		# -w
sample_h = argv[2] 		# -h
z_angle = argv[3]  		# -maxzangle
num_samples = argv[4] 	# -> -num
to_show = argv[5]		# -show

# Compute number of vectors to create for each positive imaegss
num_pos_imgs = len(glob('../positive_images/*.jpg'))
num_per_create = int(num_samples) / num_pos_imgs

# Generate vector files for each positive images in specified configurations
for (i,image_file) in enumerate(iglob('../positive_images/*.jpg')):
	command = 'opencv_createsamples -num ' + str(num_per_create) + \
				' -img ' + image_file + \
				' -bg ../negatives.txt -vec ../samples/' + str(i) + \
				'.vec -maxxangle 0.5 -maxyangle 0.5 -maxzangle ' + z_angle + \
				' -w ' + sample_w + ' -h ' + sample_h
	# print command
	os.system(command)

# Show one of the sample image from one of the vector files generated
if to_show=='y':
	command = 'opencv_createsamples -vec ../samples/0.vec' + \
				' -w ' + sample_w + ' -h ' + sample_h
	os.system(command)

# Merge vector files into one vector file
command = 'cd .. && python ./tools/mergevec.py -v samples/ -o samples.vec'
os.system(command)