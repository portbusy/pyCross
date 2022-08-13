import fnmatch
from c_matrix.module import CMatrix
import numpy as np


def print_rows(c: CMatrix):
    print('\nrows: \n')
    for r in range(c.rows):
        print([word.string for word in c.read_row_words(r)])


def print_col(c: CMatrix):
    print('\ncols: \n')
    for cl in range(c.columns):
        print([word.string for word in c.read_column_words(cl)])


if __name__ == '__main__':
    """
    Start the encrypted crosswords solver
    """
    c = CMatrix.from_text()
    c = c.fill()
    # c.fill_from_random_letters()
    with open('words/280000_parole_italiane.txt') as words:
        lines = words.readlines()
        matrix_rows = c.find_easiest_words()
        for word in matrix_rows:
            print(word.string)
            matches = fnmatch.filter([line.replace('\n', '') for line in lines], word.string)
            for match in matches:
                result = word.find(match)
                if any([x in c.mapped_letters for x in result.values()]):
                    pass
                else:
                    print(f'Result: {result} :)')
                    branch_c = c.copy_matrix()
                    for k, v in result.items():
                        branch_c.fill_number(k, v)
                    print_rows(branch_c)
