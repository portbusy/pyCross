class CCell:

    """
    Handles the cell-related logic
    """

    unknown = '?'

    def __init__(self, number: int, letter: str = unknown):
        """

        :param number:
        :param letter:
        """
        self._number = number
        self._letter = letter

    def __repr__(self):
        return self._letter

    def __copy__(self):
        return CCell(self._number, self._letter)

    @property
    def letter(self) -> str:
        return self._letter

    @letter.setter
    def letter(self, letter: str):
        self._letter = letter

    @property
    def number(self) -> int:
        return self._number

    @property
    def is_solved(self) -> bool:
        return self._letter != self.unknown

