"""Custom Exceptions."""

"""We aren't doing anything special here. Now, that questions the existence of these classes itself."""

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
