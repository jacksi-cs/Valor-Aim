import serial
from pynput import mouse

ser = serial.Serial('COM5', 9600)

def on_click(x,y,button,pressed):
	if (button == mouse.Button.left and pressed):
		ser.write('r'.encode())

with mouse.Listener(on_click=on_click) as listener:
	listener.join()

		