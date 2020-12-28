from threading import Thread
from pynput import keyboard

import cv2 # pip install opencv-python
import numpy as np
from mss import mss  # pip install mss==2.0.22
from PIL import Image # pip install Pillow
import time
import serial # pip install pyserial
import struct
from enum import Enum

class Border(Enum):
    RED = 1
    PURPLE = 2
    YELLOWD = 3
    YELLOWP = 4

# ** CUSTOM SETTINGS **
screen_width = 1600
screen_height = 900
detect_width = 127
detect_height = 127
offset_x = 0
offset_y = 0
script_toggle = keyboard.Key.caps_lock
border = Border.RED

scripts_on = False
ser = serial.Serial('COM5', 9600, write_timeout=5)



def smooth_move(var, x_or_y):
    global detect_width
    global detect_height
    global offset_x
    global offset_y
    return int(var - detect_width/2 - offset_x/2) if (x_or_y == 'x') else int(var - detect_height/2 - offset_y/2) 

def arduino_communication(x, y):
    global scripts_on
    global ser

    if scripts_on:
        ser.write(struct.pack('h', smooth_move(y, 'y')))
        ser.write(struct.pack('h', smooth_move(x, 'x')))

# def nothing(x):
#     pass

def aimbot():
    # time.sleep(5)
    global screen_width
    global screen_height
    global detect_width
    global detect_height
    global border
    mon = {'top': int((screen_height-offset_y-detect_height)/2), 'left': int((screen_width-offset_x-detect_width)/2), 'width': detect_width, 'height': detect_height}
    sct = mss()

    # Used for determining HSV values
    # cv2.namedWindow("Trackbars")
    # cv2.createTrackbar("LOWER H", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("LOWER S", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("LOWER V", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("UPPER H", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("UPPER S", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("UPPER V", "Trackbars", 0, 255, nothing)

    if border == Border.RED:
        lower_range = np.array([200,50,200])
        upper_range = np.array([300,150,300])
    elif border == Border.PURPLE:
        # Ranges for RGB purple (source recommends 250,100,250 with 60 range)
        lower_range = np.array([200,50,200])
        upper_range = np.array([300,150,300])
    elif border == Border.YELLOWD:
        lower_range = np.array([200,50,200])
        upper_range = np.array([300,150,300])
    elif border == Border.YELLOWP:
        lower_range = np.array([200,50,200])
        upper_range = np.array([300,150,300])

    while True:
        # l_h = cv2.getTrackbarPos("LOWER H", "Trackbars")
        # l_s = cv2.getTrackbarPos("LOWER S", "Trackbars")
        # l_v = cv2.getTrackbarPos("LOWER V", "Trackbars")
        # u_h = cv2.getTrackbarPos("UPPER H", "Trackbars")
        # u_s = cv2.getTrackbarPos("UPPER S", "Trackbars")
        # u_v = cv2.getTrackbarPos("UPPER V", "Trackbars")
        
        # Ranges for using the trackbars
        # lower_range = np.array([l_h, l_s, l_v])
        # upper_range = np.array([u_h, u_s, u_v])

        sct.get_pixels(mon)
        img = Image.frombytes('RGB', (sct.width, sct.height), sct.image) # RGB image
        # hsv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV) # HSV image
        # mask = cv2.inRange(hsv, lower_range, upper_range) # B/W mask of image (RGB? BGR? GRAYSCALE?)
        mask = cv2.inRange(np.array(img), lower_range, upper_range) # using a mask with RGB rather than HSV (seems to work better)
        real_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) # BGR image	
        res = cv2.bitwise_and(real_img, real_img, mask= mask) # BGR and mask put together

        pixels = np.nonzero(mask) # Tuple of arrays containing coordinates of white pixels

        sum0 = sum(pixels[0])
        len0 = len(pixels[0])
        sum1 = sum(pixels[1])
        len1 = len(pixels[1])

        if sum0 != 0 or len0 != 0 or sum1 != 0 or len1 != 0:
            min1 = int(round(pixels[0][0])) # minimum value in the array (highest point on the y axis <head>)
            min2 = int(round(pixels[1][0])) # the x coordinate of the lowest y value
            cv2.circle(real_img, (min2, min1+5), 5, (0,255,255), -1)
            arduino_communication(min2, min1+5)

        frame = np.array(real_img)
        # cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow("frame1", mask)
        cv2.imshow("frame2", real_img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def scripts_switch():

    def on_press(key):
        global scripts_on
        global script_toggle
        global ser
        if key == script_toggle:
            scripts_on = not scripts_on
            if scripts_on == False:
                ser.write(struct.pack('h', 9999))

            print(scripts_on)

    with keyboard.Listener(
        on_press=on_press) as listener:
            listener.join()


Thread(target = aimbot).start()
Thread(target = scripts_switch).start()