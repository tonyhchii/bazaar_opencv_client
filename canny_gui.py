import cv2 as cv
import numpy as np
from cannysettings import CannySettings

class Canny_Gui:
    TRACKBAR_WINDOW = "Canny Trackbars"

    def apply_canny_filter(self,original_image, canny_settings=None):
        if not canny_settings:
            canny_settings = self.get_canny_settings_from_controls()
        gray = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (canny_settings.blur_kernel_size, canny_settings.blur_kernel_size), canny_settings.gaussian_sigma)
        canny = cv.Canny(blurred, canny_settings.low_threshold, canny_settings.high_threshold)

        return canny

    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 600, 300)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        cv.createTrackbar('BKSize', self.TRACKBAR_WINDOW, 0, 5, nothing)
        cv.createTrackbar('GSig', self.TRACKBAR_WINDOW, 0, 100, nothing)
        cv.createTrackbar('CLow', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('CHigh', self.TRACKBAR_WINDOW, 0, 255, nothing)


        cv.setTrackbarPos('CHigh', self.TRACKBAR_WINDOW, 150)
        cv.setTrackbarPos('BKSize', self.TRACKBAR_WINDOW, 2)

    def get_canny_settings_from_controls(self):
        canny_settings = CannySettings()
        canny_settings.blur_kernel_size = cv.getTrackbarPos('BKSize', self.TRACKBAR_WINDOW) * 2 + 1
        canny_settings.gaussian_sigma = cv.getTrackbarPos('GSig', self.TRACKBAR_WINDOW)/50
        canny_settings.low_threshold = cv.getTrackbarPos('CLow', self.TRACKBAR_WINDOW)
        canny_settings.high_threshold = cv.getTrackbarPos('CHigh', self.TRACKBAR_WINDOW)

        return canny_settings