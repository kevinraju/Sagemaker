from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
import joblib

# Generate some dummy training data
X, y = make_classification(n_samples=100, n_features=4, random_state=42)

# Train a simple model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the model to the root folder (outside venv!)
joblib.dump(model, "model.joblib")
print("Model successfully saved as model.joblib!")