import cv2
from sys import argv

target = argv[1]

image = cv2.imread(target)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('grayed'+target,gray_image)
