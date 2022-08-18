import typing

from .cmatrix import CMatrix


class Solver:

    def __init__(self):
        self._loaded: typing.List[str] = list()
        self._should_type = True

    def init(self):
        print("Loading vocabulary..")
        languages = ['it', 'en']
        for lang in languages:
            with open(f'words/{lang}.txt') as f:
                self._loaded += [x.replace('\n', '').lower() for x in f.readlines()]

    def solve(self, file_path: str, should_type: bool=False):
        c_matrix = CMatrix.from_text(file_path, self)
        print("Filling matrix..")
        c_matrix.fill()
        print("Solving..")
        solution = c_matrix.solve(should_type)
        if solution:
            print("\nSolution found:")
            solution.print()
        else:
            print("\nNo solution found.")

    @property
    def vocabulary(self) -> typing.List[str]:
        return self._loaded
