import cv2
import time

video = cv2.VideoCapture(r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Video\drive1.mp4")	

prev_time = 0
FPS = 1

while True:

    ret, frame = video.read()
    
    current_time = time.time() - prev_time

    if (ret is True) and (current_time > 1./ FPS) :
    	
        prev_time = time.time()
        
        cv2.imshow('VideoCapture', frame)
    	
        if cv2.waitKey(1) > 0 :
            
            break