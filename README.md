# CVC2020_Image_Processing
  This repo is for the image processing competition CVC20 ,where we will create application that converts photos,videos and live stream   with web camera to cartoonized version

  In the cartoonization process, an edge detection and bilateral filter are required. The bilateral filter is used to reduce the color     palette of an image. Afterward, we can apply edge detection to this image for generating a dark shaped image. Therefore, finally, some   tricks can apply for this image to get a cartoon image. 

## Link for exe:
https://drive.google.com/file/d/17ewSURCkm98JY4PnmG_rpIR4BHCau9Va/view?usp=sharing

## Modes Of Operation

### Cartoonize an image

### Cartoonize a video 
 #### two output qualities are available , with difference in execution time of each
  Low Quality: Code uses Bilateral filter and edge detection to Cartoonize within small execution time


  High Quality: Code uses the same code for low quality and additionally uses K-means clustering to reduce number of colors used to       produce a stronger cartoonization effect , but with more execution time

 ### Cartoonize Live video stream from your webcam


## Installation

### Steps to install

1. Clone the repository.
2. Download K-Codec pack media player
>https://codecguide.com/download_k-lite_codec_pack_full.htm
--
3. Install the required packages.
>pip install -r requirements.txt
---

## samples
### Image

#### input
![Sample1](https://github.com/kareem1002009/CVC2020_Image_Processing/blob/master/Samples/Images/sample2.jpg)
![Sample2](https://github.com/kareem1002009/CVC2020_Image_Processing/blob/master/Samples/Images/sample3.jpg)
![Sample3](https://github.com/kareem1002009/CVC2020_Image_Processing/blob/master/Samples/Images/sample4.jpg)


#### output

![Sample1](https://github.com/kareem1002009/CVC2020_Image_Processing/blob/master/Samples/Images/sample2_cartoon.jpg)
![Sample2](https://github.com/kareem1002009/CVC2020_Image_Processing/blob/master/Samples/Images/sample3_cartoon.jpg)
![Sample3](https://github.com/kareem1002009/CVC2020_Image_Processing/blob/master/Samples/Images/sample4_cartoon.jpg)




### Video
https://github.com/kareem1002009/CVC2020_Image_Processing/tree/master/Samples/Videos
