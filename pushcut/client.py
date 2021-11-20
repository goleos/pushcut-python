import requests
import datetime
from typing import Optional, List, Union
import json
from pushcut.exceptions import raise_pushcut_api_exception
from pushcut.notifications import Notification


class Client:
    """
    A client to interact with the Pushcut app API as documented on https://www.pushcut.io/webapi.html

    Further help resources are available here: https://www.pushcut.io/support.html

    Create a client instance as follows:

        >>> import pushcut
        >>> client = pushcut.Client(api_key="super-secret key", default_notification_name="My First Notification")

    :param api_key: you can obtain an API key under the 'Integrations' tab of the pushcut app. This is not the same
        as webhook secret
    :param default_notification_name: this is the name (identifier) of a notification from your list of
        notifications that you want to use as a template when sending a customised notification
    """

    def __init__(self, api_key: str, default_notification_name: Optional[str]=None):
        self.api_key = api_key
        self.home_endpoint = f"https://api.pushcut.io/v1"
        self.default_notification_name = default_notification_name
        self.headers = {"API-Key": api_key, "Accept": "application/json"}

    def _perform_request(self, method: str, target: str, json_data: Optional) -> str:
        response = requests.request(method=method, url=f"{self.home_endpoint}/{target}", json=json_data,
                                   headers=self.headers)
        print(json_data)
        status_code = response.status_code
        info = response.text
        if 200 <= status_code <= 299:
            return info
        else:
            raise_pushcut_api_exception(response)

    def devices(self) -> List[dict]:
        """Returns a list of devices currently connected to the pushcut account"""
        return json.loads(self._perform_request("GET", "devices", None))

    def notifications(self) -> List[dict]:
        """Returns the list of notifications currently enabled in the pushcut account"""
        return json.loads(self._perform_request("GET", "notifications", None))

    def trigger_notification(self, name: str) -> str:
        """
        Triggers the given notifications from the list of notifications in your pushcut account
        :param name: name of the notification you want to trigger
        :return: response of the http request as a string
        """
        return self.send_notification(Notification(), notification_name=name)

    def send_notification(self, notification: Notification, notification_name: Optional[str]=None) -> str:
        """
        Allows to customise each aspect of the notification you want to send such as title, text, sound etc.
        :param notification: a :class:`Notification` object with customised attributes
        :param notification_name: name of one of the available notifications in your pushcut account. If none is
            provided, the `default_notification_name` is used instead
        :return: response of the http request as a string
        """
        if not notification_name:
            notification_name = self.default_notification_name
        return self._perform_request("POST", f"notifications/{notification_name}", notification.as_dict())

    def execute_action(self,
                       shortcut: Optional[str] = None, input: Optional = None, homekit: Optional[str] = None,
                       timeout: Union[int, str, None]=None, delay: Union[datetime.timedelta, str, None]=None,
                       identifier: Optional[str] = None) -> str:
        """
        Tells Pushcut Automation Server to execute either a shortcut or a homekit scene
        :param shortcut: name of shortcut you want to execute (must be enabled in the app)
        :param input: input you want to pass to the shortcut (not valid if used with homekit scene)
        :param homekit: name of homekit scene you want to execute
        :param timeout: time in seconds to wait for completion of execution before giving up on the request. Note that
            an action may still be completed even if timeout has passed
        :param delay: delay execution of an the action. Can either be a :class:`datetime.timedelta` or :type:`str`.
            NOTE: you must have Pushcut Server Extended to use this parameter
        :param identifier: id of this action to be used if you want to cancel a scheduled action in the future
        :return: response of the http request as a string
        """
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
                     delay: Union[datetime.timedelta, str, None]=None, identifier: Optional[str] = None) -> str:
        """
        Tells Pushcut Automation Server to execute a shortcut
        :param name: name of shortcut you want to execute (must be enabled in the app)
        :param input: input you want to pass to the shortcut (not valid if used with homekit scene)
        :param timeout: time in seconds to wait for completion of execution before giving up on the request. Note that
            an action may still be completed even if timeout has passed
        :param delay: delay execution of an the action. Can either be a :class:`datetime.timedelta` or :type:`str`.
            NOTE: you must have Pushcut Server Extended to use this parameter
        :param identifier: identifier: id of this action to be used if you want to cancel a scheduled action in the
            future
        :return: response of the http request as a string
        """
        return self.execute_action(shortcut=name, input=input, timeout=timeout, delay=delay,
                                   identifier=identifier)

    def launch_homekit_scene(self, name: str, timeout: Optional[float]=None, delay: datetime.timedelta=None,
                             identifier: Optional[str] = None) -> str:
        """
        Tells Pushcut Automation Server to execute a homekit scene
        :param name: name of homekit scene you want to execute
        :param timeout: time in seconds to wait for completion of execution before giving up on the request. Note that
            an action may still be completed even if timeout has passed
        :param delay: delay execution of an the action. Can either be a :class:`datetime.timedelta` or :type:`str`.
            NOTE: you must have Pushcut Server Extended to use this parameter
        :param identifier: identifier: id of this action to be used if you want to cancel a scheduled action in the
            future
        :return: response of the http request as a string
        """
        return self.execute_action(homekit=name, timeout=timeout, delay=delay, identifier=identifier)

    def cancel_server_action(self, identifier: str) -> str:
        """
        Tells Pushcut Automation Server to cancel a previously scheduled shortcut or homekit scene
        :param identifier: the id you gave to the action when scheduling it
        :return: response of the http request as a string
        """
        return self._perform_request("POST", "cancelExecution", {"identifier": identifier})
