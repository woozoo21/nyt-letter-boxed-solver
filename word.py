from typing import NamedTuple, Set

class Word(NamedTuple):
    text: str                  # apple
    unique_letters: Set[str]   # {a, p, p, l ,e}
    num_unique_letters: int    # non repeated words - a,p,l,e

    @staticmethod              
    def create(text: str):
        unique_letters = set(text)   # converts the word into a set of unique letters
        return Word(text, unique_letters, len(unique_letters))   