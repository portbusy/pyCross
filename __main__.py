from ccross import Solver, CMatrix


def print_col(matrix: CMatrix):
    print('Cols: \n')
    for cl in range(matrix.columns):
        print([w.string for w in matrix.column_words(cl)])


def main():
    solver = Solver()
    solver.init()
    solver.solve('schema/crossword.csv', True)


if __name__ == '__main__':
    """
    Start the encrypted crosswords solver
    """
    main()
