import cv2

class FaceDetector:
    def __init__(self, cascade_file_path, scale_factor):
        self.cascade = cv2.CascadeClassifier(cascade_file_path)
        self.scale_factor = scale_factor

    def detect_faces(self, image):
        """
        Detects faces in an image and returns their coordinates.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,  # Use the configured scale factor
            minNeighbors=5,
            minSize=(30, 30)
        )
        # Return the raw coordinates, do not draw on the image here
        return [tuple(f) for f in faces]
