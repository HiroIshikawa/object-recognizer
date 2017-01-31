from PIL import Image
from sys import argv
import cv2
import glob
import numpy as np
import os
import shutil

def process(filename, key, w, h):
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

w = int(argv[1])
h = int(argv[2])
is_rorate = argv[3]
is_parallel = argv[4]

shutil.rmtree('./output')
os.system('mkdir output')

for (i,image_file) in enumerate(glob.iglob('./source/*.jpg')):
	process(image_file, i, w, h)