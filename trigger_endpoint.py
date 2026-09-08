import os
import json
import boto3

# Initialize SageMaker Runtime client
runtime = boto3.client('sagemaker-runtime')
endpoint_name = os.environ.get('ENDPOINT_NAME', 'sagemaker-prediction-endpoint')

def lambda_handler(event, context):
    try:
        # Parse incoming JSON payload from event/API Gateway
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event
        data = body.get('data', [[1, 2]])  # Default fallback feature array
        
        # Invoke SageMaker Endpoint
        response = runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(data)
        )
        
        # Read prediction output
        result = json.loads(response['Body'].read().decode())
        
        return {
            'statusCode': 200,
            'body': json.dumps({'prediction': result})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }