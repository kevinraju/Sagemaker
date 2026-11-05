import os
import joblib
import numpy as np

def model_fn(model_dir):
    """
    Deserializes and loads the trained model from the model directory.
    SageMaker automatically calls this when starting the endpoint container.
    """
    model_path = os.path.join(model_dir, "model.joblib")
    model = joblib.load(model_path)
    return model

def predict_fn(input_data, model):
    """
    Performs prediction using the deserialized model and incoming input data.
    """
    # If input_data is received as a list or JSON payload, convert or run prediction directly
    prediction = model.predict(input_data)
    
    # Return output as a NumPy array (compatible with SageMaker's default serialization)
    return np.array(prediction)