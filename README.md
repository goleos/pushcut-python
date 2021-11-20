# Pushcut API Python Client
A python client used to interact with the [Pushcut API](https://www.pushcut.io/webapi.html). See detailed description [here](https://www.pushcut.io/support_notifications.html).

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

<p float="left">
  <img src="screenshots/notification1.PNG" width="100" />
  <img src="screenshots/notification1_2.PNG" width="100" />
</p>


[comment]: <> (<img alt="Notification Screenshot" src="screenshots/notification1.PNG"/> )

[comment]: <> (<img alt="Notification Screenshot" height="200" src="screenshots/notification1_2.PNG" width="100"/>)



Attribution: Szczenie Jack Russell Terrier.jpg: Siristruderivative work: Wuhazet, Public domain, via Wikimedia Commons