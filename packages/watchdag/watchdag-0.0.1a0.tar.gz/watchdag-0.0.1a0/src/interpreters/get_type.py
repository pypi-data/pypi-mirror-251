import tensorflow as tf
import numpy as np
import torch

def get_model_type(obj):
    """ Get the type of the model object.

    Args:
        obj: The model object.
        We assume the model object is either a tensorflow, tensorflow-lite or pytorch model.
    """
    
    if isinstance(obj, tf.keras.Model):
        return "tensorflow-keras"
    elif hasattr(obj, "signatures"):
        return "tensorflow"
    elif isinstance(obj, tf.lite.Interpreter):
        return "tensorflow-lite"
    elif isinstance(obj, torch.nn.Module):
        return "pytorch"
    else:
        raise TypeError("The model object is not a tensorflow, tensorflow-lite or pytorch model.")