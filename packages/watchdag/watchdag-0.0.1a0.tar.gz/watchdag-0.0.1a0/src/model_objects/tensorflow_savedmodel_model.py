import tensorflow as tf
import numpy as np

from base_model import BaseModel

from test import randomly_construct_tf_model

tf_dtype_to_np_dtype = {
    tf.float16: np.float16,
    tf.float32: np.float32,
    tf.float64: np.float64,
    tf.int8: np.int8,
    tf.int16: np.int16,
    tf.int32: np.int32,
    tf.int64: np.int64,
    tf.uint8: np.uint8,
    tf.uint16: np.uint16,
    tf.uint32: np.uint32,
    tf.uint64: np.uint64,
}

class TensorflowSavedModel(BaseModel):
    """Tensorflow Saved Model object.

    Args:
        BaseModel (BaseModel): The base model object.
    """
    def __init__(self, config: dict, model, input_shapes: dict, output_shapes: dict):
        """ Initialize a tensorflow saved model object.

        Args:
            config: A dictionary containing the model configuration.
            model: The model object.
            input_shapes: A dictionary containing the input shapes and types of the model.
            output_shapes: A dictionary containing the output shapes and types of the model.
        """
        
        super().__init__(config, model, "Tensorflow-SavedModel", input_shapes, output_shapes)
    
    @classmethod
    def init(cls, config: dict, model) -> 'TensorflowSavedModel':
        """ A constructor-like function to init a tensorflow saved model object.

        Args:
            config: A dictionary containing the model configuration.
            model: The model object.
            input_shapes_and_types: A dictionary containing the input shapes and types of the model.
            output_shapes_and_types: A dictionary containing the output shapes and types of the model.
        """
        
        # since it is a tensorflow saved model, we can get the input and output shapes and types from the model object
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
                        
        for signature in model.signatures.values():
            input_shapes = signature.structured_input_signature
            output_shapes = signature.structured_outputs
            break
                    
        input_shapes = get_dict(input_shapes)
        output_shapes = get_dict(output_shapes)
            
        input_specs = []
        output_specs = []
        
        for key in input_shapes:
            value = input_shapes.get(key)
            input_specs.append({
                'name': key,
                'shape': value.shape.as_list(),
                'dtype': tf_dtype_to_np_dtype[value.dtype]
            })
        
        for key in output_shapes:
            value = output_shapes.get(key)
            output_specs.append({
                'name': key,
                'shape': value.shape.as_list(),
                'dtype': tf_dtype_to_np_dtype[value.dtype]
            })
            
        return cls(config, model, input_specs, output_specs)
    
if __name__ == "__main__":
    model, input_shapes, output_shapes = randomly_construct_tf_model()
    model = tf.saved_model.save(model, "./saved_model")
    model = tf.saved_model.load("./saved_model")
    model = TensorflowSavedModel.init({}, model)
    print(model.input_shapes)
    print(model.output_shapes)