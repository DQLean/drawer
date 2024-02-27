import pyautogui
import time
import keyboard

def draw_action(points_sequence, zero_sequence=(0, 0), duration = 0, delay=0.0001):
    zero_x, zero_y = zero_sequence
    if zero_x is None:
        zero_x = 0
    if zero_y is None:
        zero_y = 0

    is_mouse_down = False
    
    for strokes in points_sequence:
        for point in strokes:
            if keyboard.is_pressed('esc'):
                pyautogui.mouseUp()
                print("draw action is interrupted by esc key press")
                return
            
            target_x = zero_x + point[0]
            target_y = zero_y + point[1]
            
            pyautogui.moveTo(target_x, target_y, duration=duration)
            if not is_mouse_down:
                pyautogui.mouseDown()
                print("mouse down")
            is_mouse_down = True
            # time.sleep(delay)
        pyautogui.mouseUp()
        print("mouse up")
        is_mouse_down = False