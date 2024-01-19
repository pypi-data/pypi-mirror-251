import numpy as np
import inspect
from functools import wraps

try:
    import torch
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
# unify function inputs     
def pytorch_precedence(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        params = sig.parameters
        is_numpy_present = 'is_numpy' in params
        if is_numpy_present and 'is_numpy' not in kwargs:
            kwargs['is_numpy'] = True
        if PYTORCH_AVAILABLE:
            args = list(args)
            gpu_device = next((arg.device for arg in args if isinstance(arg, torch.Tensor) and arg.is_cuda), None)
            is_tensor_present = any(isinstance(arg, torch.Tensor) for arg in args)
            if is_tensor_present:
                args = [torch.from_numpy(arg).to(gpu_device) if isinstance(arg, np.ndarray) else (arg.to(gpu_device) if gpu_device and isinstance(arg, torch.Tensor) else arg) for arg in args]
                kwargs = {k: torch.from_numpy(v).to(gpu_device) if isinstance(v, np.ndarray) else (v.to(gpu_device) if gpu_device and isinstance(v, torch.Tensor) else v) for k, v in kwargs.items()}
                if is_numpy_present:
                    kwargs['is_numpy'] = False
        return func(*args, **kwargs)
    return wrapper