"""Custom Exceptions."""


class InvalidCliInputError(Exception):
    """Invalid CLI arguments error."""

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message (str): Error message to be displayed.
        """
        self.message = message
        super().__init__(self.message)


class InvalidMeasUIError(Exception):
    """Invalid measurement UI file error."""

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__()
