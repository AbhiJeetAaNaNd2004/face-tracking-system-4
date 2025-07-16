# Face Recognition stub for basic functionality
import numpy as np

def face_locations(img, number_of_times_to_upsample=1, model="hog"):
    """Mock face locations function"""
    return []

def face_encodings(img, known_face_locations=None, num_jitters=1, model="small"):
    """Mock face encodings function"""
    return []

def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    """Mock face comparison function"""
    return [False] * len(known_face_encodings)

def face_distance(face_encodings, face_to_compare):
    """Mock face distance function"""
    return np.array([1.0] * len(face_encodings))

def load_image_file(file_path):
    """Mock image loading function"""
    return np.zeros((480, 640, 3), dtype=np.uint8)