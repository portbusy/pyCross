from ccross import Solver


def main():
    print("Loading vocabulary..")
    vocabulary = list()
    for lang in ['it', 'en']:
        with open(f'words/{lang}.txt') as f:
            vocabulary += [x.replace('\n', '').lower() for x in f.readlines()]
    solver = Solver(vocabulary, should_type=True)
    solver.solve('schema/crossword.csv')


if __name__ == '__main__':
    main()
