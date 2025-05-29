import cv2 as cv
import numpy as np
import os
from windowcapture import WindowCapture


os.chdir(os.path.dirname(os.path.abspath(__file__)))

cap = WindowCapture('The Bazaar')

while True:
    screenshot = cap.quartz_screenshot()

    cv.imshow('Computer Vision', screenshot)

    if cv.waitKey(5) & 0xFF == ord('q'):
        break

    cv.destroyAllWindows()
