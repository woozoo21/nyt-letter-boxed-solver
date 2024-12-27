import pathlib   #for file paths
from typing import Dict
from app_types import WordSeq
from word import Word

class Words:
    words: list[Word]   # list of all valid Words

    def __init__(self, letter_groups: str) -> None:
        def find_paths(letters: str) -> Dict[str, str]:
            'Creates dictionary that maps each letter to the letters it can make'

            def other_group_letters(group: str) -> str:
                return ''.join(gl for gl in grouped_letters if gl != group)
            'Removes a group of letters and returns letters of other groups' #'abc' → 'defghijkl'

            grouped_letters: list[str] = letters.split() #['abc', 'def', 'ghi', 'jkl']
            return {letter: other_group_letters(group)
                    for group in grouped_letters for letter in group}

        def word_works(word: str) -> bool:   # Iterates through each consecutive pair of letters in the word
            for i in range(len(word) - 1):
                letter = word[i]
                next_letter = word[i + 1]
                if not (ok_next_letters := paths.get(letter)):
                    return False
                if next_letter not in ok_next_letters:
                    return False
            return True

        paths: Dict[str, str] = find_paths(letter_groups)
        all_words = pathlib.Path('resources/words.txt').read_text().strip().split('\n')  # loads words from words.txt
        candidate_words = list(filter(word_works, all_words))    # filter words that pass the word_works check

        print(f'{len(candidate_words):,} candidate words loaded from list of {len(all_words):,} words')

        self.words = list(map(Word.create, candidate_words))   # Converts valid words into Word objects
        self.words.sort(key=lambda word: word.num_unique_letters, reverse=True)    #Sorts them by the number of unique letters; most unique letters first

    def best_words_for_needed_letters(self, needed_letters: set[str]) -> WordSeq:   # Finds the best words that use the most needed letters
        def num_needed_letters(word: Word):
            return len(word.unique_letters.intersection(needed_letters))  # Computes how many needed letters each word contains

        num_needed_letters_and_words: list[tuple[int, Word]] = [     # Sorts the words in descending order of the needed letters
            (num_needed_letters(word), word) for word in self.words]
        num_needed_letters_and_words.sort(reverse=True)
        return [lw[1] for lw in num_needed_letters_and_words]