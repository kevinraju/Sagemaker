import json
import joblib

# 1. Load your local model
print("Loading model.joblib...")
model = joblib.load("model.joblib")

# 2. Load test input from payload.json
with open("payload.json", "r") as f:
    data = json.load(f)

print("Input Payload:", data)

# 3. Make a prediction locally
prediction = model.predict(data)
print("\n--- LOCAL PREDICTION SUCCESS ---")
print("Prediction Result:", prediction)