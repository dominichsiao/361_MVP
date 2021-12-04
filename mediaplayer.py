from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QFileInfo, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,QPushButton, QShortcut, QSizePolicy, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
import sys
import visualizer

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("VisualSIMP") 
        self.visual = visualizer.AduioVisualizer()

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        #Create Play button
        self.playButton = QPushButton()
        #self.playButton.setEnabled(False)
        self.playButton.setToolTip("Play/Pause Media. Press spacebar to toggle as well.")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play) #trigger play/pause toggle when clicked
        

        #Use Space to play/pause media
        self.playbackToggle = QShortcut(QKeySequence(' '), self)
        self.playbackToggle.activated.connect(self.play)


        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

       
        # Create open file action
        openAction = QAction('&Open File', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a media file')
        openAction.triggered.connect(self.openFile)

        # Create exit program action
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add file open/ exit actions
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)


        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        

        #create program layout
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.error.connect(self.handleError)






    def openFile(self):
        
        global filePath
        global filename
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Media File",
                QDir.homePath())

        if filePath != '':
            #print(filePath)
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(filePath)))
            filename = QFileInfo(filePath).fileName()
            

            
            #Check file extension. Want to show generic "music-y" image when playing audio file.
            #if filename.lower().endswith(audioFileTypes):
             #   print("File is an audio file.")

            self.enableButtons()
           #self.setWindowTitle("SIMP: Now Playing " + filename)
            print(filename)
            #visual = visualizer.AduioVisualizer()
            self.play(self.visual.click(filename))
            #self.visual.click(filename)
    


    def enableButtons(self):
        self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.visual.set_False()
        else:
            self.mediaPlayer.play()
            self.visual.set_True()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(300,300)
    player.show()
    player.openFile()
    sys.exit(app.exec_())