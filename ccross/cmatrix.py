import copy
import typing

import numpy
import fnmatch

from .cword import CWord
from .ccell import CCell


class SolverInstance:

    def __init__(self, solver):
        self._solver = solver
        self._recognized = list()
        self._unrecognized = list()
        self._unsolvable = list()
        self._wrong_vectors: typing.List[str] = list()

    @staticmethod
    def _make_vector(pairs: typing.Dict[int, str]) -> str:
        return "".join([f'{k}{v}' for k, v in sorted(pairs.items(), key=lambda x: x[0])])

    def add_wrong(self, pairs: typing.Dict[int, str]):
        self._wrong_vectors.append(self._make_vector(pairs))

    def is_wrong(self, pairs: typing.Dict[int, str]) -> bool:
        return self._make_vector(pairs) in self._wrong_vectors

    @property
    def vocabulary(self) -> typing.List[str]:
        return self._solver.vocabulary + self._recognized

    def matches(self, string: str) -> typing.List[str]:
        return list(set(fnmatch.filter(self.vocabulary, string)))

    def contains(self, string: str) -> bool:
        return string in self.vocabulary

    def ask(self, string: str) -> bool:
        if not self._solver.should_type or string in self._unrecognized:
            return False
        answer = input(f"- Do you recognize the word '{string}'? (Y/N) ")
        if answer.lower() == 'y':
            self._recognized.append(string)
            return True
        self._unrecognized.append(string)
        return False

    def require(self, word_to_solve: str) -> bool:
        if not self._solver.should_type:
            return False
        string = word_to_solve.replace(CCell.unknown, '*')
        if string in self._unsolvable:
            return False
        answer = input(f"- Can you solve the word '{string}'? (leave empty to skip) ")
        if answer:
            self._recognized.append(answer.lower())
            return True
        else:
            self._unsolvable.append(string)
            return False


class CMatrix:
    """ Handles the operations on the crossword.csv (rows and columns). """

    _min_word = 3

    def __init__(self, matrix: numpy.ndarray, instance: SolverInstance, parent=None):
        self._np_matrix = matrix
        self._instance: SolverInstance = instance
        self._random_mapping: typing.Dict = dict()
        self._parent = parent

    @property
    def depth(self) -> int:
        if self._parent:
            return self._parent.depth + 1
        return 0

    @classmethod
    def from_text(cls, file_name: str, solver):
        print("Loading matrix from text..")
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
        return cls(numpy.array(matrix), SolverInstance(solver))

    def copy(self):
        return CMatrix(copy.deepcopy(self._np_matrix), self._instance, self)

    @property
    def rows(self):
        return len(self._np_matrix[0, :])

    @property
    def columns(self):
        return len(self._np_matrix[:, 0])

    @staticmethod
    def _read_words(words_array: typing.List[CCell]):
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
        """ Get mapped number-letters. """
        return {c.number: c.letter for r in self._np_matrix for c in r if c is not None and c.is_solved}

    @property
    def mapped_letters(self) -> typing.List[str]:
        """ Get mapped letters only. """
        return list(self.mapped.values())

    @property
    def unmapped(self) -> typing.List:
        """ Get unmapped numbers only. """
        return list(set(c.number for r in self._np_matrix for c in r if c is not None and c.is_solved))

    @staticmethod
    def _fill_number(matrix: numpy.ndarray, number: int, letter: str):
        for r in matrix:
            for c in r:
                if c and c.number == number:
                    c.letter = letter

    def fill(self):
        """ Fill the matrix with already filled matches. """
        for k, v in self.mapped.items():
            self._fill_number(self._np_matrix, k, v)

    def fill_with(self, pairs: typing.Dict[int, str]):
        """ Fill the matrix with given number-letter pairs. """
        for k, v in pairs.items():
            self._fill_number(self._np_matrix, k, v)

    def next_word(self) -> CWord:
        """ Get the next word to solve. """
        crossword_words = dict()
        for word in self.row_words() + self.column_words():
            if not word.is_solved and word.length > self._min_word:
                crossword_words[word] = word.unsolved_chars
        sorted_words = {k: v for k, v in sorted(crossword_words.items(), key=lambda x: x[1])}
        words = [k for k, v in sorted_words.items() if v == min(sorted_words.values())]
        words = list(sorted(words, key=lambda x: x.length, reverse=True))
        if words: return words[0]

    def has_match(self, pairs: typing.Dict[int, str]) -> bool:
        """ Check if the matrix already has the given number-letter match pairs. """
        for x in pairs.values():
            if x in self.mapped_letters:
                return True
        return False

    def _word_has_sense(self, w: CWord) -> bool:
        """ Check if a word can have sense or if it exists in the vocabulary. """
        return w.length <= self._min_word or not w.is_solved or self._instance.contains(w.string)

    def has_sense(self) -> bool:
        """ Check if the matrix words has sense, also by asking to the solver, if required. """
        for word in self.row_words() + self.column_words():
            if not self._word_has_sense(word):
                return self._instance.ask(word.string)
        return True

    def _r_find_matches(self, word: CWord):
        def _can_match(s: str):
            return ll == len(set([s[i] for i in word.unsolved_indexes]))
        ll = len(word.unsolved_indexes)
        matches = [s for s in self._instance.matches(word.string) if _can_match(s)]
        if not matches and self._instance.require(word.string):
            matches = self._r_find_matches(word)
        return matches

    def solve(self):
        """ Solve the matrix and return the solved branch, if any. """
        # Find next word to solve
        word_to_solve = self.next_word()
        # Check for matches with the word to solve, otherwise this is a wrong branch matrix
        matches = self._r_find_matches(word_to_solve)
        # If there is not match, get back
        print(f'{self.depth+1}) Solving: {word_to_solve}')
        # For each matching word
        branches: typing.Dict[str, CMatrix] = dict()
        for match in matches:
            # Find the match pairs for the match on the word to solve
            match_pairs = word_to_solve.find(match)
            # If the matrix does not contain any of the match pairs
            if not self.has_match(match_pairs) and not self._instance.is_wrong(match_pairs):
                # We might have a matrix branch to deepen
                branch = self.copy()
                # Fill the match pairs in the matrix branch
                branch.fill_with(match_pairs)
                branches[match] = branch
        # Check branches by correctness
        branches = {k: v for k, v in sorted(branches.items(), key=lambda x: x[1].correctness)}
        for match, branch in branches.items():
            # If the solved words in the matrix make sense
            if branch.has_sense():
                # If the branch is solved, return the branch as the solution
                if branch.is_solved:
                    return branch
                else:
                    # Keep solving in depth and return the solution, if any
                    solution = branch.solve()
                    if solution:
                        return solution
            else:
                self._instance.add_wrong(word_to_solve.find(match))

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
                if word.is_solved and word.string in self._instance.vocabulary:
                    points += word.length
        return round(points / max_points, ndigits=3)
