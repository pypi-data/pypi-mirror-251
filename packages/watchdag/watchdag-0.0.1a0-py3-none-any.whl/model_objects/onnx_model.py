import numpy as np
import os
import shutil
from base_model import BaseModel
import onnxruntime as ort
import onnx
from test import randomly_construct_onnx_model

onnx_dtype_to_np_dtype = {
    'tensor(float16)': np.float16,
    'tensor(float)': np.float32,
    'tensor(double)': np.float64,
    'tensor(int8)': np.int8,
    'tensor(int16)': np.int16,
    'tensor(int32)': np.int32,
    'tensor(int64)': np.int64,
    'tensor(uint8)': np.uint8,
    'tensor(uint16)': np.uint16,
    'tensor(uint32)': np.uint32,
    'tensor(uint64)': np.uint64,
}

class OnnxModel(BaseModel):
    """Onnx Model object.

    Args:
        BaseModel (BaseModel): The base model object.
    """
    def __init__(self, config: dict, model, input_shapes: dict, output_shapes: dict):
        """ Initialize an onnx model object.

        Args:
            config: A dictionary containing the model configuration.
            model: The model object.
            input_shapes: A dictionary containing the input shapes and types of the model.
            output_shapes: A dictionary containing the output shapes and types of the model.
        """
        
        super().__init__(config, model, "OnnxModel", input_shapes, output_shapes)
    
    @classmethod
    def init(cls, config: dict, model) -> 'OnnxModel':
        """ A constructor-like function to init a onnx model object.

        Args:
            config: A dictionary containing the model configuration.
            model: The model object.
            input_shapes_and_types: A dictionary containing the input shapes and types of the model.
            output_shapes_and_types: A dictionary containing the output shapes and types of the model.
        """
        if os.path.exists("tmp/temp_saved_model"):
            shutil.rmtree("tmp/temp_saved_model")
            os.makedirs("tmp/temp_saved_model")
        else:
            os.makedirs("tmp/temp_saved_model")
        
        onnx.save(model, "tmp/temp_saved_model/model.onnx")
        sess = ort.InferenceSession("tmp/temp_saved_model/model.onnx")
        input_specs = []
        output_specs = []
        
        def format_shape(shape):
            for i in range(len(shape)):
                if isinstance(shape[i], str) and shape[i].startswith("unk__"):
                    shape[i] = None
            return shape
        
        for item in sess.get_inputs():
            input_specs.append({
                "name": item.name,
                "shape": format_shape(item.shape),
                "dtype": onnx_dtype_to_np_dtype[item.type]
            })
        for item in sess.get_outputs():
            output_specs.append({
                "name": item.name,
                "shape": format_shape(item.shape),
                "dtype": onnx_dtype_to_np_dtype[item.type]
            })
        
        return cls(config, model, input_specs, output_specs)
    
if __name__ == "__main__":
    model, input_shapes, output_shapes = randomly_construct_onnx_model()
    onnxModel = OnnxModel.init({}, model)
    print(onnxModel.input_shapes)
    print(onnxModel.output_shapes)