import glob
import cv2
import shutil
import os
from sys import argv

w = int(argv[1])
h = int(argv[2])

shutil.rmtree('./output')
os.system('mkdir output')

def process(filename, key, w, h):

    image = cv2.imread(filename)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_resized_image = cv2.resize(gray_image, (w, h))
    print("writing..")
    print(gray_resized_image)
    print(filename)
    cv2.imwrite('./output/'+str(key)+'.jpg', gray_resized_image)

for (i,image_file) in enumerate(glob.iglob('./source/*.jpg')):
	process(image_file, i, w, h)