import smtplib
from email.mime.text import MIMEText

def lambda_handler(event, context):
    prediction = event.get('prediction')
    
    sender_email = "your-email@gmail.com"
    app_password = "your-gmail-app-password" # Generated from Google Account App Passwords
    receiver_email = "recipient@gmail.com"
    
    msg = MIMEText(f"SageMaker Model Inference Result: {prediction}")
    msg['Subject'] = "SageMaker Prediction Complete"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    return {'status': 'Email sent via SMTP'}