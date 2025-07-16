# Faiss stub for basic functionality
import numpy as np

class IndexFlatL2:
    def __init__(self, d):
        self.d = d
        self.ntotal = 0
        self.vectors = []
        
    def add(self, vectors):
        self.vectors.extend(vectors)
        self.ntotal += len(vectors)
        
    def search(self, query_vectors, k):
        # Return empty results
        n_queries = len(query_vectors)
        distances = np.full((n_queries, k), float('inf'))
        indices = np.full((n_queries, k), -1, dtype=np.int64)
        return distances, indices
        
    def reset(self):
        self.vectors = []
        self.ntotal = 0

def IndexFlatIP(d):
    return IndexFlatL2(d)

def normalize_L2(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)