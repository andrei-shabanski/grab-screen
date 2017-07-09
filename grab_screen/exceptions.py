class Error(Exception):
    default_message = "Oops, something went wrong"

    def __init__(self, message=None):
        super(Error, self).__init__(message)

        self.message = message or self.default_message

    def __str__(self):
        return self.message


class ScreenError(Error):
    pass


class StorageError(Error):
    pass
