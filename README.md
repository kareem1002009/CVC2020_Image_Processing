# CVC2020_Image_Processing
  This repo is for the image processing competition CVC20 ,where we will create application that converts photos,videos and live stream   with web camera to cartoonized version

  In the cartoonization process, an edge detection and bilateral filter are required. The bilateral filter is used to reduce the color     palette of an image. Afterward, we can apply edge detection to this image for generating a dark shaped image. Therefore, finally, some   tricks can apply for this image to get a cartoon image. 

## Modes Of Operation

### Cartoonize an image

### Cartoonize a video 
 #### two output qualities are available , with difference in execution time of each
  Low Quality: Code uses Bilateral filter and edge detection to Cartoonize within small execution time


  High Quality: Code uses the same code for low quality and additionally uses K-means clustering to reduce number of colors used to       produce a stronger cartoonization effect , but with more execution time

 ### Cartoonize Live video stream from your webcam




## samples

### Image

#### input


#### output


### Video
[[url to samples folder ]]
