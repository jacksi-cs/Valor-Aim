import cv2
import numpy as np
from mss import mss
from PIL import Image
import time

def nothing(x):
    pass

mon = {'top': 290, 'left': 710, 'width': 500, 'height': 500}
sct = mss()

cv2.namedWindow("Trackbars")
cv2.createTrackbar("LOWER H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("LOWER S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LOWER V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("UPPER H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("UPPER S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("UPPER V", "Trackbars", 0, 255, nothing)

while True:
    l_h = cv2.getTrackbarPos("LOWER H", "Trackbars")
    l_s = cv2.getTrackbarPos("LOWER S", "Trackbars")
    l_v = cv2.getTrackbarPos("LOWER V", "Trackbars")
    u_h = cv2.getTrackbarPos("UPPER H", "Trackbars")
    u_s = cv2.getTrackbarPos("UPPER S", "Trackbars")
    u_v = cv2.getTrackbarPos("UPPER V", "Trackbars")
    
    lower_range = np.array([200,50,200])
    upper_range = np.array([300,150,300])
    #lower_range = np.array([l_h, l_s, l_v])
    #upper_range = np.array([u_h, u_s, u_v])
    #lower_range = np.array([159,104,127])
    #upper_range = np.array([179,255,255])
    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image) # RGB image
    #hsv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV) # HSV image
    #mask = cv2.inRange(hsv, lower_range, upper_range) # B/W mask of image (RGB? BGR? GRAYSCALE?)
    mask = cv2.inRange(np.array(img), lower_range, upper_range) # using a mask with RGB rather than HSV (seems to work better)
    real_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) # BGR image	
    res = cv2.bitwise_and(real_img, real_img, mask= mask) # BGR and mask put together

    pixels = np.nonzero(mask) # Tuple of arrays containing coordinates of white pixels

    sum0 = sum(pixels[0])
    len0 = len(pixels[0])
    sum1 = sum(pixels[1])
    len1 = len(pixels[1])

    if sum0 != 0 or len0 != 0 or sum1 != 0 or len1 != 0:
        minval = min(pixels[0]) # highest point on the y axis (should be the head)
        min1 = int(round(pixels[0][0])) # minimum value in the array (highest point on the y axis <head>)
        min2 = int(round(pixels[1][0])) # the x coordinate of the lowest y value
        cv2.circle(real_img, (min2, min1+5), 5, (0,255,255), -1)

    frame = np.array(real_img)
    #cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("frame1", mask)
    cv2.imshow("frame2", real_img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
	    cv2.destroyAllWindows()
	    break