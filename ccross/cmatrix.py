import typing
import copy

import numpy

from .cword import CWord
from .ccell import CCell
from .csolver import Solver


class CMatrix:
    """ Handles the operations on the crossword.csv (rows and columns). """

    _min_word = 3

    def __init__(self, matrix: numpy.ndarray, parent=None):
        self._np_matrix = matrix
        self._random_mapping: typing.Dict = dict()
        self._parent = parent

    @property
    def depth(self) -> int:
        if self._parent:
            return self._parent.depth + 1
        return 0

    @classmethod
    def from_text(cls, file_name: str):
        with open(file_name) as c_file:
            matrix = []
            for line in c_file.readlines():
                cells = []
                for char_symbol in line.replace('\n', '').split(';'):
                    if char_symbol in ['#', '']:
                        cells.append(None)
                    else:
                        char = eval(char_symbol)
                        cells.append(CCell(char[0], char[1]) if isinstance(char, tuple) else CCell(char))
                matrix.append(cells)
        np_matrix = numpy.array(matrix)
        return cls(np_matrix)

    def copy(self):
        return CMatrix(copy.deepcopy(self._np_matrix), self)

    @property
    def rows(self):
        return len(self._np_matrix[0, :])

    @property
    def columns(self):
        return len(self._np_matrix[:, 0])

    @staticmethod
    def _read_words(words_array: typing.List[CCell]):
        """
        :param words_array:
        :return:
        """
        cells: typing.List[CCell] = list()
        word_list: typing.List[CWord] = list()
        for cell in words_array:
            if cell is not None:
                cells.append(cell)
            else:
                word_list.append(CWord(cells))
                cells = list()
        if cells:
            word_list.append(CWord(cells))
        return word_list

    def row_words(self, index: int=None) -> typing.List[CWord]:
        """ Get the words in the rows. """
        words = list()
        if index is None:
            _min, _max = 0, self.rows
        else:
            _min, _max = index, index + 1
        for i in range(_min, _max):
            words += self._read_words(self._np_matrix[i, :].tolist())
        return words

    def column_words(self, index: int=None):
        """ Get words in the columns. """
        words = list()
        if index is None:
            _min, _max = 0, self.rows
        else:
            _min, _max = index, index + 1
        for i in range(_min, _max):
            words += self._read_words(self._np_matrix[:, i].tolist())
        return words

    @property
    def mapped(self) -> typing.Dict[int, str]:
        return {cell.number: cell.letter for row in list(self._np_matrix)
                for cell in row if cell is not None and cell.is_solved}

    @property
    def mapped_letters(self) -> typing.List[str]:
        return list(self.mapped.values())

    @property
    def unmapped(self) -> typing.List:
        return list(set([cell.number for row in list(self._np_matrix)
                         for cell in row if cell is not None and cell.is_solved]))

    @staticmethod
    def _fill_number(matrix: numpy.ndarray, number: int, letter: str):
        for row in matrix:
            for cell in row:
                if cell and cell.number == number:
                    cell.letter = letter

    def fill(self):
        np_matrix_copy: numpy.ndarray = numpy.copy(self._np_matrix)
        for k, v in self.mapped.items():
            self._fill_number(np_matrix_copy, k, v)
        return CMatrix(np_matrix_copy)

    def fill_with(self, pairs: typing.Dict[int, str]):
        for k, v in pairs.items():
            self._fill_number(self._np_matrix, k, v)

    def next_word(self) -> CWord:
        crossword_words = dict()
        for word in self.row_words() + self.column_words():
            if not word.is_solved and word.length > self._min_word:
                crossword_words[word] = word.unsolved_chars
        sorted_words = {k: v for k, v in sorted(crossword_words.items(), key=lambda x: x[1])}
        words = [k for k, v in sorted_words.items() if v == min(sorted_words.values())]
        words = list(sorted(words, key=lambda x: x.length, reverse=True))
        if words: return words[0]

    def contains(self, match_pairs: dict) -> bool:
        for x in match_pairs.values():
            if x in self.mapped_letters:
                return True
        return False

    def has_sense(self, should_type: bool=False) -> bool:
        for word in self.row_words() + self.column_words():
            if word.length > self._min_word and word.is_solved and not Solver().contains(word.string):
                if self.depth > self._min_word:
                    if should_type:
                        return Solver().ask(word.string)
                    return False
        return True

    def close(self):
        print("\nSolution found:")
        self.print()
        exit()

    def solve(self, should_type: bool=False):
        # Check if is solved
        if self.is_solved:
            self.close()
        # Find next word to solve
        word_to_solve = self.next_word()
        # Find word matches
        matches = word_to_solve.find_matches()
        # If there is no match for the word to solve, this is a wrong branch
        if not matches:
            if should_type and Solver().require(word_to_solve.string):
                matches = word_to_solve.find_matches()
        # Find matches of the word to solve
        print(f'{self.depth+1}) Solving: {word_to_solve}')
        # For each matching word
        branches: typing.Dict[str, CMatrix] = dict()
        for match in matches:
            # Find the match pairs for the match on the word to solve
            match_pairs = word_to_solve.find(match)
            # TODO: Check if the solution is a valid one by verifying if the solution array does not belong to
            #  the possible solution domain.
            # If the matrix does not contain any of the match pairs
            if not self.contains(match_pairs):
                # We might have a matrix branch to deepen
                branch = self.copy()
                # Fill the match pairs in the matrix branch
                branch.fill_with(match_pairs)
                branches[match] = branch
        # Check branches by correctness
        branches = {k: v for k, v in sorted(branches.items(), key=lambda x: x[1].correctness)}
        for match, branch in branches.items():
            # If the solved words in the matrix makes no sense, return
            if branch.has_sense(should_type):
                # Keep solving in depth
                branch.solve(should_type)

    def _print_line(self):
        print('\t'.join(['-' for i in range(self.rows)]))

    def print(self):
        self._print_line()
        for row in self._np_matrix:
            print('\t'.join([c.letter if c else chr(9608) for c in row]))
        self._print_line()
        print()

    @property
    def is_solved(self):
        for word in self.row_words():
            if word.length > self._min_word and not word.is_solved:
                return False
        return True

    @property
    def correctness(self) -> float:
        points = 0
        max_points = 0
        for word in self.row_words() + self.column_words():
            if word.length > self._min_word:
                max_points += word.length
                if word.is_solved and word.string in Solver().vocabulary:
                    points += word.length
        return round(points / max_points, ndigits=3)
