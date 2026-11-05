import boto3
import sagemaker
from sagemaker.sklearn.model import SKLearnModel
from sagemaker.serverless import ServerlessInferenceConfig

sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::508139322670:role/AmazonSageMaker-ExecutionRole"

model = SKLearnModel(
    model_data="s3://hanan-sagemaker-model-bucket/model.tar.gz",
    role=role,
    entry_point="train.py",
    framework_version="1.2-1",
    py_version="py3",
    sagemaker_session=sagemaker_session
)

serverless_config = ServerlessInferenceConfig(
    memory_size_in_mb=3072,
    max_concurrency=5
)

print("Starting serverless endpoint deployment to SageMaker...")

predictor = model.deploy(
    serverless_inference_config=serverless_config,
    endpoint_name="sagemaker-serverless-endpoint-v4"
)

print(f"Deployment completed! Endpoint Name: {predictor.endpoint_name}")