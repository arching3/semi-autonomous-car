import cv2
import numpy as np
from numpy.core.fromnumeric import resize, shape


video_path = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Video\OVVideo.avi"
#streamserver = "http://192.168.137.158:81/stream"
cap = cv2.VideoCapture(video_path)



while True:

    _, frame = cap.read()
    frame = cv2.rotate(frame,cv2.ROTATE_180)
    frame = cv2.resize(frame,(400,296))
    gray = frame[120:296, 0:400]

    gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray,140,255)


    h,w = gray.shape[:2]

    roi = gray[int((h*5)/6):h,0:w]
    gray = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    lines = cv2.HoughLinesP(roi,1,np.pi/180,1,None,1,1)
    
    try:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            if(int((x1+x2)/2)) >  int(roi.shape[1]/2):
                print("right")
            
            elif (int((x1+x2)/2)) <  int(roi.shape[1]/2):
                print("left")



    except Exception as e:
        print(e)

    cv2.imshow("roi",roi)
    cv2.imshow("gray",gray)
    cv2.imshow("src",frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break