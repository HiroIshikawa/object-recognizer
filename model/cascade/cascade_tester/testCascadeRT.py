#opens up a webcam feed so you can then test your classifer in real time
#using detectMultiScale
import numpy
import cv2
from sys import argv

obj_w = int(argv[1])
obj_h = int(argv[2])
scale_factor = float(argv[3])
min_neighs = int(argv[4])
win_w = int(argv[5])
win_h = int(argv[6])

def detect(img):
    cascade = cv2.CascadeClassifier("cascade.xml")
    rects = cascade.detectMultiScale(img, scale_factor, min_neighs, cv2.cv.CV_HAAR_SCALE_IMAGE, (obj_w,obj_h))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    # cv2.imwrite('one.jpg', img);

cap = cv2.VideoCapture(0)
cap.set(3,win_w)
cap.set(4,win_h)

while(True):
    ret, img = cap.read()
    rects, img = detect(img)
    box(rects, img)
    cv2.imshow("frame", img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
	break

