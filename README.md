# AWS SageMaker Serverless Inference Pipeline

A complete, serverless Machine Learning deployment pipeline on AWS. This project trains a Scikit-Learn classification model, packages the model artifacts, and deploys it using **Amazon SageMaker Serverless Endpoints**. The deployment is integrated with **AWS Lambda** and **Amazon API Gateway** to deliver real-time predictions via HTTP REST requests.

---

## 🏗️ Architecture Overview
1. **Client / PowerShell:** Sends feature data formatted in JSON.
2. **Amazon API Gateway:** Serves as the public REST API entry point.
3. **AWS Lambda:** Receives the HTTP request payload and invokes the downstream SageMaker runtime endpoint.
4. **SageMaker Serverless Endpoint:** Loads the trained Scikit-Learn model (`model.joblib`) inside a managed container, performs real-time inference, and returns prediction results.

---

## 📁 Repository Structure

* `train.py` – Trains the model locally and exports `model.joblib`.
* `deploy.py` – Configures and deploys the model to an AWS SageMaker Serverless Endpoint.
* `test_endpoint.py` – Invokes the live SageMaker endpoint remotely via `boto3`.
* `test_local.py` – Tests model loading and predictions locally without AWS cloud dependencies.
* `trigger_endpoint.py` – Alternative script for invoking and testing the prediction pipeline.
* `fix_model.py` – Utility script for model verification and packaging.
* `payload.json` – Sample feature input data used for testing inference.
* `model/model.joblib` – Saved Scikit-Learn model artifact.
* `model.tar.gz` – Compressed model archive structured for SageMaker deployment.

---

## 🛠️ Code Implementation Highlights

### 1. Model Deployment (`deploy.py`)
```python
import boto3
from sagemaker.serverless import ServerlessInferenceConfig
from sagemaker.sklearn.model import SKLearnModel

# Define Serverless Endpoint configuration (Memory & Concurrency)
serverless_config = ServerlessInferenceConfig(
    memory_size_in_mb=2048,
    max_concurrency=5
)

# Initialize SKLearn model object
model = SKLearnModel(
    model_data='s3://<your-s3-bucket>/model.tar.gz',
    role='<your-sagemaker-execution-role>',
    entry_point='inference.py',
    framework_version='1.2-1'
)

# Deploy to SageMaker Serverless Endpoint
predictor = model.deploy(
    serverless_inference_config=serverless_config,
    endpoint_name='sagemaker-serverless-endpoint-v4'
)
print("Endpoint successfully deployed!")
2. Lambda Trigger Handler
Python
import json
import boto3

runtime = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    payload = event['body']
    
    # Invoke SageMaker Endpoint
    response = runtime.invoke_endpoint(
        EndpointName='sagemaker-serverless-endpoint-v4',
        ContentType='application/json',
        Body=payload
    )
    
    result = json.loads(response['Body'].read().decode('utf-8'))
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'prediction': result})
    }
🚀 How to Run & Test
1. Local Offline Verification
Run a prediction locally on your computer to verify dependencies and model output:

PowerShell
python test_local.py
2. Deploy Model to AWS SageMaker
Deploy the serverless endpoint using your AWS credentials:

PowerShell
python deploy.py
3. Test Live AWS Endpoint via Boto3
PowerShell
python test_endpoint.py
4. Test End-to-End API Gateway via PowerShell
PowerShell
Invoke-RestMethod -Uri "https://508139322670[.execute-api.us-east-1.amazonaws.com/predict](https://.execute-api.us-east-1.amazonaws.com/predict)" `
                  -Method POST `
                  -ContentType "application/json" `
                  -Body '[[1.0, 2.0]]'
⚙️ Prerequisites & Environment
Python 3.x

scikit-learn, joblib, boto3, sagemaker

**AWS CLI configured** (`aws configure`)

![SageMaker API Gateway Prediction Output](https://raw.githubusercontent.com/kevinraju/Sagemaker/main/prediciton.png.png)