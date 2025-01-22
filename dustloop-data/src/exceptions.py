class CliException(Exception):
    """An exception occurred in the CLI code"""
    exit_code = 1

    def __init__(self, message: str, url: str, error: str) -> None:
        super().__init__(message)
        self.url = url
        self.error = error

    def __str__(self):
        return f"{super().__str__()}\nurl: {self.url}\nerrorRsp: {self.error}"


