# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html

# 
# http://blog.christianperone.com/2015/01/real-time-drone-object-tracking-using-python-and-opencv/

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,400)
cap.set(4,300)

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
c,r,w,h = 200-25,150-25,50,50  # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((110., 50.,50.)), np.array((130.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(True):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # print(dst)

        if not dst.any():
            print ("No dst")
        else:
        # apply meanshift to get the new location
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        x,y,w,h = track_window
        cv2.rectangle(frame, (x,y), (x+w,y+h), 255, 2)
        cv2.putText(frame, 'Tracked', (x-25,y-10), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255,255,255), 2, cv2.CV_AA)
        
        cv2.imshow('Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # # Draw it on image
        # print(ret)
        # pts = cv2.cv.BoxPoints(ret)
        # print("Pts: "+str(pts))
        # pts = np.int0(pts)
        # pts = np.array(pts, np.int32)
        # # pts = pts.reshape((-1,1,2))
        # print("Pts: "+str(pts))

        # pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        # pts = pts.reshape((-1,1,2))
        # cv2.polylines(img,[pts],True,(0,255,255))

        # img2 = cv2.polylines(frame,[pts],True,(0,0,255))
        # print(img2)
        # cv2.imshow('img2',frame)
        # cv2.imshow('img2',frame)

        # k = cv2.waitKey(60) & 0xff
        # if k == 27:
        #     break
        # else:
        #     cv2.imwrite(chr(k)+".jpg",img2)

    else:
        break

cv2.destroyAllWindows()
cap.release()