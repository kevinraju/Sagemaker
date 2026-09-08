import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 1. SageMaker Training Function
def train():
    # Model training logic here (e.g., using scikit-learn)
    X = [[1, 2], [2, 3], [3, 4], [4, 5]]
    y = [0, 0, 1, 1]
    
    model = RandomForestClassifier()
    model.fit(X, y)
    
    # Save the trained model artifact
    model_dir = os.environ.get('SM_MODEL_DIR', './model')
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, "model.joblib"))
    print("Model saved successfully!")

# 2. SageMaker Inference Handler (Used when endpoint receives API requests)
def model_fn(model_dir):
    """Loads the saved model from disk into memory."""
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def predict_fn(input_data, model):
    """Generates predictions using the loaded model."""
    prediction = model.predict(input_data)
    return prediction.tolist()

if __name__ == "__main__":
    train()