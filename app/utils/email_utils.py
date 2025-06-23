from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings  # <-- Import settings

def send_otp_email(to_email, otp):
    subject = "Your OTP Code"
    content = f"Your OTP code is: {otp}"
    from_email = settings.SENDGRID_FROM_EMAIL  # <-- Use settings
    sendgrid_api_key = settings.SENDGRID_API_KEY  # <-- Use settings

    if not sendgrid_api_key:
        print("SENDGRID_API_KEY not set in config")
        return {"message": "SendGrid API key not set", "otp": otp}

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        if response.status_code in [200, 202]:
            return {"message": "OTP sent to your email address.", "otp": otp}
        else:
            print(f"SendGrid error: {response.status_code} {response.body}")
            return {"message": "Failed to send OTP email", "otp": otp}
    except Exception as e:
        print(f"SendGrid exception: {e}")
        return {"message": "Failed to send OTP email", "otp": otp}