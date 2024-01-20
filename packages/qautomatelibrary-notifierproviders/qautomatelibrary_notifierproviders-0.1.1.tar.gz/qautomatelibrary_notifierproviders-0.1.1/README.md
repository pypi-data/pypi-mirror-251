# nofifierproviders

Custon providers for [notifiers](https://github.com/liiight/notifiers/blob/284ee16b9a07b836164973e5a9f02fd7e0eb3490/README.md) by [liiight](https://github.com/liiight)

For more indepth usage of the "providers" library, please read the library's documentation.

## Guide and Usage Examples

### Getting a schema from a provider to get the required parameters
```
from qautomatelibrary.NotifierProviders.RocketChatProvider import RocketChatProvider
r = RocketChatProvider()
print(f"Provider required settings: {r.required}")

# Provider required settings: {'required': ['user', 'password', 'channel', 'message']}

print(f"All Provider settings: {r.schema}")

# All Provider settings: {'type': 'object', 'properties': {'user': {'type': 'string'}, 'password': {'type': 'string'}, 'channel': {'type': 'string'}, 'message': {'type': 'string'}, 'attachments': {'oneOf': [{'type': 'array', 'items': {'type': 'string'}, 'minItems': 1, 'uniqueItems': True}, {'type': 'string'}]}, 'thread': {'type': 'string'}}, 'required': ['user', 'password', 'channel', 'message']}

settings = {
    "user": "Rocketchat_username",
    "password": "Rocketchat_password",
    "channel": "#Channel_where_bot_has_access",
    "message": "Hello from python!",
    "attachments": "C:\pics\Cat.jpg",
    "thread": "None"
}

r.notify(**settings)
```


### Adding to notifiers
```
import json

from pathlib import Path
from notifiers.core import _all_providers
from qautomatelibrary.NotifierProviders.RocketChatProvider import RocketChatProvider
from qautomatelibrary.NotifierProviders.O365EmailProvider import O365EmailProvider

_all_providers['RocketChatProvider.name'] = RocketChatProvider

r = get_notifier('rocketchat')

settings = json.loads( Path( "./rocketchatprovider-credentials.json" ).read_text() )

settings['message'] = "Hello from python!"

r.notify(**settings)

```

### Using a specific Provider
```
import json
from pathlib import Path
from qautomatelibrary.NotifierProviders.RocketChatProvider import RocketChatProvider

r = RocketChatProvider()

settings = json.loads( Path( "./rocketchatprovider-credentials.json" ).read_text() )

settings['message'] = "Hello from python!"

r.notify(**settings)

```

### Dynamic provider selection
Simulates a simple use case of non-hardcoded provider usage

[dynamic_example.py](./examples/dynamic_example.py)

### Loguru example
Simple example of using Loguru logger to send notifications when an error happens

[loguru_example.py](./examples/loguru_example.py)

## Running the examples
Run the examples from the directory where you have your configuration files and potential attachments.

Not all of the configuration for the examples can be done via json file, this is to force everyone to read through the examples.

```
/WorkingDir
    /examples
        dynamic_example.py
    /providers
        ...
    o365emailprovider-credentials.json
    rocketchatprovider-credentials.json
    katti.jpg

> python ./examples/dynamic_example.py
```

## Configuration / Settings
### RocketchatProvider

notifier provider to enable sending messages to a rocketchat server.

Only channel-messages supported for now.

This provider has some extra functionality outside of `.notify(**configuration)`, so I've provided some simple use cases.

#### Usable kwargs(dict)
| Key            | Example           | Description             |
|-----------------|---------------------|-------------------------|
| user | MagicMike| Login name to the Rocketchat server   |
| password | hunter23 | Password to the Rocketchat server |
| channel | #Common | Channel to send the message. Robot account needs to be in the channel.
| thread | asd4fsd33 | Thread id, to post in to a thread instead of making a new message
| message | Hello from Python! | Message to send to the channel
| attachments | Cat.jpg | Attachment(s), string or a list of strings pointing to the file(s)

#### Changing the target server

```
from qautomatelibrary.NotifierProviders.RocketChatProvider import RocketChatProvider
r = RocketChatProvider()
r.base_url = "https://your.server.com/"
```

#### Finding a thread id via the provider
You can use regex in the search string, but pay attention to the formula.

Thread search is greedy, so it will pick the first match.
```
from qautomatelibrary.NotifierProviders.RocketChatProvider import RocketChatProvider
r = RocketChatProvider()
r.find_thread('#YourChannel', "/^Very Specific Message$/i")
```

#### Creating a thread and utilizing it for a notification.
```
import json
from pathlib import Path
from qautomatelibrary.NotifierProviders.RocketChatProvider import RocketChatProvider

r = RocketChatProvider()
settings = json.loads( Path( "./rocketchatprovider-credentials.json" ).read_text() )
thread_id = r.create_thread('#YourChannel', "[THREAD #1] Title message")

settings['thread'] = thread_id
settings['message'] = "A new message in the thread <3"
r.notify(**settings)
```

### O365EmailProvider

Simple O365 provider for sending emails via Microsoft Graph API.

Usage should be self-explanatory, and the provider doesn't have any special functionality.

Configure, and call `provider_instance.notity(**configuration)`

#### Usable kwargs(dict)
| Key            | Example                    | Description                                             |
|-----------------|----------------------------|---------------------------------------------------------|
| client_id       | abc123                     | Application credentials (replace with your client ID)  |
| client_secret   | xyz456                     | Application credentials (replace with your client secret)|
| tenant_id       | mytenantid                 | Tenant where the Graph API SendMail is to be used      |
| user_email      | sender@example.com         | Email address of the sender                            |
| to_email        | recipient@example.com      | Recipient(s), string, or a list of strings             |
| cc              | cc@example.com             | Carbon copy recipient(s)                               |
| bcc             | bcc@example.com            | Blind carbon copy recipient(s)                         |
| subject         | Important Meeting Invite   | Email subject                                          |
| message         | Hello, please join the meeting at 2 PM. | Email message                       |
| attachments     | [file1.pdf, file2.docx]     | Attachment(s), string, or a list of strings pointing to the file(s) |
