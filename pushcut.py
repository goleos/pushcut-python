import datetime
import requests
from typing import Optional, List


class Action:

    @classmethod
    def urlBackgroundOptions(cls, httpMethod: Optional[str] = None, httpContentType: Optional[str] = None,
                             httpHeader: Optional[List[dict]] = None, httpBody: Optional[str] = None):
        return {key: value for key, value in locals().items() if value}

    def __init__(self, name: Optional[str] = None, input: Optional[str] = None, keepNotification: Optional[bool] = None,
                 shortcut: Optional[str] = None, homekit: Optional[str] = None, runOnServer: Optional[bool] = None,
                 online: Optional[str] = None, url: Optional[str] = None, urlBackgroundOptions: Optional[dict] = None):
        self.name = name
        self.input = input
        self.keepNotification = keepNotification
        self.shortcut = shortcut
        self.homekit = homekit
        self.runOnServer = runOnServer
        self.online = online
        self.url = url
        self.urlBackgroundOptions = urlBackgroundOptions

    def as_dict(self) -> dict:
        return {key: value for key, value in vars(self).items() if value}


class Notification:

    def __init__(self, title: Optional[str] = None, text: Optional[str] = None, sound: Optional[str] = None,
                 image: Optional[str] = None, input: Optional[str] = None, defaultAction: Optional[Action] = None,
                 actions: Optional[List[Action]] = [], devices: Optional[List[str]] = []):
        self.title = title
        self.text = text
        self.sound = sound
        self.image = image
        self.input = input
        self.defaultAction = defaultAction
        self.actions = actions
        self.devices = devices

    def as_dict(self) -> dict:
        no_nones = {key: value for key, value in vars(self).items() if value}
        if no_nones.get('defaultAction'):
            no_nones['defaultAction'] = no_nones['defaultAction'].as_dict()
        if no_nones.get('actions'):
            no_nones['actions'] = [item.as_dict() for item in no_nones['actions']]
        return no_nones


class Pushcut:

    def __init__(self, api_key, default_notification_name: Optional[str]=None):
        self.api_key = api_key
        self.home_endpoint = f"https://api.pushcut.io/v1"
        self.default_notification_name = default_notification_name
        self._headers = {"API-Key": api_key, "Accept": "application/json"}

    def _perform_request(self, method: str, target: str, json_data: Optional):
        request = requests.request(method=method, url=f"{self.home_endpoint}/{target}", json=json_data,
                                   headers=self._headers)
        status_code = request.status_code
        info = request.text
        if 200 <= status_code <= 299:
            return info
        elif status_code == 502:
            raise AutomationServerNotRunning(info)
        elif status_code == 504:
            raise AutomationServerTimeout(info)
        else:
            raise PushcutError(info)

    def send_notification(self, notification: Notification, notification_name: Optional[str]=None):
        if not notification_name:
            notification_name = self.default_notification_name
        return self._perform_request("POST", f"notifications/{notification_name}", notification.as_dict())

    def devices(self):
        return self._perform_request("GET", "devices", None)

    def notifications(self):
        return self._perform_request("GET", "notifications", None)

    def execute_automation_server_action(self, shortcut: Optional[str] = None, input: Optional = None, homekit: Optional[str] = None,
                                         timeout: Optional[int]=None, delay: datetime.timedelta=None,
                                         identifier: Optional[str] = None):
        data = {
            "shortcut": shortcut,
            "input": input,
            "homekit": homekit,
            "timeout": str(timeout) if timeout else None,
            "delay": f'{int(delay.seconds)}s' if delay else None,
            "identifier": identifier
        }
        data = {key: value for key, value in data.items() if value}
        return self._perform_request("POST", "execute", data)

    def run_shortcut_from_server(self, name: str, input: Optional = None, timeout: Optional[float]=None,
                                 delay: datetime.timedelta=None, identifier: Optional[str] = None):
        return self.execute_automation_server_action(shortcut=name, input=input, timeout=timeout, delay=delay,
                                              identifier=identifier)

    def launch_homekit_scene(self, name: str, timeout: Optional[float]=None, delay: datetime.timedelta=None,
                             identifier: Optional[str] = None):
        return self.execute_automation_server_action(homekit=name, timeout=timeout, delay=delay, identifier=identifier)

    def cancel_server_action(self, identifier: str):
        return self._perform_request("POST", "cancelExecution", {"identifier": identifier})


class PushcutError(Exception):

    def __init__(self, message=""):
        self.message = message

    def __repr__(self):
        return self.message


class AutomationServerNotRunning(PushcutError):
    pass


class AutomationServerTimeout(PushcutError):
    pass
