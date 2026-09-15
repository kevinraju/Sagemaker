import boto3
import json

runtime = boto3.client("sagemaker-runtime")

endpoint_name = "sagemaker-serverless-endpoint-v4"

with open("payload.json", "r") as f:
    payload = f.read()

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="application/json",
    Body=payload
)

result = json.loads(response["Body"].read().decode())
print("Endpoint Response:", result)