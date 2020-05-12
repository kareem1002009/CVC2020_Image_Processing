#Live cartoonization of video stream
#takes no arguments
#functions loops while stream is ON , and returns when Esc is pressed
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