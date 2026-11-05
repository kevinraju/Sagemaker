import os
import botocore.client

# 1. Set environment variables first
os.environ["AWS_ACCESS_KEY_ID"] = "AKIAIOSFODNN7EXAMPLE"
os.environ["AWS_SECRET_ACCESS_KEY"] = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# 2. Intercept botocore API calls to mock AWS STS and ECR locally
original_make_api_call = botocore.client.BaseClient._make_api_call

def mocked_make_api_call(self, operation_name, kwarg):
    if operation_name == 'GetCallerIdentity':
        return {
            'UserId': 'AKIAIOSFODNN7EXAMPLE',
            'Account': '111122223333',
            'Arn': 'arn:aws:iam::111122223333:user/local-user'
        }
    elif operation_name == 'GetAuthorizationToken':
        return {
            'authorizationData': [{
                'authorizationToken': b'QVdTOkFLSUFJT1NST0ROTjdFWEFNUExFCg==',
                'proxyEndpoint': 'https://111122223333.dkr.ecr.us-east-1.amazonaws.com'
            }]
        }
    elif operation_name == 'ListBuckets':
        return {'Buckets': []}
    elif operation_name in ['HeadBucket', 'CreateBucket', 'DescribeRepositories', 'CreateRepository']:
        return {}
    return original_make_api_call(self, operation_name, kwarg)

botocore.client.BaseClient._make_api_call = mocked_make_api_call

import sagemaker
from sagemaker.sklearn.model import SKLearnModel

# Initialize LocalSession with local code config
sagemaker_session = sagemaker.LocalSession()
sagemaker_session.config = {'local': {'local_code': True}}

role = "arn:aws:iam::111122223333:role/service-role/AmazonSageMaker-ExecutionRole"
image_uri = "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3"

model = SKLearnModel(
    model_data="file://model.tar.gz",
    role=role,
    entry_point="inference.py",
    source_dir="code",
    image_uri=image_uri,
    sagemaker_session=sagemaker_session
)

print("Deploying model locally via Docker...")
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="local"
)

print("Testing prediction on local Docker endpoint...")
sample_data = [[0.5, -0.2, 1.1, -0.5]]
result = predictor.predict(sample_data)
print("Docker Container Prediction Result:", result)

# Clean up endpoint container
predictor.delete_endpoint()