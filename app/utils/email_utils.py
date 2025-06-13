import smtplib
from email.mime.text import MIMEText

def send_otp_email(to_email, otp):
    print(f"OTP for {to_email}: {otp}")
    return {"message": "OTP generated", "otp": otp}