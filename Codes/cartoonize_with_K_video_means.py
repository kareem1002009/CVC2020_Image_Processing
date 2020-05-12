def cartoonize_with_K_video_means(frame):
    bi = frame
    #Use bilateral Filter to smooths flat regions while keeping edges sharp 
    for i in range(5):
        bi = cv2.bilateralFilter(bi, d=5, sigmaColor=9, sigmaSpace=7)  # bilateral filter
    
    #img_edge = cv2.Canny(bi, 100, 200)
    img_cartoon = np.array(bi)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) 
    img_blur = cv2.medianBlur(img_gray,3)  
    # detect Edges to use it later in finding contours
    img_edge = cv2.Canny(img_blur, 100, 200)

    x, y, c = img_cartoon.shape
    # Change photo to HSV
    img_cartoon = cv2.cvtColor(img_cartoon, cv2.COLOR_RGB2HSV)
    # Get Histogram for each channel on HSV
    histograms = []
    for i in range(c):
        if i == 0 :
          histograms.append(np.histogram(img_cartoon[:, :, i], bins=np.arange(256))[0])
        else :
          histograms.append(np.histogram(img_cartoon[:, :, i], bins=np.arange(200))[0])

    #Get the centroids of each group in each channel( one channel has a list of centroids )
    channel_cenroids = []
    for i in range(c) :
        channel_cenroids.append(K_means(histograms[i]))

    # Flatten the two dimension of each channel for the image and dims will be (width*height,3)
    img_cartoon = img_cartoon.reshape((-1, c))
    for i in range(c):
        #Get one of Channels of photo
        channel = img_cartoon[:, i]
        # Using broadcasting to subtract each pixel value (stored as colomn vector) from all centroids (stored as row vector)
        # and get index of minimum result to know each pixel value closest to which centroid and assign value of this cetroid to the pixel
        dum = np.abs(channel[:, np.newaxis] - channel_cenroids[i])
        index = np.argmin(dum, axis=1)
        img_cartoon[:, i] = channel_cenroids[i][index]
    # Rerturn Original shape of image
    img_cartoon = img_cartoon.reshape((x, y, c))
    #Return Image to RGB
    img_cartoon = cv2.cvtColor(img_cartoon, cv2.COLOR_HSV2RGB)
    #Get the contours and draw it on cartonized version
    contours, _ = cv2.findContours(img_edge,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img_cartoon, contours, -1, 0, thickness=1)
    
    
    return img_cartoon