import fnmatch
import typing

from .ccell import CCell
from .utils import Singleton


@Singleton
class Solver:

    def __init__(self):
        print("Loading vocabulary..")
        self._loaded: typing.List[str] = list()
        languages = ['it', 'en']
        for lang in languages:
            with open(f'words/{lang}.txt') as f:
                self._loaded += [x.replace('\n', '').lower() for x in f.readlines()]
        self._recognized = list()
        self._unrecognized = list()
        self._unsolvable = list()
        self._should_type = True

    @property
    def vocabulary(self):
        return self._loaded + self._recognized

    def match(self, string: str) -> bool:
        return list(set(fnmatch.filter(self.vocabulary, string)))

    def contains(self, string: str) -> bool:
        return string in self.vocabulary

    def ask(self, string: str) -> bool:
        if string in self._unrecognized:
            return False
        answer = input(f"- Do you recognize the word '{string}'? (Y/N) ")
        if answer.lower() == 'y':
            self._recognized.append(string)
            return True
        self._unrecognized.append(string)
        return False

    def require(self, word_to_solve: str):
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
