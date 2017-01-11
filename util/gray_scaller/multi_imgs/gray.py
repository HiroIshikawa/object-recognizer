# import cv2
# from sys import argv

# target = argv[1]

# image = cv2.imread(target)
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imwrite('grayed'+target,gray_image)

import cv2

def process(filename, key):

    image = cv2.imread(filename)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("writing..")
    print(gray_image)
    print(filename)
    cv2.imwrite('./output/'+str(key)+'.jpg', gray_image)