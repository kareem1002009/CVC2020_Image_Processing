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