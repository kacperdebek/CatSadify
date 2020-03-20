import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor


class App(QWidget):

    def __init__(self):
        super().__init__()
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

        label = QLabel(self)
        label.resize(550, 500)
        pixmap = QPixmap('res/hurtingcat.jpg')
        label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.IgnoreAspectRatio))

        gridLayout.addWidget(label, 0, 0)
        gridLayout.addWidget(QPushButton("Load image"), 1, 0, 1, 1, Qt.AlignCenter)
        gridLayout.addWidget(QLabel("test"), 0, 1, Qt.AlignCenter)

        self.setLayout(gridLayout)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.drawRect(10, 10, 552, 502)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
