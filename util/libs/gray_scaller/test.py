import glob
import cv2

from gray import process

for (i,image_file) in enumerate(glob.iglob('./source/*.jpg')):
        process(image_file, i)