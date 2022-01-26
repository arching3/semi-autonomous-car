from xml.etree import ElementTree
import cv2
import os
from xml.etree.ElementTree import Element, ElementTree

def list2str(target_list : list):

    result_str = ""
    for two_dimention in target_list:
        temp_str = ""
        for one_dimention in two_dimention:
            temp_str += str(one_dimention)
        print(two_dimention)
        print(temp_str)
        result_str += temp_str + "\n"
    return result_str


def indent(elem, level=0): #자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

path = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\Image\sign"

img_name = os.listdir(path=path)

hash_value = []

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

        roi = brightness[y:y+h, x:x+w]

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

        avg = img_blur_thresh.mean()
        bin = 1 * (img_blur_thresh > avg)
        hash_value.append(bin)
except:
    pass

xml_path = r"D:\Hawon\A_Study\VScode\pythonAutoCar\resource\image_hash_value.xml"


root = Element("img_mean_hash_value")

for i in range(0,len(img_name)):
    img_node = Element("img", name=img_name[i])
    root.append(img_node)

    hash_node = Element("hash", length=str(len(hash_value[i])))
    string = list2str(hash_value[i])
    hash_node.text = string
    img_node.append(hash_node)

indent(root)
tree = ElementTree(root)
tree.write(xml_path)