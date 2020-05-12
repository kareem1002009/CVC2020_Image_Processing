import numpy as np
import cv2
import os
import time
from moviepy.editor import *
from collections import defaultdict
from scipy import stats

#global variables to be accessed by all functions
final_output_path = ''
output_video = ''
img_cartoon = ''
output_file = ''

#This function is for cartoonization of the video frames
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

#this function get path of the desired video to be cartoonized,and apply on it cartoonize_video_frame() on every frame to get the final output
def cartoonize_video(path,is_high=False):
    global final_output_path, output_video, output_file
    # code for video
    #start_time = time.time()
    #Get the input video through VideoFileClip
    input_video = VideoFileClip(path)
    #Extract the audio file from this video to write it with the modified video
    audio_file = input_video.audio
    #we create output_file first to put in it the video with the modification but without audio in the file named output
    #this file is just temporary, we will remove it in the end
    output_file = os.getcwd() + "/output.mp4"
    # Checks and deletes the output file
    if os.path.isfile(output_file):
        os.remove(output_file)
    # Getting the frames from the video
    cap = cv2.VideoCapture(path)
    
    # Get current width of frame
    frame_width = int(cap.get(3))
    #print(frame_width)
    # Get current height of frame
    frame_height = int(cap.get(4))
    #print(frame_height)
    #get the frame per second for every video
    fps = cap.get(cv2.CAP_PROP_FPS)
    #print(fps)
    # Define the codec and create VideoWriter object
    #Another formats for foucc MJPG, DIVX, XVID
    #we define fourcc with mp4v for mp4 videos
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #we start creating the output_video,using its path,fourcc for encoding the video, frame per second, the width & height
    out = cv2.VideoWriter(output_file, fourcc, fps,(frame_width, frame_height))
    while(cap.isOpened()):
        #read frame by frame
        ret, frame = cap.read()
        if ret == True:
            # cartoon the frame
            #if you want the video with better quality
            if is_high:
                cartoon=cartoonize_with_K_video_means(frame)
            else:            
                cartoon = cartoonize_video_frame(frame)
            #if is_high
            #write cartoonized frame to video
            out.write(cartoon)
            # cv2.imshow('frame',cartoon)
        else:
            break
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    # When everything done, release the capture
    cap.release()
    out.release()
    #Create the final output video by reading the cartoonized video 
    output_video = VideoFileClip(output_file)
    #then add the audio file from the original video
    output_video.audio = audio_file
    #we get the name of video in file_name
    file_name = (path.split('/'))[-1]
    #then we get the extension to make the output video the same extension and to its name _cartoon
    tmp = os.path.splitext(file_name)
    name = tmp[0] + "_cartoon" + tmp[1]
    name = os.path.join(os.getcwd(), name)
    final_output_path = name
    #then we write the final video to the same path where the program run
    output_video.write_videofile(final_output_path)
    #print("Execution Time = %s second " % (time.time() - start_time))
    return final_output_path


def cartoonize_live():
    global final_output_path, output_video, output_file
    # Capturing video from webcam:
    cap = cv2.VideoCapture(0)
   
    while(True):
        #read frame by frame
        ret, frame = cap.read()
        if ret == True:
        
            # cartoon the frame
            #cartoon = cartoonize_video_frame(frame)
            cartoon = cartoonize_with_K_video_means(frame)

            cv2.imshow('Live Stream (press Esc to close)',cartoon)
        else:
            break
#to close the live press Esc
        k = cv2.waitKey(5) & 0xFF
        if k == 27 :
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
   
    return 0


#this function is for deleting the outputs if the user doesn't want to save it, or if he wants to save it in specific place with specific name 
def delete_output(save_new=False, im=False, path=None):
    global final_output_path, output_video, img_cartoon, output_file
    #for saving the video
    if save_new == True and im == False:
        output_video.write_videofile(path)
        #remove the file with video without audio
        os.remove(output_file)
    #for saving the image
    elif save_new == True and im == True:
        cv2.imwrite(path, img_cartoon)
    #to delete file with video without audio
    elif save_new == False and im == False:
        os.remove(output_file)
    #remove the final_video in the old path 
    os.remove(final_output_path)



def cartoonize_with_K_means(path):
    global final_output_path,img_cartoon
    frame = cv2.imread(path)
    #frame = path
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
    
    #Pass photoes to GUI
    file_name = (path.split('/'))[-1]
    tmp = os.path.splitext(file_name)
    name = tmp[0] + "_cartoon" + tmp[1]
    name = os.path.join(os.getcwd(), name)
    final_output_path = name
    cv2.imwrite(final_output_path, img_cartoon)
    return final_output_path


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




def K_means(hist,No_of_groups=10) :
    # Initialize Cetroids by dividing the range of histogram to equal size Clusters
    step = int(len(hist)/No_of_groups)
    dum = [i for i in range(0,len(hist)+1,step)]
    old_centroids = np.array(dum)
    new_centroids= np.zeros_like(old_centroids)
   
    while True :
        clusters = defaultdict(list)
        #Construct dictionary contains the Clusters by subtract each histogram value from all centroids and get index of 
        # minimum result to know each histogram value closest to each cluster and append it to the list of this cluster
        for i in range(len(hist)) :
            if hist[i] == 0:
                continue
            dis = np.abs(old_centroids-i)
            index = np.argmin(dis)
            clusters[index].append(i)

        #Calculate New Centroids by making a weighted average for each cluster 
        for i,ind in clusters.items(): 
            if np.sum(hist[ind]) == 0:
                continue
            new_centroids[i] = int(np.sum(ind*hist[ind])/np.sum(hist[ind]))
        #Break if we saturated and new_centroids eqls old_centroids
        if np.array(new_centroids-old_centroids).any() == False :
            break ;
        old_centroids = new_centroids
    return new_centroids


def cartoonize_image(path):
    global img_cartoon, final_output_path
    frame = cv2.imread(path)
    k = 25
    im2 = (frame / k)
    im2 = im2.astype(np.uint8)
    im2 = im2 * k
    bi = im2
    #cv2.imshow("Image", bi)
    for i in range(5):
        bi = cv2.bilateralFilter(
            bi, d=11, sigmaColor=9, sigmaSpace=7)  # bilateral filter

    #cv2.imshow("Image", bi)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # gray aaki
    #cv2.imshow("Image", img_gray)
    img_blur = cv2.medianBlur(img_gray, 7)  # blur filter
    #cv2.imshow("Image", img_blur)
    # detect and enhance edges
    img_edge = cv2.adaptiveThreshold(
        img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=7, C=4)
    # convert back to color, bit-AND with color image
    #cv2.imshow("Image", img_edge)
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    #cv2.imshow("Image", img_edge)
    kernel_bta3na = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    img_edge = cv2.dilate(img_edge, kernel_bta3na, iterations=1)
    size_img_edge = img_edge.shape
    print(size_img_edge)
    print(img_blur.shape)
    print(frame.shape)
    # cv2.resize(img_blur,)
    img_cartoon = cv2.bitwise_and(bi, img_edge)
    file_name = (path.split('/'))[-1]
    tmp = os.path.splitext(file_name)
    name = tmp[0] + "_cartoon" + tmp[1]
    name = os.path.join(os.getcwd(), name)
    # name=file_name.split('.')
    final_output_path = name
    print(final_output_path)
    cv2.imwrite(final_output_path, img_cartoon)
    #cv2.imshow("Image", img_cartoon)
    # img_cartoon = cv2.bilateralFilter(img_cartoon, d=11, sigmaColor=9, sigmaSpace=5)  # bilateral filter
    #cv2.imshow("Image", img_cartoon)
    #img_cartoon = cv2.erode(img_cartoon, kernel_bta3na, iterations=1)

    return final_output_path
