import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import time
import numpy as np
import pyautogui
from imager import load_image, read_image, resize_image_if_needed, get_contour_image, show_image, create_white_image
from drawer import draw_action

window_width = 800
window_height = 600

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drawer")

        screen_x, screen_y = pyautogui.size()
        self.setGeometry(screen_x / 2 - window_width / 2, screen_y / 2 - window_height / 2, window_width, window_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_layout = QHBoxLayout()
        self.layout.addLayout(self.image_layout)

        self.label_image = QLabel()
        self.image_layout.addWidget(self.label_image)

        self.label_contour = QLabel()
        self.image_layout.addWidget(self.label_contour)

        self.btn_open = QPushButton("Open Image")
        self.btn_open.clicked.connect(lambda: self.open_image())
        self.layout.addWidget(self.btn_open)

        self.btn_start_drawing = QPushButton("Start Drawing")
        self.btn_start_drawing.clicked.connect(lambda: self.start_drawing())
        self.layout.addWidget(self.btn_start_drawing)

        self.image = None
        self.points_sequence = None

        self.__load_history__()

    def __load_history__(self):
        if os.path.exists("__origin.jpg"):
            self.open_image(file_path="__origin.jpg")

    def open_image(self, file_path = None):
        if file_path is None:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image files (*.jpg *.jpeg *.png *.bmp)")
            file_path = file_path.encode('utf-8').decode(sys.getfilesystemencoding())
        if file_path:
            print("load image: ", file_path)
            try:
                image = load_image(image_path=file_path)
                self.image_size = (image.shape[1], image.shape[0])
                # resize the image by the screen size if needed
                image = resize_image_if_needed(image=image)
                cv2.imwrite("__origin.jpg", image)
                points_sequence = read_image(image=image)

                # save the image to a temporary file
                contours = create_white_image(image.shape[1], image.shape[0])
                contours = get_contour_image(image=contours, points_sequence=points_sequence)
                cv2.imwrite("__contour.jpg", contours)
                q_img = QImage("__contour.jpg")
                pixmap = QPixmap.fromImage(q_img)
                self.label_contour.clear()
                self.label_contour.setAlignment(Qt.AlignCenter)
                self.label_contour.setPixmap(pixmap)

                # get the Contour blending original image
                image = get_contour_image(image=image, points_sequence=points_sequence)

                self.points_sequence = points_sequence

                # save the image to a temporary file
                cv2.imwrite("__mix.jpg", image)
                q_img = QImage("__mix.jpg")
                pixmap = QPixmap.fromImage(q_img)
                self.label_image.clear()
                self.label_image.setAlignment(Qt.AlignCenter)
                self.label_image.setPixmap(pixmap)

                print(points_sequence)
            except Exception as e:
                QMessageBox.warning(self, "Warning", str(e))

    def start_drawing(self):
        if self.points_sequence:
            time.sleep(3)
            try:
                screen_x, screen_y = pyautogui.size()
                screen_center_sequence = (screen_x / 2, screen_y / 2)
                zero_sequence = (round(screen_center_sequence[0]-self.image_size[1]/2), round(screen_center_sequence[1]-self.image_size[0]/2))
                print("zero_sequence: ", zero_sequence)
                draw_action(self.points_sequence, zero_sequence=zero_sequence)
            except Exception as e:
                QMessageBox.warning(self, "Warning", str(e))
        else:
            QMessageBox.warning(self, "Warning", "No image is opened")

def GUI():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())