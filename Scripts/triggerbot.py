from threading import Thread

from pynput import mouse
import cv2
import numpy as np
from mss import mss
from PIL import Image
import pyautogui
import keyboard
import time

scoped = False
alreadyScoped = False

def standby(real_img):
	global scoped
	global alreadyScoped

	# print("Scoped value: ", scoped)
	if (scoped):
		print("1")
		if (real_img[250,250][0] == 201 and real_img[250,250][1] == 40 and real_img[250,250][2] == 40):
			if not alreadyScoped:
				print("2")
				time.sleep(0.2)
			print("3")
			pyautogui.click()
		alreadyScoped = True
	else:
		alreadyScoped = False


def nothing(x):
	pass

def color_aimbot():

	mon = {'top': 200, 'left': 550, 'width': 500, 'height': 500}
	sct = mss()

	while True:
		last_time=time.time()
		lower_range = np.array([145, 160, 150])
		upper_range = np.array([150, 190, 255])

		sct.get_pixels(mon)
		img = Image.frombytes('RGB', (sct.width, sct.height), sct.image) # RGB image
		hsv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV) # HSV image
		mask = cv2.inRange(hsv, lower_range, upper_range) # B/W mask of image (RGB? BGR? GRAYSCALE?)
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
		else:
			scoped = False	

	with mouse.Listener(on_click=on_click) as listener:
		listener.join()	
			


Thread(target = color_aimbot).start()
Thread(target = mouse_listener).start()