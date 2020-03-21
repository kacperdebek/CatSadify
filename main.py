import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.resize(550, 500)
        self.setImageToLabel('res/empty.png')
        self.title = 'CatSadify'
        self.width = 800
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(56, 56, 61, 127))
        self.setPalette(palette)

        gridLayout = QGridLayout()

        loadButton = QPushButton("Load image");
        loadButton.clicked.connect(lambda: self.openImage())

        gridLayout.addWidget(self.label, 0, 0)
        gridLayout.addWidget(loadButton, 1, 0, 1, 1, Qt.AlignCenter)
        gridLayout.addWidget(QLabel("test"), 0, 1, Qt.AlignCenter)
        self.setLayout(gridLayout)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.drawRect(10, 10, 552, 502)

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        self.setImageToLabel(imagePath)

    def setImageToLabel(self, imagePath):
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap.scaled(self.label.size(), QtCore.Qt.IgnoreAspectRatio))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
