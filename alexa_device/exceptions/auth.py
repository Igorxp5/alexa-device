from requests import Response

class CodePairError(RuntimeError):
    def __init__(self, response: Response):
        super().__init__(response)


class AccessGrantError(RuntimeError):
    def __init__(self, response: Response):
        super().__init__(response)


class MissingCodePair(RuntimeError):
    def __init__(self):
        super().__init__('Request code pair before requesting the access token')
