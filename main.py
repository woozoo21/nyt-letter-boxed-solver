import random
from typing import Set, Tuple
from word import Word
from words import Words
from app_types import WordSeq, StrSeq

class LetterBoxedSolver:
    def __init__(self, letter_groups: str) -> None:
        print(f'{LetterBoxedSolver.__name__} is ready to solve "{letter_groups}"')
        self.letters = letter_groups.replace(' ', '')
        self.words = Words(letter_groups)               # removes gaps

    def solve(self) -> StrSeq:   # Randomly selects a word from the best matches, prioritizng higher ranked words
        def randomly_choose_word(words: WordSeq) -> Word:
            num_words_to_choose_from = 20
            high = min(len(words), num_words_to_choose_from) - 1
            mode = -1  # 0 yields too few 0 values
            index = round(random.triangular(0, high, mode))
            return words[index]

        letters_needed = set(self.letters)
        selected_words = []
        first_letter = None    # keeps track of selected words and the first letter of the next word

        while letters_needed and len(selected_words) < 7: # limits to 7 words max
            words: WordSeq = self.words.best_words_for_needed_letters(letters_needed) # Finds the best words for the remaining needed letters

            def connects_to_previous(word: Word) -> bool:
                return not first_letter or word.text[0] == first_letter  # Sorts words that connect to the previous word; if any

            connectable_words = list(filter(connects_to_previous, words))
            word = randomly_choose_word(connectable_words)
            selected_words.append(word.text)
            letters_needed.difference_update(word.unique_letters)
            first_letter = word.text[-1]      # randomly selects and updates the letters_needed and sequence of seleccted words
        return selected_words

    def solve_multiple(self, num_runs) -> StrSeq:
        random.seed(1)  # Get consistent results despite randomness

        unique_solutions: Set[Tuple[str]] = set(
            tuple(self.solve()) for _ in range(num_runs))
        lengths_and_solutions: list[tuple[int, tuple[str]]] = [
            (len(''.join(solution)), solution)
            for solution in unique_solutions]
        lengths_and_solutions.sort()  # Fewer letters is better
        print(f'{len(lengths_and_solutions):,} unique solutions found in {num_runs:,} runs')
        solutions: StrSeq = list(map(lambda ls: ls[1], lengths_and_solutions))
        return solutions


if __name__ == '__main__':
    solver = LetterBoxedSolver('ryl pqf aeo bui')
    solutions = solver.solve_multiple(100)
    print('\n'.join([' ➟ '.join(solution) for solution in solutions[:10]]))