import requests
import datetime
from typing import Optional, List, Union
import json
from pushcut.exceptions import raise_pushcut_api_exception
from pushcut.notifications import Notification


class Client:

    def __init__(self, api_key: str, default_notification_name: Optional[str]=None):
        self.api_key = api_key
        self.home_endpoint = f"https://api.pushcut.io/v1"
        self.default_notification_name = default_notification_name
        self.headers = {"API-Key": api_key, "Accept": "application/json"}

    def _perform_request(self, method: str, target: str, json_data: Optional) -> str:
        response = requests.request(method=method, url=f"{self.home_endpoint}/{target}", json=json_data,
                                   headers=self.headers)
        status_code = response.status_code
        info = response.text
        if 200 <= status_code <= 299:
            return info
        else:
            raise_pushcut_api_exception(response)

    def devices(self) -> List[dict]:
        return json.loads(self._perform_request("GET", "devices", None))

    def notifications(self) -> List[dict]:
        return json.loads(self._perform_request("GET", "notifications", None))

    def trigger_notification(self, name: str):
        return self.send_notification(Notification(), notification_name=name)

    def send_notification(self, notification: Notification, notification_name: Optional[str]=None):
        if not notification_name:
            notification_name = self.default_notification_name
        return self._perform_request("POST", f"notifications/{notification_name}", notification.as_dict())

    def execute_action(self,
                       shortcut: Optional[str] = None, input: Optional = None, homekit: Optional[str] = None,
                       timeout: Union[int, str, None]=None, delay: Union[datetime.timedelta, str, None]=None,
                       identifier: Optional[str] = None):
        data = {
            "shortcut": shortcut,
            "input": input,
            "homekit": homekit,
            "timeout": str(timeout) if isinstance(timeout, int or float) else timeout,
            "delay": f'{int(delay.seconds)}s' if isinstance(delay, datetime.timedelta) else delay,
            "identifier": identifier
        }
        data = {key: value for key, value in data.items() if value}
        return self._perform_request("POST", "execute", data)

    def run_shortcut(self, name: str, input: Optional = None, timeout: Optional[float]=None,
                     delay: Union[datetime.timedelta, str, None]=None, identifier: Optional[str] = None):
        return self.execute_action(shortcut=name, input=input, timeout=timeout, delay=delay,
                                   identifier=identifier)

    def launch_homekit_scene(self, name: str, timeout: Optional[float]=None, delay: datetime.timedelta=None,
                             identifier: Optional[str] = None):
        return self.execute_action(homekit=name, timeout=timeout, delay=delay, identifier=identifier)

    def cancel_server_action(self, identifier: str):
        return self._perform_request("POST", "cancelExecution", {"identifier": identifier})
