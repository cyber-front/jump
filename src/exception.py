# File: exception.py
#
# Description: Contains an exception class for the puzzle


class PuzzleException(Exception):
    """
    Exception to indicate there is an error in the configuration
    which was detected while the
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
