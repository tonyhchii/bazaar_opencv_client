import cv2 as cv
import threading
import time
from windowcapture import WindowCapture
from hsv_gui import HSV_Gui

class App:
    def __init__(self):
        self.vision = HSV_Gui()
        self.vision.init_control_gui()
        self.cap = WindowCapture("Spotify")
        self.frame = None
        self.running = True

    def capture_loop(self):
        while self.running:
            self.frame = self.cap.quartz_screenshot()
            time.sleep(0.01)  # Reduce CPU usage

    def main_loop(self):
        while self.running:
            if self.frame is not None:
                filtered = self.vision.apply_hsv_filter(self.frame)
                cv.imshow("HSV_FILTER", filtered)
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
