import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.draft_creator import DraftCreator

SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def _get_gmail_service(credentials_path: str, token_path: str):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def _fetch_signature(service) -> str:
    result = service.users().settings().sendAs().list(userId="me").execute()
    for alias in result.get("sendAs", []):
        if alias.get("isDefault"):
            return alias.get("signature", "")
    return ""


class GmailApiDraftCreator(DraftCreator):
    def __init__(self, credentials_path: str, token_path: str = "token.json"):
        self._service = _get_gmail_service(credentials_path, token_path)
        self._signature = _fetch_signature(self._service)

    def create_draft(self, to: str, subject: str, html_body: str, attachment_path: str) -> None:
        full_body = html_body.replace("{{email_signature}}", self._signature or "")

        msg = MIMEMultipart()
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(full_body, "html"))

        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(attachment_path)}"',
        )
        msg.attach(part)

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        result = self._service.users().drafts().create(
            userId="me", body={"message": {"raw": raw}}
        ).execute()
        return result["id"]

    def send_draft(self, draft_id: str) -> None:
        self._service.users().drafts().send(
            userId="me", body={"id": draft_id}
        ).execute()
