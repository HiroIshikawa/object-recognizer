import cv2
import numpy as np
import os

from sys import argv

source = argv[1]
w = int(argv[2])
h = int(argv[3])

img_names = os.listdir("../../data/images/"+source)

for img_name in img_names:
	img = cv2.imread("../../data/images/"+source+"/"+img_name, cv2.IMREAD_GRAYSCALE)
	# should be larger than samples / pos pic (so we can place our image on it)
	resized_image = cv2.resize(img, (w, h))
	cv2.imwrite("resized/"+img_name, resized_image)