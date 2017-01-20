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

def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite('boxed_'+imagePath, img);


# Create the haar cascade
cascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

rects, img = detect(cascade, gray)
box(rects, img)


#cv2.imshow("Cups found", image)
#cv2.waitKey(0)