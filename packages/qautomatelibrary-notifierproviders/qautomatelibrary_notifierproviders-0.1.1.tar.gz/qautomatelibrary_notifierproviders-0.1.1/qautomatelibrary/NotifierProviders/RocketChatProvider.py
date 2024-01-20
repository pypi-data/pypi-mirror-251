# Cloud based messages idea:
# Post a message with cloud name and uri, collect the message id, and save it to db.
# For each cloud's messages, use that message id to add a new message to a thread.
# You can add attachments and everything to a message, so it works just like a normal message.
import logging
import mimetypes
from functools import lru_cache

from notifiers.core import Provider
from notifiers.core import Response
from notifiers.exceptions import BadArguments
from notifiers.utils.schema.helpers import one_or_more
from requests import Session


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)


class RocketChatProvider(Provider):
    base_url = "https://chat.codemen.fi/api/v1"
    name = "rocketchat"
    site_url = "https://chat.codemen.fi"
    _required = {"required": ["user", "password", "channel", "message"]}
    _schema = {
        "type": "object",
        "properties": {
            "user": {"type": "string"},
            "password": {"type": "string"},
            "channel": {"type": "string"},
            "message": {"type": "string"},
            "attachments": one_or_more({"type": "string"}),
            "thread": {"type": "string"},
        },
    }
    debug = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Cache these functions to speed up the process and do it here instead of decorator
        # to prevent memory leaks
        self.get_channel_id = lru_cache(maxsize=10)(self.get_channel_id)
        self.find_thread = lru_cache(maxsize=10)(self.find_thread)
        self._session = Session()

    def get_channel_id(self, channel: str) -> str:
        if not self._session:
            raise BadArguments("Login first")
        if channel.startswith("#"):
            channel = channel[1:]
        r = self._session.get(self.base_url + "/rooms.info?roomName=" + channel)
        if r.status_code != 200:
            raise BadArguments("Failed to get channel id : " + r.json()["error"])
        return r.json()["room"]["_id"]

    def find_thread(self, channel_name: str, text: str) -> str:
        channel_id = self.get_channel_id(channel_name)
        if not self._session:
            raise BadArguments("Login first")

        r = self._session.get(
            self.base_url
            + "/chat.search?roomId="
            + channel_id
            + "&searchText="
            + text
            + "&count=1"
        )
        if r.status_code != 200:
            raise BadArguments("Failed to find thread: " + r.json()["error"])

        if self.debug:
            msgs = self._session.get(
                self.base_url
                + "/chat.getThreadMessages?tmid="
                + r.json()["messages"][0]["_id"]
            )

            for msg in msgs.json()["messages"]:
                logger.debug(f'{msg["u"]["username"]} sent:\n\t"{msg["msg"]}"')

        return r.json()["messages"][0]["_id"]

    def create_thread(self, channel: str, text: str) -> str:
        if not self._session:
            raise BadArguments("Login first")

        r = self._session.post(
            self.base_url + "/chat.postMessage", json={"channel": channel, "text": text}
        )
        if r.status_code != 200:
            raise BadArguments("Failed to create thread")
        return r.json()["message"]["_id"]

    def authenticate(self, user: str, password: str) -> Response:
        r = self._session.post(
            self.base_url + "/login", json={"user": user, "password": password}
        )
        if r.status_code != 200:
            raise BadArguments("Login failed")
        self._session.headers.update(
            {
                "X-Auth-Token": r.json()["data"]["authToken"],
                "X-User-Id": r.json()["data"]["userId"],
            }
        )

        return True

    def _send_notification(self, data: dict) -> Response:
        if not data.get("user") and not self.user:
            raise BadArguments("Missing user")
        if not data.get("password") and not self.password:
            raise BadArguments("Missing password")
        if not data.get("channel") and not self.channel:
            raise BadArguments("Missing channel")
        if not data.get("message") and not self.message:
            raise BadArguments("Missing message")

        baseurl = data.get("baseurl") or self.base_url
        user = data.get("user") or self.user
        password = data.get("password") or self.password
        channel = data.get("channel") or self.channel
        text = data.get("message")
        thread = data.get("thread")
        attachments = data.get("attachments")
        files = []

        self.authenticate(user, password)
        _channel_id = self.get_channel_id(channel)

        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]
            for attachment in attachments:
                files.append(
                    (
                        "file",
                        (
                            attachment,
                            open(attachment, "rb"),
                            mimetypes.guess_type(attachment)[0],
                        ),
                    )
                )

            payload = {
                "msg": (None, text),
                "description": (None, ""),
                "tmid": thread,
            }
            if len(files) == 1:
                r = self._session.post(
                    baseurl + "/rooms.upload/" + _channel_id, files=files, data=payload
                )
            else:
                first = files.pop(0)
                r = self._session.post(
                    baseurl + "/rooms.upload/" + _channel_id,
                    files=[first],
                    data=payload,
                )
                payload["msg"] = (None, "")
                for file in files:
                    r = self._session.post(
                        baseurl + "/rooms.upload/" + _channel_id,
                        files=[file],
                        data=payload,
                    )
        else:
            r = self._session.post(
                baseurl + "/chat.postMessage",
                json={"channel": channel, "text": text, "tmid": thread},
            )

        return self.create_response(None, r)

    def configure(self, user=None, password=None, channel=None, baseurl=None):
        self.password = password
        self.user = user
        self.channel = channel
        self.base_url = baseurl
