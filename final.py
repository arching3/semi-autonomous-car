import cv2
import os
import numpy as np
import pickle
from numpy.core.fromnumeric import shape, resize
import socket

"""
30 : 130
50 : 150

max value = 255

turn_left, turn_right = 150
"""

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

#streamserver = "http://192.168.137.158:81/stream"
streamserver = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Video\drive1.mp4"

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "192.168.137.146"
command = ""
strength = 0

cap = cv2.VideoCapture(streamserver)
th_bl = np.zeros_like(cap.read()[1])

pickle_list = os.listdir(path=r"D:\Hawon\A_Study\VScode\pythonAutoCar\source\pickle")
im_ct_list = []
for i in pickle_list:
    with open(r"D:\Hawon\A_Study\VScode\pythonAutoCar\source\pickle" + "\\" + i,'rb') as f:
        im_ct_list.append(pickle.load(f))
num_list = [30,50,70,90]


while True:
    _, frame = cap.read()


    frame = cv2.rotate(frame,cv2.ROTATE_180)
    frame = cv2.resize(frame,(400,296))
    orgin_frame = frame.copy()

    _, _ , red = Cov_BGR2YUV_and_split(frame)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)


    _, th = threshold(red,175,255)
    contours, _ = cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    
    try:
        contours = find_max_ct(contours) 

        (x,y,w,h) = cv2.boundingRect(contours)

        th = frame[y:y+h, x:x+w]

        _, _, th = cv2.split(th)

        _, th = threshold(th, 70, 255,cv2.THRESH_BINARY_INV)


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

        if num_list[dist.index(min(dist))] == 30:
            print("detect limit velocity : 50")
            strength = 130

        elif num_list[dist.index(min(dist))] == 50:
            print("detect limit velocity : 30")
            strength = 150
        
            
    
    except Exception as e:
        print(e)

    gray = orgin_frame[120:296, 0:400]

    gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray,140,255)


    h,w = gray.shape[:2]

    roi = gray[int((h*5)/6):h,0:w]
    gray = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    lines = cv2.HoughLinesP(roi,1,np.pi/180,1,None,1,1)
    
    try:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            if(int((x1+x2)/2)) >  int(roi.shape[1]/2)+10:

                print("right")


            
            elif (int((x1+x2)/2)) <  int(roi.shape[1]/2)-10:

                print("left")

            
            elif int(roi.shape[1]/2)-10 < (int((x1+x2)/2)) and (int((x1+x2))/2) < int(roi.shape[1]/2)+10:

                print("foward")

    except Exception as e:
        print(e)

    cv2.imshow("left",roi)
    cv2.imshow("src",orgin_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
