import cv2
import numpy as np

url = r"D:\Hawon\A_Study\VScode\Project\PythonProject\pythonAutoCar\resource\Video\test1.mp4"
cap = cv2.VideoCapture(url)
while True:
    ret,src = cap.read()
    src = cv2.cvtColor(src,cv2.COLOR_RGB2GRAY)
    src = cv2.resize(src,(720,480))
    src = cv2.GaussianBlur(src,(5,5),0)
    cv2.imshow("source",src)
    cv2.imshow("canny",cv2.Canny(src,230,230,None,3))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break