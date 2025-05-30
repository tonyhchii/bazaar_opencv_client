import cv2 as cv
import threading
import time
from windowcapture import WindowCapture
from hsv_gui import HSV_Gui
from canny_gui import Canny_Gui
from hsvfilter import HsvFilter

class App:
    def __init__(self):
        self.hsv_gui = HSV_Gui()
        self.canny_gui = Canny_Gui()
        self.hsv_gui.init_control_gui()
        self.canny_gui.init_control_gui()
        self.hsv_filter = HsvFilter(12,99,61,25,168,162,0,0,0,0)
        self.cap = WindowCapture("The Bazaar")
        self.frame = None
        self.running = True

    def capture_loop(self):
        while self.running:
            self.frame = self.cap.quartz_screenshot()
            time.sleep(0.02)  # Reduce CPU usage

    def main_loop(self):
        while self.running:
            if self.frame is not None:
                filtered = self.hsv_gui.apply_hsv_filter(self.frame, hsv_filter=self.hsv_filter)
                cannyFilter = self.canny_gui.apply_canny_filter(filtered)
                #cv.imshow("HSV_FILTER", filtered)
                cv.imshow("CANNY_FILTER", cannyFilter)
            if cv.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break
        cv.destroyAllWindows()

    def run(self):
        capture_thread = threading.Thread(target=self.capture_loop, daemon=True)
        capture_thread.start()
        self.main_loop()

if __name__ == "__main__":
    app = App()
    app.run()
