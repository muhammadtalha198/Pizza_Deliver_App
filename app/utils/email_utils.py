
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.core.config import settings

def send_email_verification(to_email: str, token: str):
    sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = Email(settings.EMAIL_SENDER)
    to_email = To(to_email)
    subject = "Email Verification"
    verification_link = f"http://localhost:8000/api/auth/verify-email/{token}"

    content = Content("text/plain", f"Please verify your email by clicking this link: {verification_link}")
    mail = Mail(from_email, to_email, subject, content)

    try:
        response = sg.send(mail)
        return response
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")
