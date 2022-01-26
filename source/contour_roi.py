import cv2

path = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Image\sign\20.jpg"
img = cv2.imread(path)
img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)

brightness, _, red = cv2.split(img_yuv)
ret,th = cv2.threshold(red,135,255,cv2.THRESH_BINARY_INV)
th = cv2.bitwise_not(th)

contours, hierarchy = cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


maxC = []


for i in contours:
    maxC.append(len(i))
temp = max(maxC)
maxC = contours[maxC.index(temp)]
((x,y,w,h),((zx,zy),raduis)) = (cv2.boundingRect(maxC),cv2.minEnclosingCircle(maxC))


roi = brightness[y:y+h, x:x+w]

_, roi_th = cv2.threshold(roi,30,255,cv2.THRESH_BINARY_INV)

img_blurred = cv2.GaussianBlur(roi_th, ksize=(5, 5), sigmaX=0)

img_blur_thresh = cv2.adaptiveThreshold(
    img_blurred,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
)
# img_blur_thresh =  cv2.bitwise_not(img_blur_thresh)



cv2.imshow("yuv",th)
cv2.imshow("original",img)
cv2.imshow("roi_th",roi_th)
cv2.imshow("roi_gg",img_blur_thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()