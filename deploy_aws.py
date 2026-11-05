import sagemaker
from sagemaker.sklearn.model import SKLearnModel

# This automatically uses the compliant default session bucket name for your account
sagemaker_session = sagemaker.Session()
bucket = sagemaker_session.default_bucket() 

role = "arn:aws:iam::508139322670:role/AmazonSageMaker-ExecutionRole"

model = SKLearnModel(
    model_data="s3://sagemaker-model-bucket-508139322670/model.tar.gz",
    role=role,
    entry_point="inference.py",
    source_dir="code",
    framework_version="1.2-1",  # <-- Match your local pip scikit-learn version here!
    sagemaker_session=sagemaker_session
)

print("Deploying model to AWS SageMaker...")
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.xlarge"
)

print(f"Endpoint deployed successfully! Name: {predictor.endpoint_name}")