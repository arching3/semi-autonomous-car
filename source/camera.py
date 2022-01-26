import cv2
import os
import numpy as np

def img2yuv_and_split(img):
    y,u,v = cv2.split(cv2.cvtColor(img,cv2.COLOR_BGR2YUV))
    return (y,u,v)

def threshold(src,threshold,Max,Method):
    ret,threshold_img = cv2.threshold(src,threshold,Max,Method)
    return (ret,threshold_img)

#include GaussianBlur
def adaptive_threshold(img, MaxVal : float, ksize : tuple, sigMax : int):
    img = cv2.GaussianBlur(img,ksize=ksize,sigmaX=sigMax)
    img_th = cv2.adaptiveThreshold(
        img,
        maxValue=MaxVal,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )
    return img_th

def find_maxContours(target,contour_method,point_method):
    contours, _ = cv2.findContours(target, contour_method, point_method)
    try:
        maxC = []
        for i in contours:
            maxC.append(len(i))
        temp = max(maxC)
        maxC = contours[maxC.index(temp)]
        return (True,maxC)
    except:
        return (False,None)

def cal_hash(img):
    avg = img.mean()
    bin = 1 * (img > avg)
    return bin

def hamming_distance(target_hash,original_hash):
    target_hash = target_hash.reshape(1,-1)
    original_hash = original_hash.reshape(1,-1)
    print(type(target_hash),type(original_hash))
    distance = (original_hash != target_hash)
    print(distance)
    return distance


path = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Image\sign"

img_name = os.listdir(path=path)

hash_val_original = []

try:
    for i in img_name:
        url = path + "\\" +  i

        src = cv2.imread(url)
        brightness,_,v = cv2.split(cv2.cvtColor(src,cv2.COLOR_BGR2YUV))

        _,th = cv2.threshold(v,220,250,cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   


        maxC = []
        for i in contours:
            maxC.append(len(i))
        temp = max(maxC)
        maxC = contours[maxC.index(temp)]

        ((x,y,w,h),((zx,zy),raduis)) = (cv2.boundingRect(maxC),cv2.minEnclosingCircle(maxC))


        cv2.circle(src,(int(zx),int(zy)),int(raduis),(0,0,255),2)
        src = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
        roi = src[y:y+h, x:x+w]
        roi = cv2.resize(roi,(64,64))

        """
        _, roi_th = cv2.threshold(roi, 160, 255, cv2.THRESH_BINARY)

        img_blurred = cv2.GaussianBlur(roi_th, ksize=(5, 5), sigmaX=0)
        img_blur_thresh = cv2.adaptiveThreshold(
            img_blurred,
            maxValue=255.0,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY_INV,
            blockSize=19,
            C=9
        )
        img_blur_thresh = cv2.resize(img_blur_thresh,(64,64))
        """

        avg = roi.mean()
        bin = 1 * (roi > avg)
        hash_val_original.append(bin)
    print(hash_val_original)
    os.system("pause")

except:
    pass

#hash_value
#img_name


streamServer = r"http://192.168.43.31:81/stream"
cap = cv2.VideoCapture(streamServer)
img_blur_thresh = np.zeros_like(cap.read()[1])




while True:
    _, src = cap.read()

    src = cv2.rotate(src,cv2.ROTATE_180)
    src = cv2.resize(src,(400,296))
    brightness, _, v = img2yuv_and_split(src)
    src = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

    _,th = threshold(v,190,255,cv2.THRESH_BINARY)

    ret, max_contours = find_maxContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if ret == True:

        ((x,y,w,h),((zx,zy),raduis)) = (cv2.boundingRect(max_contours),cv2.minEnclosingCircle(max_contours))

        cv2.circle(src,(int(zx),int(zy)),int(raduis),(0,0,255),2)

        roi = src[y:y+h, x:x+w]
        roi = cv2.resize(src,(64,64))



    elif ret == False:
        print("Cannot Find Contours")
        pass


    cv2.imshow("src",src)
    try:
        cv2.imshow("www",roi)
    except:
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break