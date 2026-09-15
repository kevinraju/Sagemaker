import joblib
import tarfile
import os
import boto3
from sklearn.linear_model import LogisticRegression

# 1. Create a minimal dummy model
model = LogisticRegression()
model.fit([[1, 2], [3, 4]], [0, 1])

# 2. Save explicitly as 'model.joblib'
joblib.dump(model, "model.joblib")

# 3. Compress directly to 'model.tar.gz' without any subdirectories
with tarfile.open("model.tar.gz", "w:gz") as tar:
    tar.add("model.joblib", arcname="model.joblib")

# 4. Upload to your S3 bucket
s3 = boto3.client("s3")
s3.upload_file("model.tar.gz", "hanan-sagemaker-model-bucket", "model.tar.gz")

print("New model.tar.gz successfully uploaded to S3!")