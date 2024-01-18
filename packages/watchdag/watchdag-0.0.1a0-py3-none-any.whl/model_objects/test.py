import tensorflow as tf
import numpy as np
import tf2onnx
import os, shutil

def randomly_construct_tf_model():
    """ 
    Randomly construct a tensorflow model object.
    This is done with keras.
    
    let's say inputs can be 2D, 3D or 4D tensors.
    if it is a 2D tensor, then it is a batch of 1D tensors. size: (batch_size, width)
    if it is a 3D tensor, then it is a batch of 2D tensors. size: (batch_size, width, height)
    if it is a 4D tensor, then it is a batch of 3D tensors. size: (batch_size, width, height, channels)
    let's assume batch size is always 1.
    """
    
    random_number_of_inputs = np.random.randint(1, 10)
    random_number_of_outputs = np.random.randint(1, 10)
    random_input_shapes = {}
    random_output_shapes = {}
    
    for i in range(random_number_of_inputs):
        random_number_of_dimensions = np.random.randint(2, 5)
        random_shape = [1]
        for j in range(random_number_of_dimensions):
            random_shape.append(np.random.randint(1, 10))
        random_shape = tuple(random_shape)
        random_input_shapes["input_" + str(i)] = random_shape
    
    for i in range(random_number_of_outputs):        
        random_number_of_dimensions = np.random.randint(2, 5)
        random_shape = [1]
        for j in range(random_number_of_dimensions):
            random_shape.append(np.random.randint(1, 10))
        random_shape = tuple(random_shape)
        random_output_shapes["output_" + str(i)] = random_shape
        
    # now we need to build a model that conforms to the input and output shapes
    # let's just do this for now:
    # model takes all input, flatten them, linear them all to a tensor with size [1, 42]
    # then this tensor is linear to all output.

    inputs = []
    for i in range(random_number_of_inputs):
        curr_input = tf.keras.Input(shape=random_input_shapes["input_" + str(i)])
        inputs.append(curr_input)
    flattened_inputs = []
    for i in range(random_number_of_inputs):
        curr_flattened_input = tf.keras.layers.Flatten()(inputs[i])
        flattened_inputs.append(curr_flattened_input)
    concatenated_inputs = tf.keras.layers.concatenate(flattened_inputs)
    linear_to_2 = tf.keras.layers.Dense(2)(concatenated_inputs)
    outputs = []
    for i in range(random_number_of_outputs):
        curr_output = tf.keras.layers.Dense(np.prod(random_output_shapes["output_" + str(i)]))(linear_to_2)
        curr_output = tf.keras.layers.Reshape(random_output_shapes["output_" + str(i)])(curr_output)
        outputs.append(curr_output)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs)

    return model, random_input_shapes, random_output_shapes

def randomly_construct_onnx_model():
    """
    Randomly construct an onnx model object.
    This function is converting a randomly constructed tensorflow model to onnx.
    """
    
    def get_dict(obj):
        if isinstance(obj, dict):
            return obj
        if isinstance(obj, tuple):
            for item in obj:
                if isinstance(item, dict):
                    return item
        if isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    return item
    
    input_signature = []
    model, tmp1, tmp2 = randomly_construct_tf_model()
    
    for key in tmp1:
        value = tmp1.get(key)
        value = list(value)
        value.insert(0, None)
        value = tuple(value)
        input_signature.append(tf.TensorSpec(value, tf.float32, name=key))
    
    onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature=input_signature, opset=13)
    return onnx_model, tmp1, tmp2

# model, _, _ = randomly_construct_tf_model()
model, _, _ = randomly_construct_onnx_model()