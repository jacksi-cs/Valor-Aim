from threading import Thread

from pynput import mouse, keyboard
import cv2
import numpy as np
from mss import mss
from PIL import Image
import pyautogui
import time
from enum import Enum

class Border(Enum):
    RED = 1
    PURPLE = 2
    YELLOW = 3

scoped = False
alreadyScoped = False
scripts_on = False

# ** CUSTOM SETTINGS **
screen_width = 1920
screen_height = 1080
detect_width = 500
detect_height = 500
offset_x = 0
offset_y = 0
script_toggle = keyboard.Key.num_lock
border = Border.YELLOW

def standby(real_img):
	global scoped
	global alreadyScoped
	global scripts_on

	if (scoped and scripts_on):
		if (real_img[250,250][0] == 201 and real_img[250,250][1] == 40 and real_img[250,250][2] == 40):
			if not alreadyScoped:
				time.sleep(0.2)
			pyautogui.click()
		alreadyScoped = True
	else:
		alreadyScoped = False


def nothing(x):
	pass

def color_aimbot():
	global screen_width
	global screen_height
	global detect_width
	global detect_height
	global offset_x
	global offset_y
	global border

	if border == Border.RED:
		lower_range = np.array([200,50,50])
		upper_range = np.array([255,100,100])
	elif border == Border.PURPLE:
        # Ranges for RGB purple (source recommends 250,100,250 with 60 range)
		lower_range = np.array([200,50,200])
		upper_range = np.array([255,150,255])
	elif border == Border.YELLOW:
		lower_range = np.array([200,200,0])
		upper_range = np.array([255,255,60])

	mon = {'top': int((screen_height-offset_y-detect_height)/2), 'left': int((screen_width-offset_x-detect_width)/2), 'width': detect_width, 'height': detect_height}
	sct = mss()

	while True:
		last_time=time.time()

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
			minx = int(round(min(pixels[0])))
			maxx = int(round(max(pixels[0])))
			miny = int(round(min(pixels[1])))
			maxy = int(round(max(pixels[1]))) 
			real_img[minx:maxx, miny:maxy] = [201,40,40]

		standby(real_img)

		frame = np.array(real_img)
		cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.imshow("frame", frame)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

def mouse_listener():
	global scoped

	# Forces me to reclick right click after shooting rather than just holding down right click
	def on_click(x, y, button, pressed):
		if (button == mouse.Button.right and pressed):
			global scoped 
			scoped = True
			print(scoped)
		else:
			scoped = False	
			print(scoped)

	with mouse.Listener(on_click=on_click) as listener:
		listener.join()	

def scripts_switch():

    def on_press(key):
        global scripts_on
        global script_toggle
        global ser
        if key == script_toggle:
            scripts_on = not scripts_on

    with keyboard.Listener(
        on_press=on_press) as listener:
            listener.join()
			
Thread(target = color_aimbot).start()
Thread(target = mouse_listener).start()
Thread(target = scripts_switch).start()