from PIL import Image
from sys import argv
import cv2
import glob
import numpy as np
import os
import shutil

def process(filename, key, w, h):
    """
    Resize, rotate, and gray scale the image given inputs.

    Resize is applied before rotation so make sure the 
    aspect of your inputs mathces with original image.
    """
    image = Image.open(filename)
    resized_image = image.resize((w,h))
    if is_rorate=='y':
        if is_parallel=='y':
            if i%2==0:
                angle = 90
            else:
                angle = 270
        else:
            if i%2==0:
                angle = 0
            else:
                angle = 180
    else:
        angle = 0
    resized_rotated_image = resized_image.rotate(angle)
    resized_rotated_gray_image = cv2.cvtColor(np.array(resized_rotated_image), cv2.COLOR_RGB2GRAY)
    print(filename + ' converted')
    cv2.imwrite('./output/'+str(key)+'.jpg', resized_rotated_gray_image)

w = int(argv[1])  # the width of output image before rotation
h = int(argv[2])  # the height of output image before rotation
is_rorate = argv[3]  # if 'y' rotation will be applied 
is_parallel = argv[4]  # if 'y' the angle will be adjustd in 90 degree

shutil.rmtree('./output')
os.system('mkdir output')

for (i,image_file) in enumerate(glob.iglob('./source/*.jpg')):
	process(image_file, i, w, h)