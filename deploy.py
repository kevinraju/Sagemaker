import boto3
import sagemaker
from sagemaker import Model

# Initialize SageMaker Session
sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::YOUR_ACCOUNT_ID:role/service-role/AmazonSageMaker-ExecutionRole"

# Define generic Model container using a pre-built Scikit-learn image
image_uri = sagemaker.image_uris.retrieve(
    framework="sklearn",
    region=sagemaker_session.boto_region_name,
    version="1.2-1"
)

model = Model(
    image_uri=image_uri,
    model_data="s3://your-s3-bucket/model.tar.gz",
    role=role,
    entry_point="train.py",
    sagemaker_session=sagemaker_session
)

# Deploy to a real-time HTTP endpoint
predictor = model.deploy(
    instance_type="ml.t2.medium",
    initial_instance_count=1,
    endpoint_name="sagemaker-prediction-endpoint"
)

print(f"Endpoint deployed successfully: {predictor.endpoint_name}")