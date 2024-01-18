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
        input_specs = []
        output_specs = []
        
        def format_shape(shape_list):
            for i in range(len(shape_list)):
                if shape_list[i] == -1:
                    shape_list[i] = None
            return shape_list
        
        for value in model.get_input_details():
            input_specs.append({
                'name': value['name'],
                'index': value['index'],
                'shape': format_shape(list(value['shape_signature'])),
                'dtype': value['dtype'],
                'quantization_specs':{
                    'quantization': value['quantization'],
                    'quantization_parameters': value['quantization_parameters'],
                    'sparsity_parameters': value['sparsity_parameters'],
                }
            })
        
        for value in model.get_output_details():
            output_specs.append({
                'name': value['name'],
                'index': value['index'],
                'shape': format_shape(list(value['shape_signature'])),
                'dtype': value['dtype'],
                'quantization_specs':{
                    'quantization': value['quantization'],
                    'quantization_parameters': value['quantization_parameters'],
                    'sparsity_parameters': value['sparsity_parameters'],
                }
            })
            
        return cls(config, model, input_specs, output_specs)
    
if __name__ == "__main__":
    model, input_shapes, output_shapes = randomly_construct_tf_model()
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the model.
    with open('./model.tflite', 'wb') as f:
        f.write(tflite_model)

    # Load the TFLite model in TFLite Interpreter
    interpreter = tf.lite.Interpreter('./model.tflite')

    model = TensorflowSavedModel.init({}, interpreter)
    print(model.input_shapes)
    print(model.output_shapes)