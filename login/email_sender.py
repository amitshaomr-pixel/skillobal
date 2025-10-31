#email_sender.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(receiver_email: str, otp: str) -> bool:
    html_content = f"""
    <div style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
        <h2 style="color: #6c63ff;">Email Verification</h2>
        <p>Dear User,</p>
        <p>We received a request to verify your account. Your verification code (valid for 5 minutes):</p>
        <div style="background-color: #6c63ff; color: white; font-size: 24px; font-weight: bold; display: inline-block; padding: 10px 20px; border-radius: 5px;">
            {otp}
        </div>
        <p>If you did not request this, please ignore this email.</p>
        <p style="margin-top: 20px; font-weight: bold;">- Skillobal Support Team</p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email
    msg["Subject"] = "Skillobal: Email Verification Code"

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print("Email sending error:", e)
        return False
