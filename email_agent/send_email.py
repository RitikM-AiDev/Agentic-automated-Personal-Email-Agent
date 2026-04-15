import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import sys
from auth import auth
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
subject = sys.argv[1]
content = sys.argv[2]
to_email = sys.argv[3]

def send_email():
    service = auth()
    message = EmailMessage()
    message.set_content(content)
    message["To"] = to_email
    message["From"] = "me"
    message["Subject"] = subject
    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()
    send_message = {"raw" : encoded_message}
    result= service.users().messages().send(
        userId = "me",
        body = send_message
    ).execute()
    print(result["id"])
if __name__ == "__main__":
    send_email()