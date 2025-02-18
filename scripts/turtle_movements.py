import time
from turtle_1 import walking_state_1, walking_state_2, walking_state_3, walking_state_4, stand
from rotate import rotate_state_1, rotate_state_2, rotate_state_3, rotate_state_4, rotate_state_5, rotate_state_6, rotate_state_7

current_state = "stop"

def move_forward():
    global current_state
    if current_state != "forward":
        print("Moving forward")
        current_state = "forward"
    walking_state_1()
    time.sleep(0.25)
    walking_state_2()
    time.sleep(0.25)
    walking_state_3()
    time.sleep(0.25)
    walking_state_4()
    time.sleep(0.25)

def move_backward():
    global current_state
    if current_state != "backward":
        print("Moving backward")
        current_state = "backward"
    walking_state_4()
    time.sleep(0.25)
    walking_state_3()
    time.sleep(0.25)
    walking_state_2()
    time.sleep(0.25)
    walking_state_1()
    time.sleep(0.25)

def rotate_clockwise():
    global current_state
    if current_state != "clockwise":
        print("Rotating clockwise")
        current_state = "clockwise"
    rotate_state_1()
    time.sleep(0.25)
    rotate_state_2()
    time.sleep(0.25)
    rotate_state_3()
    time.sleep(0.25)
    rotate_state_4()
    time.sleep(0.25)
    rotate_state_5()
    time.sleep(0.25)
    rotate_state_6()
    time.sleep(0.25)
    rotate_state_7()
    time.sleep(0.25)

def rotate_counterclockwise():
    global current_state
    if current_state != "counterclockwise":
        print("Rotating counter-clockwise")
        current_state = "counterclockwise"
    rotate_state_7()
    time.sleep(0.25)
    rotate_state_6()
    time.sleep(0.25)
    rotate_state_5()
    time.sleep(0.25)
    rotate_state_4()
    time.sleep(0.25)
    rotate_state_3()
    time.sleep(0.25)
    rotate_state_2()
    time.sleep(0.25)
    rotate_state_1()
    time.sleep(0.25)

def stop_movement():
    global current_state
    if current_state != "stop":
        print("Stopping")
        current_state = "stop"
        stand()
