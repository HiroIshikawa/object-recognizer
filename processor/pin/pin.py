import cv2
import sys

# Get user supplied values
imagePath = sys.argv[1]
cascPath = sys.argv[2]

def detect(cascade, img):
    rects = cascade.detectMultiScale(img, 1.1, 3, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,40))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def boxing(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite('boxed_'+imagePath, img);

def img_center(img):
	height, width, channels = img.shape
	center_x = width/2
	center_y = height/2
	print('center of image, x: '+str(center_x))
	print('center of image, y: '+str(center_y))
	return (center_x, center_y)

def box_size(rects):
	box_width = abs(rects[0][0] - rects[0][2])
	box_height = abs(rects[0][1] - rects[0][3])
	print('width of box: '+str(box_width))
	print('height of box: '+str(box_height))
	return (box_width, box_height)

def box_center(recnts):
	box_x = abs(rects[0][0] - rects[0][2])/2 + rects[0][0]
	box_y = abs(rects[0][1] - rects[0][3])/2 + rects[0][1]
	print('x of object: '+str(box_x))
	print('y of object: '+str(box_y))
	return (box_x, box_y)

def box_to_center(img_center, box_center):
	box_rel_x = img_center[0]-box_center[0]
	box_rel_y = img_center[1]-box_center[1]
	print('position of box to x: '+str(box_rel_x))
	print('position of box to y: '+str(box_rel_y))
	return (box_rel_x, box_rel_y)

# Create the haar cascade
cascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect object maching with given cascade
rects, img = detect(cascade, image)

# Box around detected object
boxing(rects, img)

# Get the coordinate of the center of the image
img_center = img_center(img)

# Get the size of the box
box_size = box_size(rects)

# Get the coordinate of the center of box
box_center = box_center(rects)

# Get the relative positon of the box to the center of image
box_to_center = box_to_center(img_center, box_center)
