import random
import string
import typing

import numpy as np

from c_word.module import CWord
from cell.module import Cell


class CMatrix:
    """
    Handles the operations on the crossword.csv (rows and columns)
    """

    def __init__(self, matrix: np.ndarray):
        self._np_matrix = matrix
        self._random_mapping: typing.Dict = dict()

    @classmethod
    def from_text(cls):
        with open('crossword.csv', 'r') as c_file:
            matrix = list()
            for line in c_file.readlines():
                cells = list()
                for char_symbol in line.split(';'):
                    char_symbol = char_symbol.replace('\n', '')
                    if char_symbol == '#':
                        cells.append(None)
                    else:
                        char = eval(char_symbol)
                        if isinstance(char, tuple):
                            cells.append(Cell(char[0], char[1]))
                        else:
                            cells.append(Cell(char))
                matrix.append(cells)
        return cls(np.array(matrix))

    def copy_matrix(self):
        return CMatrix(self.copy())

    def copy(self):
        return np.copy(self._np_matrix)

    @property
    def rows(self):
        return len(self._np_matrix[0, :])

    @property
    def columns(self):
        return len(self._np_matrix[:, 0])

    @staticmethod
    def _read_words(words_array: typing.List[Cell]):
        """

        :param words_array:
        :return:
        """
        cells: typing.List[Cell] = list()
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

    def read_row_words(self, row_index: int):
        """

        :param row_index:
        :return:
        """
        return self._read_words(self._np_matrix[row_index].tolist())

    def read_column_words(self, col_index: int):
        """

        :param col_index:
        :return:
        """
        return self._read_words(self._np_matrix[:, col_index].tolist())

    @property
    def mapped(self) -> typing.Dict:
        return {cell.number: cell.letter for row in list(self._np_matrix)
                for cell in row if cell is not None and cell.letter != '?'}

    @property
    def mapped_letters_string(self) -> str:
        return ''.join(self.mapped_letters)

    @property
    def mapped_letters(self) -> list:
        return list(self.mapped.values())

    @property
    def unmapped(self) -> typing.List:
        return [cell.number for row in list(self._np_matrix)
                for cell in row if cell is not None and cell.letter == '?']

    def fill(self):
        np_matrix_copy: np.ndarray = np.copy(self._np_matrix)
        for k, v in self.mapped.items():
            self._fill_number(np_matrix_copy, k, v)
        return CMatrix(np_matrix_copy)

    def fill_number(self, number: int, letter: str):
        self._fill_number(self._np_matrix, number, letter)

    @staticmethod
    def _fill_number(matrix: np.ndarray, number: int, letter: str):
        for row in matrix:
            for cell in row:
                if cell and cell.number == number:
                    cell.letter = letter

    def fill_from_random_letters(self):
        unmapped_letters = [letter for letter in string.ascii_lowercase if letter not in self.mapped_letters_string]
        for number in self.unmapped:
            random_unmapped_letter = random.choice(unmapped_letters)
            self._random_mapping[number] = random_unmapped_letter
            self.fill_number(number=number, letter=random_unmapped_letter)

    def find_easiest_words(self) -> typing.List:
        crossword_words = dict()
        for row_index in range(self.rows):
            for word in self.read_row_words(row_index):
                if '?' in word.string and len(word.string) > 2:
                    crossword_words[word] = word.string.count('?')
        for col_index in range(self.columns):
            for word in self.read_column_words(col_index):
                if '?' in word.string and len(word.string) > 2:
                    crossword_words[word] = word.string.count('?')

        sorted_words = {k: v for k, v in sorted(crossword_words.items(), key=lambda item: item[1])}

        return [k for k, v in sorted_words.items() if v == min(sorted_words.values())]



