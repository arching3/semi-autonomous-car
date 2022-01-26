import os
import cv2
import numpy as np
import pickle

def Cov_BGR2YUV_and_split(src):
    src = cv2.cvtColor(src,cv2.COLOR_BGR2YUV)
    return cv2.split(src)

def threshold(src, threshold_val, maxV, method = cv2.THRESH_BINARY):
    ret, src = cv2.threshold(src,threshold_val,maxV,method)
    return ret, src

def find_max_ct(contours):

    try:
        maxC = []
        for i in contours:
            maxC.append(len(i))
        temp = max(maxC)
        for i in range(len(maxC)):
            maxC[i] = temp - maxC[i]
        
        Max_ct = contours[maxC.index(0)]
        return Max_ct
    except:
        return None
streamserver = "http://192.168.137.112:81/stream"
#streamserver = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Video\OVVideo.avi"

cap = cv2.VideoCapture(streamserver)
th_bl = np.zeros_like(cap.read()[1])

pickle_list = os.listdir(path=r"D:\Hawon\A_Study\VScode\pythonAutoCar\source\pickle")
im_ct_list = []
for i in pickle_list:
    with open(r"D:\Hawon\A_Study\VScode\pythonAutoCar\source\pickle" + "\\" + i,'rb') as f:
        im_ct_list.append(pickle.load(f))
num_list = [30,50]

while True:
    _, frame = cap.read()


    frame = cv2.rotate(frame,cv2.ROTATE_180)
    frame = cv2.resize(frame,(400,296))
    show_frame = frame.copy()

    _, _ , red = Cov_BGR2YUV_and_split(frame)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)


    _, th = threshold(red,175,255)
    contours, _ = cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    
    try:
        contours = find_max_ct(contours) # Assigning maximum value of contours to variable

        (x,y,w,h) = cv2.boundingRect(contours) # Finding the largest rectangle

        th = frame[y:y+h, x:x+w] # ROI

        _, _, th = cv2.split(th) # HSV

        _, th = threshold(th, 90, 255,cv2.THRESH_BINARY_INV) # Binary


    except:
        print("Cannot find Contours")

    try:
        th_ct, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        th_ct = find_max_ct(th_ct)

        (cx,cy,cw,ch) = cv2.boundingRect(th_ct)
        ct_roi_o = th[cy:cy+ch,cx:cx+cw]


        dist = []
        for i in range(len(im_ct_list)):
            temp = cv2.matchShapes(th_ct,im_ct_list[i],cv2.CONTOURS_MATCH_I3,0)
            dist.append(temp)

        # 30 50
        print("detect : " + str(num_list[dist.index(min(dist))]) + str(min(dist)))
    except:
        pass

    try:
        cv2.imshow("frame",show_frame)
        cv2.imshow("mnum",ct_roi_o)
        cv2.imshow("Value",th)
    except:
        pass
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
