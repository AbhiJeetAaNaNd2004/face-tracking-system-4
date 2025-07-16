#!/usr/bin/env python3
"""
Script to patch imports in files that use cv2 and face_recognition
"""

import sys
import os

# Add cv2 and face_recognition stubs to sys.modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our stubs
import cv2_stub as cv2
import face_recognition_stub as face_recognition
import faiss_stub as faiss
import torch_stub as torch
import insightface_stub as insightface
import bytetracker_stub as bytetracker

# Add them to sys.modules so they can be imported
sys.modules['cv2'] = cv2
sys.modules['face_recognition'] = face_recognition
sys.modules['faiss'] = faiss
sys.modules['torch'] = torch
sys.modules['insightface'] = insightface
sys.modules['bytetracker'] = bytetracker

if __name__ == "__main__":
    print("Patched cv2 and face_recognition imports")
    print("cv2:", cv2)
    print("face_recognition:", face_recognition)