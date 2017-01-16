import glob
import cv2
import shutil
import os
import numpy as np
from sys import argv

w = int(argv[1])
h = int(argv[2])
is_parallel = argv[3]

shutil.rmtree('./output')
os.system('mkdir output')

def rotate_bound(image, angle):

    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    return cv2.warpAffine(image, M, (nW, nH))

def process(filename, key, w, h):

    image = cv2.imread(filename)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_resized_image = cv2.resize(gray_image, (w, h))
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
    gray_resized_rotated_image = rotate_bound(gray_resized_image, angle)
    print("writing..")
    print(gray_resized_rotated_image)
    print(filename)
    cv2.imwrite('./output/'+str(key)+'.jpg', gray_resized_rotated_image)

for (i,image_file) in enumerate(glob.iglob('./source/*.jpg')):
	process(image_file, i, w, h)