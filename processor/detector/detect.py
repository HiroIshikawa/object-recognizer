#opens up a webcam feed so you can then test your classifer in real time
#using detectMultiScale
import numpy
import cv2
from sys import argv

w1 = int(argv[1])
h1 = int(argv[2])
scale_factor = float(argv[3])
min_neighs = int(argv[4])
win_w = int(argv[5])
win_h = int(argv[6])
cas1 = argv[7]
cas2 = argv[8]

def detect(img, cas, w, h):
    cascade = cv2.CascadeClassifier(cas)
    rects = cascade.detectMultiScale(img, scale_factor, min_neighs, cv2.cv.CV_HAAR_SCALE_IMAGE, (w,h))

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
    rects1, img = detect(img,cas1, w1, h1)
    w2 = h1
    h2 = w1
    rects2, img = detect(img,cas2, w2, h2)
    box(rects1, img)
    box(rects2, img)
    cv2.imshow("frame", img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
	break