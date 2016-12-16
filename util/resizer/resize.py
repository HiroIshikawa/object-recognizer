import cv2
import numpy as np
import os

from sys import argv

img_names = os.listdir("source")

w = int(argv[1])
h = int(argv[2])

for img_name in img_names:
	img = cv2.imread("source/"+img_name, cv2.IMREAD_GRAYSCALE)
	# should be larger than samples / pos pic (so we can place our image on it)
	resized_image = cv2.resize(img, (w, h))
	cv2.imwrite("resized/"+img_name, resized_image)
