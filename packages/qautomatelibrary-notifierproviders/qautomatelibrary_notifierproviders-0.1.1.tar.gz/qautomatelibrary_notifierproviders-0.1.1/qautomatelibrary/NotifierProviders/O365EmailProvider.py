# TODO: Cache login session
# TODO: configure/authenticate method to allow for long living sessions
import base64
import logging
import mimetypes

from notifiers.core import Provider
from notifiers.exceptions import BadArguments
from notifiers.utils.schema.helpers import list_to_commas
from notifiers.utils.schema.helpers import one_or_more
from requests import post
from requests import Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class O365EmailProvider(Provider):
    """Provider for sending emails using O365."""

    # Define provider schema
    base_url = "https://graph.microsoft.com/v1.0"
    name = "o365email"
    site_url = "https://graph.microsoft.com"
    _required = {
        "required": [
            "client_id",
            "client_secret",
            "tenant_id",
            "user_email",
            "to_email",
            "subject",
            "message",
        ]
    }

    _session = None

    # This is required for the base class to work properly
    _schema = {
        "type": "object",
        "properties": {
            "client_id": {"type": "string"},
            "client_secret": {"type": "string"},
            "tenant_id": {"type": "string"},
            "user_email": {"type": "string"},
            "to_email": one_or_more({"type": "string"}),
            "subject": {"type": "string"},
            "message": {"type": "string"},
            "mailbox_alias": {"type": "string"},
            "attachments": one_or_more({"type": "string"}),
            "cc": one_or_more({"type": "string"}),
            "bcc": one_or_more({"type": "string"}),
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._session = Session()

    def _send_notification(self, data):
        """Send the notification."""

        # Retrieve and validate required data
        client_id = data.get("client_id")
        client_secret = data.get("client_secret")
        tenant_id = data.get("tenant_id")
        user_email = data.get("user_email")
        to_email = data.get("to_email")
        subject = data.get("subject")
        body = data.get("message")
        cc = data.get("cc")
        bcc = data.get("bcc")
        mailbox_alias = data.get("mailbox_alias", user_email)
        attachments = data.get("attachments")

        if not self._session:
            self._session = Session()

        token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "resource": "https://graph.microsoft.com",
        }
        token_response = self._session.post(token_endpoint, data=token_data)
        if token_response.status_code != 200:
            raise BadArguments("Failed to retrieve access token")

        token_response = token_response.json()
        access_token = token_response.get("access_token")
        if not access_token:
            raise BadArguments("Failed to retrieve access token")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "text/plain",
        }

        self._session.headers.update(headers)

        # Prepare and send the email
        sendmail_endpoint = f"{self.base_url}/users/{user_email}/sendMail"

        address = {"emailAddress": {"address": mailbox_alias}}
        message = {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": list_to_commas(to_email)}}],
            "sender": address,
            "from": address,
        }
        payload = {
            "message": message,
            "saveToSentItems": False,
        }

        if cc:
            payload["message"]["ccRecipients"] = [
                {"emailAddress": {"address": list_to_commas(cc)}}
            ]
        if bcc:
            payload["message"]["bccRecipients"] = [
                {"emailAddress": {"address": list_to_commas(bcc)}}
            ]
        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]
            payload["message"]["attachments"] = []
            for attachment in attachments:
                logger.debug(f"Adding attachment: {attachment}")
                with open(attachment, "rb") as file:
                    file_bytes = base64.b64encode(file.read())

                payload["message"]["attachments"].append(
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": attachment,
                        "ContentBytes": file_bytes.decode(),
                        "contentType": mimetypes.guess_type(attachment)[0],
                    }
                )
        response = post(sendmail_endpoint, headers=headers, json=payload, timeout=30)

        return self.create_response(data, response)
