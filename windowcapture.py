import cv2 as cv
import numpy as np
import os
from time import time
import Quartz
from CoreServices import LaunchServices

class WindowCapture:

    def __init__(self, window_title):
        self.window_id = self.get_window_id_by_title(window_title)

    def get_window_bounds(self, window_id):
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID
        )
        for w in windows:
            if w.get('kCGWindowNumber') == window_id:
                bounds = w.get('kCGWindowBounds')
                return bounds  # This is a dict with keys: X, Y, Width, Height
        return None

    def quartz_screenshot(self):
        # Capture the entire screen
        bounds = self.get_window_bounds(self.window_id)
        if bounds is None:
            raise Exception("Window ID not found or no bounds available")

        rect = Quartz.CGRectMake(bounds['X'], bounds['Y'], bounds['Width'], bounds['Height'])
            
        image_ref = Quartz.CGWindowListCreateImage(
            rect,
            Quartz.kCGWindowListOptionIncludingWindow,
            self.window_id,
            Quartz.kCGWindowImageDefault
        )

        width = Quartz.CGImageGetWidth(image_ref)
        height = Quartz.CGImageGetHeight(image_ref)
        bytes_per_row = Quartz.CGImageGetBytesPerRow(image_ref)

        data_provider = Quartz.CGImageGetDataProvider(image_ref)
        data = Quartz.CGDataProviderCopyData(data_provider)
        buffer = np.frombuffer(data, dtype=np.uint8)

        # Reshape buffer to (height, bytes_per_row // 4, 4) for RGBA channels
        img = buffer.reshape((height, bytes_per_row // 4, 4))

        # Crop to actual width, since bytes_per_row can be larger than width*4
        img = img[:, :width, :]

        img = img[:, :, :3]

        return img



    def get_window_id_by_title(self, title):
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID
        )

        for window in windows:
            window_name = window.get('kCGWindowName', '')
            if window_name and title.lower() in window_name.lower():
                return window['kCGWindowNumber']
        return None