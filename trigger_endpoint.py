import json
import boto3

# Initialize SageMaker runtime client
sagemaker_runtime = boto3.client("sagemaker-runtime")

ENDPOINT_NAME = "sagemaker-serverless-endpoint-v4"

def lambda_handler(event, context):
    try:
        # Extract payload from API Gateway or direct invocation event
        if "body" in event:
            payload = event["body"]
        else:
            payload = json.dumps(event)

        # Invoke the SageMaker Serverless Endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=payload
        )

        # Parse response body
        result = json.loads(response["Body"].read().decode())

        return {
            "statusCode": 200,
            "body": json.dumps({"prediction": result})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }