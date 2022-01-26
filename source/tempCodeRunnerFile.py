while True:
    _, frame = cap.read()


    frame = cv2.rotate(frame,cv2.ROTATE_180)
    frame = cv2.resize(frame,(400,296))
    show_frame = frame.copy()

    _, _ , red = Cov_BGR2YUV_and_split(frame)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)


    _, th = threshold(red,175,255)
    contours, _ = cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    
    try:
        contours = find_max_ct(contours) # Assigning maximum value of contours to variable

        (x,y,w,h) = cv2.boundingRect(contours) # Finding the largest rectangle

        th = frame[y:y+h, x:x+w] # ROI

        _, _, th = cv2.split(th) # HSV

        _, th = threshold(th, 70, 255,cv2.THRESH_BINARY_INV) # Binary


    except:
        print("Cannot find Contours")

    try:
        th_ct, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        th_ct = find_max_ct(th_ct)

        (cx,cy,cw,ch) = cv2.boundingRect(th_ct)
        ct_roi_o = th[cy:cy+ch,cx:cx+cw]


        dist = []
        for i in range(len(im_ct_list)):
            temp = cv2.matchShapes(th_ct,im_ct_list[i],cv2.CONTOURS_MATCH_I3,0)
            if temp < 0.2:
                print(temp)
            #dist.append(temp)

        # 30 50 70 90
        #print("detect : " + str(num_list[dist.index(min(dist))]) + str(min(dist)))