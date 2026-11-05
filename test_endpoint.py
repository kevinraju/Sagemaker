import time
import boto3
import json
from botocore.exceptions import ClientError

client = boto3.client('sagemaker-runtime', region_name='us-east-1')
endpoint_name = "sagemaker-serverless-endpoint-v4"
payload = [[1.0, 2.0, 3.0, 4.0]]

print("Sending request to serverless endpoint...")

max_retries = 10
for attempt in range(max_retries):
    try:
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        result = json.loads(response['Body'].read().decode())
        print("Prediction Result:", result)
        break
    except ClientError as e:
        if "ModelNotReadyException" in str(e):
            print(f"Model is warming up (attempt {attempt + 1}/{max_retries}). Retrying in 5 seconds...")
            time.sleep(5)
        else:
            raise e