import cv2
import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QFileDialog, QGroupBox, \
    QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.resize(550, 500)
        self.set_image_to_label('res/empty.png')
        self.title = 'CatSadify'
        self.width = 800
        self.height = 600
        self.current_file = 'res/empty.png'
        self.current_path = ''
        self.cat_cascade = cv2.CascadeClassifier('res/haarcascade_frontalcatface.xml')
        self.cat_ext_cascade = cv2.CascadeClassifier('res/haarcascade_frontalcatface_extended.xml')
        self.scale_factor = 1.05
        self.neighbours = 3
        self.rect_width = 0
        self.rect_height = 0
        self.rect_x = 0
        self.rect_y = 0
        self.slider_scale_factor = QSlider(Qt.Horizontal)
        self.slider_neighbours = QSlider(Qt.Horizontal)
        self.param_visibility = False
        self.groupbox = QGroupBox("Parameters")
        self.initUI()

    def initUI(self):
        # setup window
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setAutoFillBackground(True)

        # setup colors
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(56, 56, 61, 127))
        palette.setColor(self.foregroundRole(), QColor(255, 255, 255, 200))
        self.setPalette(palette)

        grid_layout = QGridLayout()

        # setup parameters box
        self.groupbox.setCheckable(False)
        vbox = QVBoxLayout()
        self.groupbox.setLayout(vbox)

        # setup slider for parameter 1
        vbox.addWidget(QLabel("Scale factor"))
        vbox.addWidget(self.slider_scale_factor)
        self.slider_scale_factor.setMinimum(105)
        self.slider_scale_factor.setMaximum(200)
        self.slider_scale_factor.setValue(150)
        self.slider_scale_factor.setTickInterval(10)

        # setup slider for parameter 2
        vbox.addWidget(QLabel("Neighbours"))
        vbox.addWidget(self.slider_neighbours)
        self.slider_neighbours.setMinimum(1)
        self.slider_neighbours.setMaximum(10)
        self.slider_neighbours.setValue(5)
        self.slider_neighbours.setTickInterval(9)

        # connect sliders to corresponding methods
        self.slider_scale_factor.valueChanged.connect(self.valuechange_scalefactor)
        self.slider_neighbours.valueChanged.connect(self.valuechange_neighbours)

        self.groupbox.setVisible(self.param_visibility)

        # button for loading images to GUI
        load_button = QPushButton("Load image")
        load_button.clicked.connect(lambda: self.openImage())

        # button for activating image processing
        process_button = QPushButton("Find face")
        process_button.clicked.connect(lambda: self.processImage(self.current_path))

        # sadify button
        sadify_button = QPushButton("SADIFY")
        sadify_button.clicked.connect(lambda: self.blend_images())

        # setting up elements on the layout
        grid_layout.addWidget(self.label, 0, 0)
        grid_layout.addWidget(load_button, 1, 0, 1, 1, Qt.AlignCenter)
        grid_layout.addWidget(process_button, 1, 1, 1, 1, Qt.AlignCenter)
        grid_layout.addWidget(sadify_button, 1, 2, 1, 1, Qt.AlignCenter)
        grid_layout.addWidget(self.groupbox, 0, 1, Qt.AlignCenter)

        self.setLayout(grid_layout)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.drawRect(10, 10, 552, 502)

    def openImage(self):
        image_path, _ = QFileDialog.getOpenFileName()
        if image_path == "":
            return
        self.current_file = os.path.basename(image_path)
        self.set_image_to_label(image_path)
        self.groupbox.setVisible(True)
        self.current_path = image_path

    def set_image_to_label(self, image_path):
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap.scaled(self.label.size(), QtCore.Qt.IgnoreAspectRatio))

    def setImageToLabelFromImage(self, image):
        image = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label.setPixmap(pixmap.scaled(self.label.size(), QtCore.Qt.IgnoreAspectRatio))

    def processImage(self, image_dir):
        if image_dir == '':
            return
        print("processing")
        img = cv2.imread(image_dir)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cats = self.cat_cascade.detectMultiScale(gray, scaleFactor=self.scale_factor, minNeighbors=self.neighbours)
        cats_ext = self.cat_ext_cascade.detectMultiScale(gray, scaleFactor=self.scale_factor,
                                                         minNeighbors=self.neighbours)
        for (x, y, w, h) in cats:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # for (x, y, w, h) in cats_ext:
        #     img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.rect_x = cats.item(0)
        self.rect_y = cats.item(1)
        self.rect_width = cats.item(2)
        self.rect_height = cats.item(3)

        self.setImageToLabelFromImage(img)

    def valuechange_scalefactor(self):
        value = self.slider_scale_factor.value() / 100
        print(value)
        self.scale_factor = value

    def valuechange_neighbours(self):
        value = self.slider_neighbours.value()
        print(value)
        self.neighbours = value

    def overlay_image_alpha(self, img, img_overlay, pos, alpha_mask):
        x, y = pos

        y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
        x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

        y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
        x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

        if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
            return

        channels = img.shape[2]

        alpha = alpha_mask[y1o:y2o, x1o:x2o]
        alpha_inv = 1.0 - alpha

        for c in range(channels):
            img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] +
                                    alpha_inv * img[y1:y2, x1:x2, c])
    def blend_images(self):
        img = cv2.imread(self.current_path)
        template = cv2.imread("res/templates/template.png", -1)
        template = cv2.resize(template, (self.rect_width, self.rect_height))
        self.overlay_image_alpha(img, template[:, :, 0:3], (self.rect_x, self.rect_y), template[:, :, 3] / 255.0)
        self.setImageToLabelFromImage(img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
