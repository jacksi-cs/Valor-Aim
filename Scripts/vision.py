from threading import Thread
from pynput import keyboard

import cv2 # pip install opencv-python
import numpy as np
from mss import mss  # pip install mss==2.0.22
from PIL import Image # pip install Pillow
import time
import serial # pip install pyserial
import struct

# ** CUSTOM SETTINGS **
detect_width = 254
detect_height = 254

scripts_on = False

def smooth_move(var, x_or_y):
    return int(var - detect_width/2) if (x_or_y == 'x') else int(var - detect_height/2) 
    #return var - 127

def arduino_communication(x, y):
    global scripts_on
    ser = serial.Serial('COM5', 9600, write_timeout=5)

    if scripts_on:
        ser.write(struct.pack('h', smooth_move(y, 'y')))
        ser.write(struct.pack('h', smooth_move(x, 'x')))

# def nothing(x):
#     pass

def aimbot():
    # time.sleep(5)
    global detect_width
    global detect_height
    mon = {'top': int((1080-detect_height)/2), 'left': int((1920-detect_width)/2), 'width': detect_width, 'height': detect_height}
    #mon = {'top': 290, 'left': 710, 'width': 500, 'height': 500}
    #mon = {'top': 415, 'left': 835, 'width': 250, 'height': 250 }
    sct = mss()

    # Used for determining HSV values
    # cv2.namedWindow("Trackbars")
    # cv2.createTrackbar("LOWER H", "Trackbars", 0, 179, nothing)
    # cv2.createTrackbar("LOWER S", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("LOWER V", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("UPPER H", "Trackbars", 0, 179, nothing)
    # cv2.createTrackbar("UPPER S", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("UPPER V", "Trackbars", 0, 255, nothing)

    while True:
        # print("in while true")
        #while scripts_on:

        # l_h = cv2.getTrackbarPos("LOWER H", "Trackbars")
        # l_s = cv2.getTrackbarPos("LOWER S", "Trackbars")
        # l_v = cv2.getTrackbarPos("LOWER V", "Trackbars")
        # u_h = cv2.getTrackbarPos("UPPER H", "Trackbars")
        # u_s = cv2.getTrackbarPos("UPPER S", "Trackbars")
        # u_v = cv2.getTrackbarPos("UPPER V", "Trackbars")
        
        #Ranges for RGB purple (source recommends 250,100,250 with 60 range)
        lower_range = np.array([190,40,190])
        upper_range = np.array([310,160,310])

        # Ranges for using the trackbars
        # lower_range = np.array([l_h, l_s, l_v])
        # upper_range = np.array([u_h, u_s, u_v])

        # Ranges for HSV red
        # lower_range = np.array([159,104,127])
        # upper_range = np.array([179,255,255])

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
    # def on_click(x,y,button,pressed):
    #     global scripts_on
    #     if (button == mouse.Button.right and pressed):
    #         print(1234)
    #         scripts_on = True
    #     else:
    #         print(6543)
    #         scripts_on = False

    # with mouse.Listener(on_click=on_click) as listener:
    #     listener.join()
    def on_press(key):
        global scripts_on
        if key == keyboard.Key.caps_lock:
            print("asdf")
            scripts_on = not scripts_on
    
    # def on_release(key):
    #     global scripts_on
    #     if key == keyboard.Key.caps_lock:
    #         print("1234")
    #         scripts_on = False

    with keyboard.Listener(
        on_press=on_press) as listener:
            listener.join()


Thread(target = aimbot).start()
Thread(target = scripts_switch).start()