import tensorflow as tf
from get_type import *
import numpy as np
import torch

def get_input_shape(obj):
    """ Get the model input tensor shape.

    Args:
        obj: The model object.
        We assume the model object is either a tensorflow, tensorflow-lite or pytorch model.
    """

    model_type = get_model_type(obj)

    if model_type == "tensorflow":
        return obj.get_layer(index = 0).input_shape
    elif model_type == "tensorflow-lite":
        return obj.get_input_details()[0]["shape"]
    elif model_type == "pytorch":
        pass