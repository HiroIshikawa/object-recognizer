from __future__ import print_function
import cv2
import numpy as np
from matplotlib import pyplot as plt

try:
    img = cv2.imread(r'sources/source.jpg',0)
    template = cv2.imread(r'templates/template.jpg',0)
except IOError as e:
    print("({})".format(e))
else:
    img2 = img.copy()
    w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print("Method: %s" , meth)
    print("min_val: " , min_val)
    print("max_val: " , max_val)
    print("min_loc: " , min_loc)
    print("max_loc: " , max_loc)
    print(" ")
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img,top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth) #; plt.legend([min_val, max_val, min_loc, max_loc], ["min_val", "max_val", "min_loc", "max_loc"])

    plt.show()
    box = img[top_left[1]:top_left[1]+h,0:bottom_right[1]+w]
    cv2.imshow("cropped", box)
    cv2.waitKey(0)