# InsightFace stub for basic functionality
import numpy as np
import sys

class FaceAnalysis:
    def __init__(self, name='buffalo_l', providers=['CPUExecutionProvider']):
        self.name = name
        self.providers = providers
        
    def prepare(self, ctx_id=0, det_size=(640, 640)):
        pass
        
    def get(self, img):
        # Return empty list of faces
        return []
        
    def draw_on(self, img, faces):
        return img

class Face:
    def __init__(self):
        self.bbox = np.array([0, 0, 100, 100])
        self.kps = np.zeros((5, 2))
        self.det_score = 0.0
        self.embedding = np.zeros(512)
        
    def __getitem__(self, key):
        return getattr(self, key)

# Create app module structure
class AppModule:
    FaceAnalysis = FaceAnalysis

# Create the module structure
app_module = AppModule()
sys.modules['insightface.app'] = app_module