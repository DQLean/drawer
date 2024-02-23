import cv2
import numpy as np
import pyautogui

def load_image(image_path: str) -> np.ndarray:
    return cv2.imread(image_path)

# Read the image and return the points sequence
def read_image(image: np.ndarray, threshold1 = 30, threshold2 = 100, apertureSize = 3, L2gradient = True) -> list:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, threshold1=threshold1, threshold2=threshold2, apertureSize=apertureSize, L2gradient=L2gradient)
    # Identify the contours in the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # sort
    sorted_contours = sorted(contours, key=lambda x: np.mean(x[:, :, 0]))

    points_sequence = []
    for contour in sorted_contours:
        strokes = []
        for point in contour:
            strokes.append(tuple(point[0]))
        points_sequence.append(strokes)

    return points_sequence

def resize_image_if_needed(image: np.ndarray, screen_width = None, screen_height = None) -> np.ndarray:
    if not screen_width or not screen_height:
        screen_width, screen_height = pyautogui.size()
    image_height, image_width = image.shape[:2]
    
    max_width = screen_width * 0.8
    max_height = screen_height * 0.8
    
    if image_width > max_width or image_height > max_height:
        scale = min(max_width / image_width, max_height / image_height)
        resized_image = cv2.resize(image, None, fx=scale, fy=scale)
        return resize_image_if_needed(resized_image)
    else:
        return image

# Show the image with the points
# duration: 0 means the image will be closed manually
# duration must be an integer
def show_image(image: np.ndarray, points_sequence: list, delay = 0):
    delay = round(delay)
    for strokes in points_sequence:
        for point in strokes:
            cv2.circle(image, point, 1, (0, 255, 0), -1)
            if delay >= 1:
                cv2.imshow('Contours', image)
                cv2.waitKey(delay)
    cv2.imshow('Contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_contour_image(image: np.ndarray, points_sequence: list):
    for strokes in points_sequence:
        for point in strokes:
            cv2.circle(image, point, 1, (0, 255, 0), -1)
    return image