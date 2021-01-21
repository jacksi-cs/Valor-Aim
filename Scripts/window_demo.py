import cv2
import numpy as np
from mss import mss  # pip install mss==2.0.22
from PIL import Image # pip install Pillow

def nothing(x):
    pass

mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
sct = mss()

cv2.namedWindow("Trackbars")
cv2.createTrackbar("Height", "Trackbars", 127, 1080, nothing)
cv2.createTrackbar("Length", "Trackbars", 127, 1920, nothing)
cv2.createTrackbar("Y Offset pos", "Trackbars", 0, 500, nothing)
cv2.createTrackbar("X Offset pos", "Trackbars", 0, 500, nothing)
cv2.createTrackbar("Y Offset neg", "Trackbars", 0, 500, nothing)
cv2.createTrackbar("X Offset neg", "Trackbars", 0, 500, nothing)

while True:
    detect_height = cv2.getTrackbarPos("Height", "Trackbars")
    detect_width = cv2.getTrackbarPos("Length", "Trackbars")
    offset_y = cv2.getTrackbarPos("Y Offset pos", "Trackbars") - cv2.getTrackbarPos("Y Offset neg", "Trackbars")
    offset_x = cv2.getTrackbarPos("X Offset pos", "Trackbars") - cv2.getTrackbarPos("X Offset neg", "Trackbars")

    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image) # RGB image
    real_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) # BGR image	

    x1 = (1920-detect_width)/2
    y1 = (1080-detect_height)/2
    x2 = (1920+detect_width)/2
    y2 = (1080+detect_height)/2
    start_point = (int(x1 + offset_x), int(y1 + offset_y))
    end_point = (int(x2 + offset_x), int(y2 + offset_y))
    color = (255,0,0)
    thickness = 2
    cv2.rectangle(real_img, start_point, end_point, color, thickness)

    frame = np.array(real_img)
    cv2.imshow("Window", real_img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break