"""Error in user inputs."""


class InvalidCliInputError(Exception):
    """Invalid CLI arguments error."""

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message (str): Error message to be displayed.
        """
        self.message = message
        super().__init__(self.message)
