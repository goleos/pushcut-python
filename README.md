# Pushcut API Python Client
A python client used to interact with the [Pushcut API](https://www.pushcut.io/webapi.html). See detailed description
with explanations [here](https://www.pushcut.io/support_notifications.html).

With this client you can trigger any enabled notification in your Pushcut account. 
You can also send any custom notification. If you have an Automation Server running, you can tell the server to
execute any enabled shortcut or homekit scene. If you have Automation Server Extended, you can also use this client to 
delay the execution of a given shortcut or homekit scene.

## Authorisation
API Key is used as the authorisation method. Note that this is not the same as "Webhook secret".

To obtain an API key:
1. In the Pushcut app, go into the "Account" tab
2. Under "INTEGRATIONS" section click on "Add API Key"
3. Give it a name and click "Generate"

## Usage
### Example: sending a notification to my phone
```python
from pushcut import Client, Notification, NotificationAction
client = Client(api_key="super_secret_api_key", default_notification_name="My First Notification")

client.devices()
[{'id': 'iPhone 11', 'name': 'iPhone 11'}, {'id': 'iPad Pro', 'name': 'iPad Pro'}]
client.notifications()
[{'id': 'My First Notification', 'title': 'Automate Away 🚀'}]


my_notification = Notification(
    title="Python Client", 
    text="This message was sent from the Pushcut API Python Client"
)
# Add an image of a cute puppy
my_notification.image = "https://upload.wikimedia.org/wikipedia/commons/6/68/Szczenie_Jack_Russell_Terrier3.jpg"
# If we click on the notification, we want to open the webpage example.com
my_notification.defaultAction = NotificationAction(url="https://example.com")

# Set notification to only appear on my phone
my_notification.devices = ["iPhone 11"]

low_power_mode_on = NotificationAction(
    name="⚡ Turn ON Low Power Mode ⚡",
    shortcut="Enable Low Power Mode",
    keepNotification=False
)
my_notification.actions.append(low_power_mode_on)

client.send_notification(my_notification)
```

<p float="left" align="middle">
  <img src="screenshots/notification1.PNG" width="400" />
  <img src="screenshots/notification1_2.PNG" width="400" />
</p>
*Attribution: Szczenie Jack Russell Terrier.jpg: Siristruderivative work: Wuhazet, Public domain, via Wikimedia Commons*

## Errors and Exceptions
If the response code of an http request made by client does not start with 2 (ie. 200, 201 etc), then a 
`PushcutAPIException` from `pushcut.exceptions` will be raised.

Below is a list of API-related errors the client can raise:

| HTTP Response Code |                                 Error Message Example                                |           Exception Raised          |
|:------------------:|:------------------------------------------------------------------------------------:|:-----------------------------------:|
| 400                | Timeout must be a number between 1 and 45 seconds, or set to 'nowait'.               | `PushcutBadRequestError`            |
| 401                |                                                                                      | `PushcutUnauthorisedError`          |
| 403                | Invalid API-Key provided.                                                            | `PushcutForbiddenError`             |
| 402                | Automation Server Extended is required to schedule delayed requests.                 | `PushcutSubscriptionRequiredError`  |
| 404                | Notification not found.                                                              | `PushcutNotFoundError`              |
| 502                | Automation Server is currently not running on any iOS device linked to this account. | `PushcutAutomationServerNotRunning` |
| 504                | iOS device did not respond in time.                                                  | `PushcutAutomationServerTimeout`    |
| others             |                                                                                      | `PushcutAPIException`               |