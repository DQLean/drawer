import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import keyboard
import pyautogui
from imager import load_image, read_image, resize_image_if_needed, get_contour_image, show_image, create_white_image
from drawer import draw_action

window_width = 800
window_height = 600

class MainWindow(QMainWindow):
    def add_config_stroke_delay_input(self):
        # stroke delay
        self.stroke_delay_input_layout = QHBoxLayout()
        self.config_layout.addLayout(self.stroke_delay_input_layout)

        self.stroke_delay_label = QLabel("Stroke Delay (ms): ")
        self.stroke_delay_input_layout.addWidget(self.stroke_delay_label)

        self.stroke_delay_input = QLineEdit()
        self.stroke_delay_input.setText("10") 
        self.stroke_delay_input_layout.addWidget(self.stroke_delay_input)
    def get_config_stroke_delay(self):
        val = self.stroke_delay_input.text()
        if val == "":
            return 10
        return int(val)

    def add_config_threshold1_input(self):
        # threshold1
        self.threshold1_input_layout = QHBoxLayout()
        self.config_layout.addLayout(self.threshold1_input_layout)

        self.threshold1_label = QLabel("Threshold1: ")
        self.threshold1_input_layout.addWidget(self.threshold1_label)

        self.threshold1_input = QLineEdit()
        self.threshold1_input.setText("30")
        self.threshold1_input_layout.addWidget(self.threshold1_input)
    def get_config_threshold1(self):
        val = self.threshold1_input.text()
        if val == "":
            return 30
        return int(val)

    def add_config_threshold2_input(self):
        # threshold2
        self.threshold2_input_layout = QHBoxLayout()
        self.config_layout.addLayout(self.threshold2_input_layout)

        self.threshold2_label = QLabel("Threshold2: ")
        self.threshold2_input_layout.addWidget(self.threshold2_label)

        self.threshold2_input = QLineEdit()
        self.threshold2_input.setText("100")
        self.threshold2_input_layout.addWidget(self.threshold2_input)
    def get_config_threshold2(self):
        val = self.threshold2_input.text()
        if val == "":
            return 100
        return int(val)

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

        self.user_in_layout = QHBoxLayout()
        self.layout.addLayout(self.user_in_layout)

        self.btn_layout = QVBoxLayout()
        self.user_in_layout.addLayout(self.btn_layout)

        self.btn_open = QPushButton("Open Image")
        self.btn_open.clicked.connect(lambda: self.open_image())
        self.btn_layout.addWidget(self.btn_open)

        self.btn_start_drawing = QPushButton("Start Drawing Listen (F2)")
        self.btn_start_drawing.setToolTip("Press F2 to start drawing after clicking this button, press ESC to stop drawing")
        self.btn_start_drawing.clicked.connect(lambda: self.start_drawing())
        self.btn_layout.addWidget(self.btn_start_drawing)

        self.config_layout = QVBoxLayout()
        self.user_in_layout.addLayout(self.config_layout)

        self.add_config_stroke_delay_input()
        self.add_config_threshold1_input()
        self.add_config_threshold2_input()

        self.image = None
        self.points_sequence = None
        self.is_drawing = False

        self.__load_history__()

    def __load_history__(self):
        if os.path.exists("__origin.jpg"):
            self.open_image(file_path="__origin.jpg")

    def open_image(self, file_path = None):
        try: threshold1 = self.get_config_threshold1()
        except: QMessageBox.warning(self, "Warning", "Threshold1 must be an integer");return
        try: threshold2 = self.get_config_threshold2()
        except: QMessageBox.warning(self, "Warning", "Threshold2 must be an integer");return

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
                points_sequence = read_image(image=image, threshold1=threshold1, threshold2=threshold2)

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
        try: delay = self.get_config_stroke_delay()
        except: QMessageBox.warning(self, "Warning", "Stroke Delay must be an integer");return
        
        if self.points_sequence:
            print("start drawing action listen (F2)")
            keyboard.on_press_key('F2', self.start_drawing_action)
        else:
            QMessageBox.warning(self, "Warning", "No image is opened")
    def start_drawing_action(self, e):
        try: delay = self.get_config_stroke_delay()
        except: QMessageBox.warning(self, "Warning", "Stroke Delay must be an integer");return
        try:
            if self.is_drawing:
                return
            self.is_drawing = True
            screen_x, screen_y = pyautogui.size()
            screen_center_sequence = (screen_x / 2, screen_y / 2)
            zero_sequence = (round(screen_center_sequence[0]-self.image_size[1]/2), round(screen_center_sequence[1]-self.image_size[0]/2))
            print("zero_sequence: ", zero_sequence, "stroke delay: ", delay)
            draw_action(points_sequence=self.points_sequence, zero_sequence=zero_sequence, delay=delay/1000)
            self.is_drawing = False
        except Exception as e:
            self.is_drawing = False
            QMessageBox.warning(self, "Warning", str(e))

def GUI():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())