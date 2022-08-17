from ccross import Solver, CMatrix


def print_col(matrix: CMatrix):
    print('Cols: \n')
    for cl in range(matrix.columns):
        print([w.string for w in matrix.column_words(cl)])


def main():
    Solver()
    print("Loading matrix..")
    matrix = CMatrix.from_text('schema/crossword.csv')
    print("Solving..")
    matrix: CMatrix = matrix.fill()
    matrix.solve(True)


if __name__ == '__main__':
    """
    Start the encrypted crosswords solver
    """
    main()
