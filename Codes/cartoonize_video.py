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