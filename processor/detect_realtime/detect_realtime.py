#opens up a webcam feed so you can then test your classifer in real time
#using detectMultiScale
import numpy
import cv2
from sys import argv
import time
import threading


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

# Get the center of image
def centering_img(img):
    height, width, channels = img.shape
    center_x = width/2
    center_y = height/2
    # print('center of image, x: '+str(center_x))
    # print('center of image, y: '+str(center_y))
    return (center_x, center_y)

# Get the size of a box
def sizing_box(rect):
    box_width = abs(rect[0] - rect[2])
    box_height = abs(rect[1] - rect[3])
    # print('width of box: '+str(box_width))
    # print('height of box: '+str(box_height))
    return (box_width, box_height)

# Get the coordinate of the center of a box in the image
def centering_box(rect):
    box_x = abs(rect[0] - rect[2])/2 + rect[0]
    box_y = abs(rect[1] - rect[3])/2 + rect[1]
    # print('x of object: '+str(box_x))
    # print('y of object: '+str(box_y))
    return (box_x, box_y)

# Get the relative postion of the box to the center of the image
def pos_from_center(img_center, box_center):
    box_rel_x = box_center[0]-img_center[0]
    box_rel_y = box_center[1]-img_center[1]
    # print('position of box to x: '+str(box_rel_x))
    # print('position of box to y: '+str(box_rel_y))
    return (box_rel_x, box_rel_y)

def mean(l):
    if len(l)==0:
        return 0.0
    return sum(l)/len(l)

def accm_position(candidates):
    threading.Timer(1.0, accm_position, args=[candidates]).start()
    # avg_pos = reduce(lambda x, y: x + y, candidates) / len(candidates)
    avg_pos = mean(candidates)
    candidates[:] = []
    if (avg_pos > 0):
        print("Turn Right: Rotate "+str(avg_pos)+" units")
    elif (avg_pos < 0):
        print("Turn Left: Rorate "+str(avg_pos)+" units")
    else:
        print("Go Straight")
    # print("Navigation: "+str(avg_pos)+" units")
    # return True

cap = cv2.VideoCapture(0)
cap.set(3,win_w)
cap.set(4,win_h)

candidates = []

accm_position(candidates)

while(True):
    ret, img = cap.read()
    rects, img = detect(img)
    box(rects, img)

    flag = False

    # Get the coordinate of the center of the image
    img_center = centering_img(img)

    # Get the stats of the each box
    num_boxes = len(rects)
    boxes = []
    for k in range(num_boxes):
        boxes.append({'box_id':0,'box_size': (0,0),'box_center':(0,0),'box_to_center':(0,0)})

    for i, rect in enumerate(rects):
        # Record box id
        boxes[i]['box_id'] = i
        # Get the size of the box
        box_size = sizing_box(rect)
        boxes[i]['box_size'] = box_size
        # Get the coordinate of the center of box
        box_center = centering_box(rect)
        boxes[i]['box_center'] = box_center
        # Get the relative positon of the box to the center of image
        box_to_center = pos_from_center(img_center, box_center)
        boxes[i]['box_to_center'] = box_to_center

    # for box in boxes:
    #     print(box)
    # for each box, find the best one to approach 
    if (boxes):
        # elminate the boxes that above the horizon


        # find the box having the maximum size
        maxSizeItem = max(boxes, key=lambda x:x['box_size'][0]*x['box_size'][1])

        # if (maxSizeItem['box_to_center'][0] > 0):
        #     # print("Turn Right: Rotate "+str(maxSizeItem['box_to_center'][0])+" units")
        # elif (maxSizeItem['box_to_center'][0] < 0):
        #     # print("Turn Left: Rorate "+str(maxSizeItem['box_to_center'][0])+" units")
        # else:
        #     # print("Go Straight")
        
        # print("The item which has max size: "+str(maxSizeItem))

        candidates.append(maxSizeItem['box_to_center'][0])

    cv2.imshow("frame", img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
	   break
