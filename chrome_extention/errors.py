class ChromeExtError(Exception):
    """An exception to be raised when an error is found."""

    def __init__(self, message=None, error_code=None):
        """Constructor.

        :param str message: The error message with info about what went wrong
        :param str error_code: The error code
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
