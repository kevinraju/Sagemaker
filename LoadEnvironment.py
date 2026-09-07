import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
APP_PASSWORD = os.environ.get('APP_PASSWORD')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')

def lambda_handler(event, context):
    try:
        # Get the prediction payload passed from the SageMaker trigger
        prediction = event.get('prediction', 'No prediction data returned')
        
        # Build the HTML email content
        subject = "SageMaker Inference Result"
        body = f"""
        <html>
            <body>
                <h2>SageMaker Model Execution Completed</h2>
                <p><strong>Prediction Output:</strong></p>
                <pre>{json.dumps(prediction, indent=2)}</pre>
            </body>
        </html>
        """
        
        # Configure MIME Message
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECEIVER_EMAIL
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))
        
        # Connect to Gmail SMTP Server and send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
            
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'Email notification sent successfully!'})
        }

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }