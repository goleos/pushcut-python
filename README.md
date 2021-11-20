# Pushcut API Python Client
A python client used to interact with the [Pushcut API](https://www.pushcut.io/webapi.html).

## Usage
```python
from pushcut import Client, Notification, NotificationAction

client = Client(api_key="super-secret key", default_notification_name="My First Notification")

# Basic functionality

client.devices()
# [{'id': 'iPhone 11', 'name': 'iPhone 11'}, {'id': 'iPad Pro', 'name': 'iPad Pro'}]
client.notifications()
# [{'id': 'My First Notification', 'title': 'Automate Away 🚀'}]

# Sending Notifications

my_notification = Notification(
    title="Python Client", 
    text="This message was sent from the Pushcut API Python Client"
)
# Add an image
my_notification.image = "https://picsum.photos/200"

# Add actions
my_notification.defaultAction = NotificationAction(url="https://example.com")

# Set notification to only appear on my phone
my_notification.devices = ["iPhone 11"]

other_action = NotificationAction(
    name="Turn Off The Lights",
    input="off",
    shortcut="Change the lights",
    keepNotification=False
)

my_notification.actions.append(other_action)

client.send_notification(my_notification)
```
