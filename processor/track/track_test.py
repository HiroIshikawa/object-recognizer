import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,400)
cap.set(4,300)

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
r,h,c,w = 100,100,100,100  # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(True):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        print(dst)

        if not dst.any():
            print ("No dst")
        else:
        # apply meanshift to get the new location
            ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # # Draw it on image
        # print(ret)
        # pts = cv2.cv.BoxPoints(ret)
        # print("Pts: "+str(pts))
        # # pts = np.int0(pts)
        # pts = np.array(pts, np.int32)
        # # pts = pts.reshape((-1,1,2))
        # print("Pts: "+str(pts))

        pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        pts = pts.reshape((-1,1,2))
        # cv2.polylines(img,[pts],True,(0,255,255))

        img2 = cv2.polylines(frame,[pts],True,(0,0,255))
        print(img2)
        cv2.imshow('img2',frame)
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