import cv2

class VideoCapture:
    def __init__(self, device_index):
        self.cap = cv2.VideoCapture(device_index)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()

    def read_frame(self):
        return self.cap.read()
