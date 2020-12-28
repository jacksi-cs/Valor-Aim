import serial
from pynput import mouse
import time

ser = serial.Serial('COM5', 9600)

def on_click(x,y,button,pressed):
	if (button == mouse.Button.left and pressed):
		global start
		start = time.perf_counter()
		print("Pressed")
		#ser.write('p'.encode())

	if (button == mouse.Button.left and not pressed):
		end = time.perf_counter()
		print("Released")
		#ser.write('r'.encode())
		print(end-start)

with mouse.Listener(on_click=on_click) as listener:
	listener.join()

		