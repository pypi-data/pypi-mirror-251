from requests.exceptions import RequestException


class ABPowerError(Exception):
    pass


class RequestError(ABPowerError):
    o = RequestException

    def __init__(self, msg: str, o: RequestException):
        super().__init__(msg)
        self.o = o


class ParseError(ABPowerError):
    o = Exception

    def __init__(self, msg: str, o: Exception):
        super().__init__(msg)
        self.o = o
