import cv2

templit_path = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Image\sign\50.jpg"
templit = cv2.imread(templit_path)
templit = cv2.resize(templit,(100,100))
print(templit.shape)
t_red = cv2.cvtColor(templit,cv2.COLOR_BGR2GRAY)

streamServer = r"http://192.168.43.31:81/stream"
cap = cv2.VideoCapture(streamServer)

while True:
    _, src = cap.read()

    src = cv2.rotate(src,cv2.ROTATE_180)
    src = cv2.resize(src,(400,296))

    s_red = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(s_red,t_red,cv2.TM_CCORR_NORMED)

    min,max,mil,mal = cv2.minMaxLoc(result)

    x,y = mil
    h,w,_ = templit.shape
    
    cv2.rectangle(src,(x,y),(x+w,y+h),(0,0,255),2)
    roi = src[y:y+h,x:x+w]

    cv2.imshow("src",src)
    cv2.imshow("roi",roi)
    cv2.imshow("t",t_red)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
