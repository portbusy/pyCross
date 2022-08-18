import typing

from .cmatrix import CMatrix


class Solver:

    def __init__(self, vocabulary: typing.List[str], should_type: bool=False):
        """
        Solver of Encrypted-Crosswords.
        :param vocabulary: List of the valid vocabulary words.
        :param should_type: Check whether the user should type for recognitions or word solving.
        """
        self._vocabulary: typing.List[str] = vocabulary
        self._should_type = should_type

    def solve(self, file_path: str):
        matrix = CMatrix.from_text(file_path, self)
        print("Filling matrix..")
        matrix.fill()
        print("Solving..")
        solution = matrix.solve()
        if solution:
            print("\nSolution found:")
            solution.print()
        else:
            print("\nNo solution found.")

    @property
    def vocabulary(self) -> typing.List[str]:
        return self._vocabulary

    @property
    def should_type(self) -> bool:
        return self._should_type
