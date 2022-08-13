import typing

from cell.module import Cell


class CWord:

    """
    Handles the operations words inside each row and column
    """

    def __init__(self, cells: typing.List[Cell]):
        self._cells: typing.List[Cell] = cells

    @classmethod
    def from_chars(cls, chars: typing.List[typing.Union[int, tuple]]):
        return cls([Cell(i) if isinstance(i, int) else Cell(i[0], i[1]) for i in chars])

    @property
    def string(self):
        """
        Returns the letter assigned to the cell
        N.B.: '*' is used as placeholder
        :return:
        """
        return ''.join([c.letter for c in self._cells])

    def find(self, string: str):
        dd = dict()
        for i, char in enumerate(string):
            cell = self._cells[i]
            if cell.letter == '?':
                dd[cell.number] = string[i]
        return dd
