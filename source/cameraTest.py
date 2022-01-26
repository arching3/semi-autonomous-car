import cv2

url = r"http://192.168.43.31:81/stream"

cap = cv2.VideoCapture(url)

while True:
    ret, src = cap.read()
    rotation = cv2.rotate(src, cv2.ROTATE_180)
    B, _, _ = cv2.split(src)
    B = cv2.GaussianBlur(src, (5, 5), 1)

    cv2.imshow("B", B)
    cv2.imshow("src", src)
    cv2.imshow("rotation", rotation)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
