import pyautogui
import time
import keyboard
from pynput.mouse import Controller, Button

def draw_action(points_sequence, zero_sequence=(0, 0), delay=0.01):
    zero_x, zero_y = zero_sequence
    if zero_x is None:
        zero_x = 0
    if zero_y is None:
        zero_y = 0

    is_mouse_down = False
    
    mouse = Controller()
    for strokes in points_sequence:
        for point in strokes:
            if keyboard.is_pressed('esc'):
                mouse.release(Button.left)
                print("draw action is interrupted by esc key press")
                return
            
            target_x = zero_x + point[0]
            target_y = zero_y + point[1]

            mouse.position = (target_x, target_y)
            if not is_mouse_down:
                mouse.press(Button.left)
                print("mouse down")
            time.sleep(delay)
            is_mouse_down = True
        
        mouse.release(Button.left)
        print("mouse up")
        is_mouse_down = False