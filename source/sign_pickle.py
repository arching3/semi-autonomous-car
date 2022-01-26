import cv2
import pickle
import os
from cameraV2 import Cov_BGR2YUV_and_split, threshold, find_max_ct



path = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Image\sign"
names = os.listdir(path=path)

for i in names:
    img = cv2.imread(path + "\\" + i)
    show_img = img.copy()

    _, _, red = Cov_BGR2YUV_and_split(img)
    
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    _, red = threshold(red,180,255)

    ct, _ = cv2.findContours(red,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    ct = find_max_ct(ct)
    (x,y,w,h) = cv2.boundingRect(ct)
    _, _, roi = cv2.split(img[y:y+h,x:x+w])

    _, roi = threshold(roi,80,255,cv2.THRESH_BINARY_INV)

    ct_roi, _ = cv2.findContours(roi,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    ct_roi = find_max_ct(ct_roi)

    cv2.drawContours(show_img,ct_roi,-1,(0,0,255),3)

    show_roi = show_img[y:y+h,x:x+w]

    (cx,cy,cw,ch) = cv2.boundingRect(ct_roi)
    num_roi = show_roi[cy:cy+ch, cx:cx+cw]

    os.chdir(r"D:\Hawon\A_Study\VScode\pythonAutoCar\source\pickle")

    with open(str(names[names.index(i)]) + "_contour.pickle", "wb") as f:
        pickle.dump(ct_roi,f)
        print("sucess")

    cv2.imshow("mat",show_img)
    cv2.imshow("num",num_roi)
    cv2.imshow("re",roi)

    cv2.waitKey(0)