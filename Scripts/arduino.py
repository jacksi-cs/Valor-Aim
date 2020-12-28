import serial
import time
import struct

ser = serial.Serial('COM5', 9600, timeout=5)
# time.sleep(5);

while True:
    print("serial write!\n")
    ser.write(struct.pack('b', -127))
    time.sleep(1)
    print(ser.read())
    print(ser.read())