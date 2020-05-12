'''
Project Cartoony year 2020
this is gui code presenting project cartoony  
the gui contains four buttons for four algorithms used to cartoonize images and video (recodred or live)
the gui previews the output video or image and offers to save the output after viewing

Gui has three window view ,, main and image and video windows
'''

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QPalette
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QAction, QMenu, QFileDialog, QWidget, QLabel, QMessageBox, QErrorMessage
from PyQt5.QtWidgets import QDialog, QTabWidget, QSlider, QStyle
from PyQt5.QtCore import QRect, QSize, pyqtSignal, Qt, QThread, QUrl
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from CartoonyFunc import cartoonize_video, cartoonize_with_K_means, delete_output, cartoonize_live #functions implemented in cartoony.py
import sys
import time
from PyQt5.QtGui import QIcon, QPixmap

btn_enable=True
class Window(QMainWindow):
    # intializing main window components

    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)
        self.InitWindow()

    def InitWindow(self):
        global btn_enable
        self.setFixedSize(self.geometry().width(), self.geometry().height())

        # join buttons to functions
        self.VideoBtn1 = self.findChild(QPushButton, 'videobtn1')
        self.VideoBtn1.clicked.connect(self.VideoFn1)

        self.ImageBtn = self.findChild(QPushButton, "imagebtn")
        self.ImageBtn.clicked.connect(self.	ImageFn)

        self.VideoBtn2 = self.findChild(QPushButton, "videobtn2")
        self.VideoBtn2.clicked.connect(self. VideoFn2)

        self.Live = self.findChild(QPushButton, "livebtn")
        self.Live.clicked.connect(self. LiveStream)
        if btn_enable == False:
                self.VideoBtn1.setEnabled(True)
                self.VideoBtn2.setEnabled(True)
                self.ImageBtn.setEnabled(True)
                self.Live.setEnabled(True)
                btn_enable=True
        # start main window
        self.show()

    # video quality one button function
    def VideoFn1(self):
        global btn_enable
        self.statusBar().showMessage("processing your video....")
        # open new video
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:/', "Video files (*.mp4 *.m4p *.m4v *.avi *.wmv *.mov)")
        if fname[0]:
            if btn_enable == True:
                self.VideoBtn1.setEnabled(False)
                self.VideoBtn2.setEnabled(False)
                self.ImageBtn.setEnabled(False)
                self.Live.setEnabled(False)
                btn_enable=False

            self.VideoPath = fname[0]  # video path
            # print(self.VideoPath)
            # calling video quality one algorithm
            self.VideoPath = cartoonize_video(self.VideoPath,is_high=False)

            # switching to video dialog
            self.switch = VideoDialog(self.VideoPath)
            self.switch.show()
            self.close()

    # video quality two button function
    def VideoFn2(self):
        global btn_enable
        self.statusBar().showMessage("processing your video....")
        # open new video
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:/', "Video files (*.mp4)")
        if fname[0]:
            if btn_enable == True:
                self.VideoBtn1.setEnabled(False)
                self.VideoBtn2.setEnabled(False)
                self.ImageBtn.setEnabled(False)
                self.Live.setEnabled(False)
                btn_enable=False

            self.VideoPath = fname[0]  # video path
            # calling video quality two algorithm
            self.VideoPath = cartoonize_video(self.VideoPath,is_high=True)

            # switching to video dialog
            self.switch = VideoDialog(self.VideoPath)
            self.switch.show()
            self.close()

    # live stream button function
    def LiveStream(self):
        # calling Live stream algorithm
        cartoonize_live()

    # image button function
    def ImageFn(self):
        self.statusBar().showMessage("processing your image....")
        # open new video
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:/', "Image files (*.jpg *.gif *.jpeg *.png *.tiff *.jiff)")
        if fname[0]:
            self.imagePath = fname[0]  # image path
            # print(self.imagePath)
            self.imagePath = cartoonize_with_K_means(self.imagePath)  # calling image algorithm

            # switching to image dialog
            self.switch = ImageDialog(self.imagePath)
            self.switch.show()
            self.close()


class VideoDialog(QDialog):
    # intializing video dialog components
    def __init__(self, address):
        super(VideoDialog, self).__init__()
        uic.loadUi("video.ui", self)
        self.InitVideo(address)

    def InitVideo(self, address):
        self.setFixedSize(self.geometry().width(), self.geometry().height())
        self.filename = address
        self.removed = False

        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # create videowidget object
        videowidget = QVideoWidget()

        # join buttons to functions
        self.BackBtn = self.findChild(QPushButton, 'backbtn')
        self.BackBtn.clicked.connect(self.BackFn)

        self.SaveBtn = self.findChild(QPushButton, 'vidSave')
        self.SaveBtn.clicked.connect(self.SaveFn)

        # create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        hboxLayout2 = QHBoxLayout()
        hboxLayout2.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout2.addWidget(self.BackBtn)
        hboxLayout2.setSpacing(250)
        hboxLayout2.addWidget(self.vidlabel)
        hboxLayout2.addStretch(1)

        hboxLayout3 = QHBoxLayout()
        hboxLayout3.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout3.addStretch(1)
        hboxLayout3.addWidget(self.hintvideo2)
        hboxLayout3.addWidget(self.hintvideo)
        hboxLayout3.setSpacing(250)
        hboxLayout3.addWidget(self.SaveBtn)

        vboxLayout2 = QVBoxLayout()
        vboxLayout2.addLayout(hboxLayout2)
        vboxLayout2.setContentsMargins(0, 0, 0, 0)
        vboxLayout2.setAlignment(Qt.AlignTop)

        # create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addLayout(vboxLayout2)
        # vboxLayout.addStretch(1)
        vboxLayout.addWidget(videowidget)
        # vboxLayout.addStretch(1)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addLayout(hboxLayout3)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)

        # media player signals
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        if self.filename != '':
            # print(self.filename)
            self.mediaPlayer.setMedia(QMediaContent(
                QUrl.fromLocalFile(self.filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())

    def BackFn(self):
        # returns to main window
        self.cams = Window()
        self.cams.show()
        self.close()

    def SaveFn(self):
        # saves the video and delete the intermediate outputs
        self.Savefname = QFileDialog.getSaveFileName(self, 'Open file', 'c:/',
                                                     "Video files (*.mp4 *.m4p *.m4v *.avi *.wmv *.mov)")

        if self.Savefname[0]:
            self.mediaPlayer.setMedia(QMediaContent())
            delete_output(True, False, self.Savefname[0])
            self.removed = True

    def closeEvent(self, event):
        #deletes intermediate outputs
        if self.removed == False:
            self.mediaPlayer.setMedia(QMediaContent())
            #print("output delete")
            delete_output()


class ImageDialog(QDialog):
    # intializing image dialog components
    def __init__(self, address):
        super(ImageDialog, self).__init__()
        uic.loadUi("image.ui", self)
        # self.value = value
        self.InitImage(address)

    def InitImage(self, address):
        self.setFixedSize(self.geometry().width(), self.geometry().height())

        # join buttons to functions
        self.BackBtn = self.findChild(QPushButton, 'backbtn')
        self.BackBtn.clicked.connect(self.BackFn)

        self.SaveBtn = self.findChild(QPushButton, 'imSave')
        self.SaveBtn.clicked.connect(self.SaveFn)

        self.ImagePath = address
        self.removed = False

        pixmap = QPixmap(self.ImagePath)
        pixmap2 = pixmap.scaled(
            self.imview.width(), self.imview.height(), QtCore.Qt.KeepAspectRatio)
        self.imview.setPixmap(QPixmap(pixmap2)) # show output image 

    def BackFn(self):
        # switching back to main window
        self.cams = Window()
        self.cams.show()
        self.close()

    def SaveFn(self):
        # saves the image and delete the intermediate outputs
        self.Savefname = QFileDialog.getSaveFileName(self, 'Open file', 'c:/',
                                                     "Image files (*.jpg *.gif *.jpeg *.png *.tiff *.jiff)")
        delete_output(True, True, self.Savefname[0])
        self.removed = True

    def closeEvent(self, event):
        # deletes intermediate outputs
        if self.removed == False:
            delete_output(im=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()
