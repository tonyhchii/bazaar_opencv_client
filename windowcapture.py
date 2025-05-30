import cv2 as cv
import numpy as np
import os
from time import time
import Quartz
from CoreServices import LaunchServices


class WindowCapture:

    #Properties
    x = 0
    y = 0
    w = 0
    h = 0
    cropped_x = 0
    cropped_y = 0
    window_id = None


    def __init__(self, window_title=None):
        if window_title:
            self.window_id = self._get_window_id_by_title(window_title)
            self.bounds = self._get_window_bounds(self.window_id)
            if self.bounds:
                self.x = self.bounds['X']
                self.y = self.bounds['Y']
                self.w = self.bounds['Width']
                self.h = self.bounds['Height']

    def _get_window_bounds(self, window_id):
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
        self.bounds = self._get_window_bounds(self.window_id)
        if self.bounds is None:
            raise Exception("Cannot find window")

        self.x = self.bounds['X']
        self.y = self.bounds['Y']
        self.w = self.bounds['Width']
        self.h = self.bounds['Height']


        border_pixels = 8
        titlebar_pixels = 30

        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels
        
        rect = Quartz.CGRectMake(self.x + self.cropped_x, self.y + self.cropped_y, self.w, self.h)
            
        image_ref = Quartz.CGWindowListCreateImage(
            rect,
            Quartz.kCGWindowListOptionIncludingWindow,
            self.window_id,
            Quartz.kCGWindowImageDefault
        )

        if image_ref is None:
            raise Exception("Failed to capture image")


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



    def _get_window_id_by_title(self, title):
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID
        )

        for window in windows:
            window_name = window.get('kCGWindowName', '')
            if window_name and title.lower() in window_name.lower():
                return window['kCGWindowNumber']
        return None
    
    @staticmethod
    def list_all_windows():
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionAll, 
            Quartz.kCGNullWindowID
        )

        for window in windows:
            window_id = window.get('kCGWindowNumber', 'N/A')
            owner_name = window.get('kCGWindowOwnerName', 'Unknown App')
            window_title = window.get('kCGWindowName', '')

            if window_title:  # Only show windows with a visible title
                print(f"ID: {window_id}, App: {owner_name}, Title: '{window_title}'")