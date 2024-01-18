import tensorflow as tf
import numpy as np

class BaseModel:
    """ Base model object. 
    
        Each model object should contain the following attributes:
        
        config: A dictionary containing the model configuration.
        model: The model object.
        model_type: The type of the model object.
        Input shapes and types: A dictionary containing the input shapes and types of the model.
        Output shapes and types: A dictionary containing the output shapes and types of the model.
    """
    
    def __init__(self, config: dict, model, model_type: str, input_shapes: dict, output_shapes: dict):
        """ Initialize a base model object.
        
        Args:
            config: A dictionary containing the model configuration.
            model: The model object.
            model_type: The type of the model object.
            input_shapes_and_types: A dictionary containing the input shapes and types of the model.
            output_shapes_and_types: A dictionary containing the output shapes and types of the model.
        """
        
        self.config = config
        self.model = model
        self.model_type = model_type
        self.input_shapes = input_shapes
        self.output_shapes = output_shapes
        self.parsed_input_shapes_and_types = {}
        self.parsed_output_shapes_and_types = {}
        
    @classmethod
    def init(cls, config: dict, model, model_type: str, input_shapes: dict, output_shapes: dict) -> 'BaseModel':
        """ A constructor-like function to init a base model object.
        
        Args:
            config: A dictionary containing the model configuration.
            model: The model object.
            model_type: The type of the model object.
            input_shapes: A dictionary containing the input shapes and types of the model.
            output_shapes: A dictionary containing the output shapes and types of the model.
        """
            
        return cls(config, model, model_type, input_shapes, output_shapes)
    
    def __type__(self):
        """ Return the type of the model object. """
        
        return str(self.model_type)
        
    def __str__(self):
        """ Print the model configuration. """
        
        return str(self.config)
    
    def __repr__(self):
        """ Print the model configuration. """
        
        return str(self.config)
    
    def __eq__(self, other):
        """ Check if two model objects are equal. """
        
        return self.config == other.config and self.model
    
    def convert_to_javascript(self):
        """ 
        Convert the model to a javascript format. 
        Dummy function for inheriting classes to implement.
        """

        pass
    
    def insert_to_webpage(self, web_template, converted_code):
        """ 
        Insert the model to a webpage. 
        We assume that the model is already converted to a javascript format, and its javascript code is in some sort of dictionary format.
        Dummy function for inheriting classes to implement.
        """
        
        pass
    