import smtplib
import requests
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EmailMessage:
    """Handles email content."""
    def __init__(self, sender_email, receiver_email, subject, body):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.subject = subject
        self.body = body

    def build_message(self):
        """Builds an email message using MIME format."""
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body, 'plain'))
        return msg.as_string()

class EmailSender(ABC):
    """Abstract class for email sending services."""
    @abstractmethod
    def send(self, email_message: EmailMessage):
        pass

class SMTPClient:
    """Handles SMTP connection setup separately from email sending."""
    def __init__(self, smtp_host, smtp_port, username=None, password=None, use_tls=False):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_email(self, email_message: EmailMessage):
        """Sends an email using an established SMTP connection."""
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.sendmail(
                    email_message.sender_email,
                    email_message.receiver_email,
                    email_message.build_message()
                )
            print(f"Email sent successfully via {self.smtp_host}!")
        except Exception as e:
            print(f"Error sending email via {self.smtp_host}: {e}")

class SMTPService(EmailSender):
    """Handles email sending via SMTP using SMTPClient."""
    def __init__(self, smtp_client: SMTPClient):
        self.smtp_client = smtp_client

    def send(self, email_message: EmailMessage):
        self.smtp_client.send_email(email_message)

class MailHogService(SMTPService):
    """MailHog-specific email sender."""
    def __init__(self):
        super().__init__(SMTPClient('localhost', 1025))

class MailtrapSMTPService(SMTPService):
    """Mailtrap-specific email sender."""
    def __init__(self):
        super().__init__(
            SMTPClient(
                smtp_host=os.getenv('SMTP_HOST'),
                smtp_port=int(os.getenv('SMTP_PORT')),
                username=os.getenv('SMTP_USERNAME'),
                password=os.getenv('SMTP_PASSWORD'),
                use_tls=os.getenv('SMTP_USE_TLS') == 'True'
            )
        )

class MailtrapAPIService(EmailSender):
    """Handles email sending via Mailtrap's REST API."""
    def __init__(self):
        self.api_url = os.getenv("MAILTRAP_API_URL")
        self.api_token = os.getenv("MAILTRAP_API_TOKEN")

    def send(self, email_message: EmailMessage):
        payload = {
            "from": {"email": email_message.sender_email, "name": "Mailtrap Test"},
            "to": [{"email": email_message.receiver_email}],
            "subject": email_message.subject,
            "text": email_message.body,
            "category": "Integration Test"
        }
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            print("Email sent successfully via Mailtrap API!")
        except requests.exceptions.RequestException as e:
            print(f"Error sending email via Mailtrap API: {e}")

# Example usage
if __name__ == "__main__":
    sender = "from@example.com"
    receiver = "to@example.com"
    subject = "Hi Mailtrap"
    body = "This is a test email message."

    email_message = EmailMessage(sender, receiver, subject, body)

    mailhog = MailHogService()
    mailhog.send(email_message)

    mailtrap_smtp = MailtrapSMTPService()
    mailtrap_smtp.send(email_message)

    mailtrap_api = MailtrapAPIService()
    mailtrap_api.send(email_message)
