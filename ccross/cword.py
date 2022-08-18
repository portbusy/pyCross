import typing

from .ccell import CCell


class CWord:

    """
    Handles the operations words inside each row and column
    """

    def __init__(self, cells: typing.List[CCell]):
        self._cells: typing.List[CCell] = cells

    def __repr__(self):
        return self.string

    @property
    def length(self) -> int:
        return len(self.string)

    @property
    def is_solved(self) -> bool:
        return CCell.unknown not in self.string

    @property
    def unsolved_chars(self) -> int:
        return self.string.count(CCell.unknown)

    @property
    def unsolved_indexes(self) -> typing.Dict[int, int]:
        return {i: c.number for i, c in enumerate(self._cells) if c.letter == CCell.unknown}

    @classmethod
    def from_chars(cls, chars: typing.List[typing.Union[int, tuple]]):
        return cls([CCell(i) if isinstance(i, int) else CCell(i[0], i[1]) for i in chars])

    @property
    def string(self):
        """
        Returns the letter assigned to the cell.
        :return:
        """
        return ''.join([c.letter for c in self._cells])

    def find(self, string: str):
        dd = dict()
        for i, char in enumerate(string):
            cell = self._cells[i]
            if cell.letter == CCell.unknown:
                dd[cell.number] = string[i]
        return dd
