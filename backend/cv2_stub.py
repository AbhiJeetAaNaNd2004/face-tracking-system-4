# OpenCV stub for basic functionality
import numpy as np

# Mock VideoCapture class
class VideoCapture:
    def __init__(self, source=0):
        self.source = source
        self.isOpened = lambda: False
        
    def read(self):
        return False, np.zeros((480, 640, 3), dtype=np.uint8)
        
    def release(self):
        pass
        
    def get(self, prop):
        return 0
        
    def set(self, prop, value):
        return False

# Mock constants
CAP_PROP_FRAME_WIDTH = 3
CAP_PROP_FRAME_HEIGHT = 4
CAP_PROP_FPS = 5
COLOR_BGR2RGB = 4
IMREAD_COLOR = 1

# Mock functions
def cvtColor(img, code):
    return img

def imread(path, flags=IMREAD_COLOR):
    return np.zeros((480, 640, 3), dtype=np.uint8)

def imwrite(path, img):
    return True

def resize(img, size):
    return np.zeros((*size[::-1], 3), dtype=np.uint8)

def rectangle(img, pt1, pt2, color, thickness=1):
    return img

def putText(img, text, org, fontFace, fontScale, color, thickness=1):
    return img

def getTextSize(text, fontFace, fontScale, thickness):
    return ((len(text) * 10, 20), 5)

# Font constants
FONT_HERSHEY_SIMPLEX = 0