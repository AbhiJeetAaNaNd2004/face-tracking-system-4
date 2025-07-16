# PyTorch stub for basic functionality
import numpy as np

class Tensor:
    def __init__(self, data):
        self.data = np.array(data)
        
    def numpy(self):
        return self.data
        
    def cuda(self):
        return self
        
    def cpu(self):
        return self
        
    def detach(self):
        return self

def tensor(data):
    return Tensor(data)

def zeros(*shape):
    return Tensor(np.zeros(shape))

def ones(*shape):
    return Tensor(np.ones(shape))

def device(device_type):
    return device_type

def load(path, map_location=None):
    return {}

def save(obj, path):
    pass

def no_grad():
    class NoGrad:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
    return NoGrad()

# Mock cuda module
class cuda:
    @staticmethod
    def is_available():
        return False

# Mock nn module
class nn:
    class Module:
        def __init__(self):
            pass
        def eval(self):
            return self
        def __call__(self, *args, **kwargs):
            return tensor([])
    
    class Linear(Module):
        def __init__(self, in_features, out_features):
            super().__init__()
            self.in_features = in_features
            self.out_features = out_features

# Mock transforms module
class transforms:
    class Compose:
        def __init__(self, transforms):
            self.transforms = transforms
        def __call__(self, x):
            return x
    
    class Normalize:
        def __init__(self, mean, std):
            self.mean = mean
            self.std = std
        def __call__(self, x):
            return x
    
    class ToTensor:
        def __call__(self, x):
            return tensor(x)