import pyautogui
import time
import keyboard

def draw_action(points_sequence, zero_sequence=(0, 0), duration = 0, delay=0.01):
    zero_x, zero_y = zero_sequence

    is_mouse_down = False
    
    for strokes in points_sequence:
        for point in strokes:
            if keyboard.is_pressed('esc'):
                return
            
            target_x = zero_x + point[0]
            target_y = zero_y + point[1]
            
            pyautogui.moveTo(target_x, target_y, duration=duration)
            if not is_mouse_down: pyautogui.mouseDown()
            is_mouse_down = True
            time.sleep(delay)
        pyautogui.mouseUp()
        is_mouse_down = False