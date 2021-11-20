from typing import Optional, List


class NotificationAction:
    """
    Refer to https://www.pushcut.io/webapi.html for description of parameters
    """

    @classmethod
    def urlBackgroundOptions(cls, httpMethod: Optional[str] = None, httpContentType: Optional[str] = None,
                             httpHeader: Optional[List[dict]] = None, httpBody: Optional[str] = None):
        return {key: value for key, value in locals().items() if value}

    def __init__(self,
                 name: Optional[str] = None, input: Optional[str] = None, keepNotification: Optional[bool] = None,
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
    """
    Refer to https://www.pushcut.io/webapi.html for description of parameters
    """

    def __init__(self,
                 title: Optional[str] = None, text: Optional[str] = None, sound: Optional[str] = None,
                 image: Optional[str] = None, input: Optional[str] = None, defaultAction: Optional[NotificationAction] = None,
                 actions: Optional[List[NotificationAction]] = None, devices: Optional[List[str]] = None):

        actions = [] if actions is None else actions
        devices = [] if devices is None else devices

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