from requests import Response

class PushcutAPIException(Exception):

    def __init__(self, status_code, message):
        self.message = message
        self.status_code = status_code

    def __repr__(self):
        return f"Error with http status code {self.status_code}: {self.message}"


class PushcutAutomationServerNotRunning(PushcutAPIException):
    pass


class PushcutAutomationServerTimeout(PushcutAPIException):
    pass


class PushcutUnauthorisedError(PushcutAPIException):
    pass


class PushcutBadRequestError(PushcutAPIException):
    pass


class PushcutNotFoundError(PushcutAPIException):
    pass


class PushcutSubscriptionRequiredError(PushcutAPIException):
    pass


def raise_pushcut_api_exception(http_response: Response):
    status_code = http_response.status_code

    try:
        message = http_response.json()['error']
    except Exception as e:
        message = http_response.text

    if status_code == 401:
        raise PushcutUnauthorisedError(status_code, message)
    elif status_code == 400:
        raise PushcutBadRequestError(status_code, message)
    elif status_code == 404:
        raise PushcutNotFoundError(status_code, message)
    elif status_code == 502:
        raise PushcutAutomationServerNotRunning(status_code, message)
    elif status_code == 504:
        raise PushcutAutomationServerTimeout(status_code, message)
    elif status_code == 402:
        raise PushcutSubscriptionRequiredError(status_code, message)
    else:
        raise PushcutAPIException(status_code, message)