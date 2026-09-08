import boto3
import sagemaker
from sagemaker.sklearn.model import SKLearnModel

# Initialize SageMaker Session
sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::YOUR_ACCOUNT_ID:role/service-role/AmazonSageMaker-ExecutionRole"

# Define the SKLearn Model Container
model = SKLearnModel(
    model_data="s3://your-s3-bucket/model.tar.gz",  # Path to trained model tarball in S3
    role=role,
    entry_point="train.py",                          # Inference code from Step 1
    framework_version="1.2-1"
)

# Deploy to a real-time HTTP endpoint
predictor = model.deploy(
    instance_type="ml.t2.medium",                    # Free Tier eligible instance type
    initial_instance_count=1,
    endpoint_name="sagemaker-prediction-endpoint"
)

print(f"Endpoint deployed successfully: {predictor.endpoint_name}")