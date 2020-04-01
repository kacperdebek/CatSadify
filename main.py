import cv2
import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.resize(550, 500)
        self.setImageToLabel('res/empty.png')
        self.title = 'CatSadify'
        self.width = 800
        self.height = 600
        self.currentFile = 'res/empty.png'
        self.cat_cascade = cv2.CascadeClassifier('res/haarcascade_frontalcatface.xml')
        self.cat_ext_cascade = cv2.CascadeClassifier('res/haarcascade_frontalcatface_extended.xml')
        self.scale_factor = 1.05  # try different values of scale factor like 1.05, 1.3, etc
        self.neighbours = 3  # try different values of minimum neighbours like 3,4,5,6
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(56, 56, 61, 127))
        self.setPalette(palette)

        gridLayout = QGridLayout()

        loadButton = QPushButton("Load image")
        loadButton.clicked.connect(lambda: self.openImage())

        processButton = QPushButton("Find face")
        processButton.clicked.connect(lambda: self.processImage('res', self.currentFile))

        gridLayout.addWidget(self.label, 0, 0)
        gridLayout.addWidget(loadButton, 1, 0, 1, 1, Qt.AlignCenter)
        gridLayout.addWidget(processButton, 1, 1, 1, 1, Qt.AlignCenter)
        gridLayout.addWidget(QLabel("test"), 0, 1, Qt.AlignCenter)
        self.setLayout(gridLayout)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.drawRect(10, 10, 552, 502)

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        self.currentFile = os.path.basename(imagePath)
        self.setImageToLabel(imagePath)

    def setImageToLabel(self, imagePath):
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap.scaled(self.label.size(), QtCore.Qt.IgnoreAspectRatio))

    def setImageToLabelFromImage(self, image):
        image = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label.setPixmap(pixmap.scaled(self.label.size(), QtCore.Qt.IgnoreAspectRatio))

    def processImage(self, image_dir, image_filename):
        img = cv2.imread(image_dir + '/' + image_filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cats = self.cat_cascade.detectMultiScale(gray, scaleFactor=self.scale_factor, minNeighbors=self.neighbours)
        cats_ext = self.cat_ext_cascade.detectMultiScale(gray, scaleFactor=self.scale_factor,
                                                         minNeighbors=self.neighbours)
        for (x, y, w, h) in cats:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        for (x, y, w, h) in cats_ext:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.setImageToLabelFromImage(img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
