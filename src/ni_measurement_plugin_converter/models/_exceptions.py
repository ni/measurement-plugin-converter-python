"""Custom Exceptions."""


class InvalidCliArgsError(Exception):
    """Invalid CLI arguments error."""

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message (str): Error message.
        """
        super().__init__(message)


class UnsupportedDriverError(Exception):
    """Unsupported driver error."""

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message (str): Error message.
        """
        super().__init__(message)
