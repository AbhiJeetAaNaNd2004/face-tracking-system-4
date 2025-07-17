import unittest
import numpy as np
import cv2
from src.face_detector import FaceDetector

class TestFaceDetector(unittest.TestCase):
    def test_detect_faces_returns_list_of_tuples(self):
        """
        Test that detect_faces returns a list of tuples (the coordinates).
        We will use a real image for this test.
        """
        # Create a simple test image: a black square with a white rectangle inside
        # This gives the cascade classifier something to potentially detect.
        test_image = np.zeros((200, 200, 3), dtype=np.uint8)
        cv2.rectangle(test_image, (50, 50), (150, 150), (255, 255, 255), -1)

        # Initialize the detector
        detector = FaceDetector(cascade_file_path='data/haarcascade_frontalface_default.xml', scale_factor=1.1)

        # Detect faces
        faces = detector.detect_faces(test_image)

        # Check that the output is a list
        self.assertIsInstance(faces, list)

        # If any "faces" were detected, check if they are tuples of 4 integers
        if faces:
            for face in faces:
                self.assertIsInstance(face, tuple)
                self.assertEqual(len(face), 4)
                self.assertTrue(all(isinstance(i, int) for i in face))
