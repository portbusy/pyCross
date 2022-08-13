

class Cell:

    """
    Handles the cell-related logic
    """

    def __init__(self, number: int, letter: str = '?'):
        """

        :param number:
        :param letter:
        """
        self._number = number
        self._letter = letter

    @property
    def letter(self) -> str:
        return self._letter

    @letter.setter
    def letter(self, letter: str):
        self._letter = letter

    @property
    def number(self) -> int:
        return self._number

    def is_assigned(self) -> bool:
        return self._letter != '*'
