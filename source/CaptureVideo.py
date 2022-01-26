import numpy as np
import cv2
import os

os.chdir(r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Video")
cap = cv2.VideoCapture("http://192.168.137.158:81/stream")


width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # 또는 cap.get(3)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # 또는 cap.get(4)
fps = cap.get(cv2.CAP_PROP_FPS) # 또는 cap.get(5)
fourcc = cv2.VideoWriter_fourcc(*'DIVX') # 코덱 정의
out = cv2.VideoWriter('OVVideo.avi', fourcc, fps, (int(width), int(height)))

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret == False:
        break
    
    cv2.imshow('frame',frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()