def cartoonize_video_frame(frame):
    #first operation we do on the frame is that we appy on it bilateral filter to smooth flat regions without affecting edges 
    bi = cv2.bilateralFilter(frame, d=11, sigmaColor=50,sigmaSpace=50) 
    #then we get the gray image to get the edges easier 
    img_gray = cv2.cvtColor(bi, cv2.COLOR_RGB2GRAY)
    #applying blur to the image 
    img_blur = cv2.medianBlur(img_gray, 7)  # blur filter
    # detect edges
    img_edge = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=7, C=4)
    # cv2.imshow("edge1",img_edge)
    #we tried different edge detection algorithm (canny) but found the previous edges better
    ''' edge detection by canny
    img_edge = cv2.Canny(img_blur, 100, 200)
    img_edge=255-img_edge
    cv2.imshow("edge2",img_edge)'''
    #return the image to its original color
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    # to mix the edges with the photo we use bitwise_and
    img_cartoon = cv2.bitwise_and(frame, img_edge)
    return img_cartoon