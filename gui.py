import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import pyautogui
from imager import load_image, read_image, resize_image_if_needed, get_contour_image, show_image
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

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.btn_open = QPushButton("Open Image")
        self.btn_open.clicked.connect(self.open_image)
        self.layout.addWidget(self.btn_open)

        self.btn_start_drawing = QPushButton("Start Drawing")
        self.btn_start_drawing.clicked.connect(self.start_drawing)
        self.layout.addWidget(self.btn_start_drawing)

        self.image = None
        self.points_sequence = None

    def open_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image files (*.jpg *.jpeg *.png *.bmp)")
        if file_path:
            image = load_image(image_path=file_path)
            # resize the image by the screen size if needed
            image = resize_image_if_needed(image=image)
            points_sequence = read_image(image=image)
            image = get_contour_image(image=image, points_sequence=points_sequence)

            self.points_sequence = points_sequence
            self.image = image

            # save the image to a temporary file
            cv2.imwrite("temp.jpg", image)

            q_img = QImage("temp.jpg")
            pixmap = QPixmap.fromImage(q_img)
            self.label.clear()
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setPixmap(pixmap)
            print(points_sequence)

    def start_drawing(self):
        if self.points_sequence:
            draw_action(self.points_sequence)
        else:
            QMessageBox.warning(self, "Warning", "No image is opened")

def GUI():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())