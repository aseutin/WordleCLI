"""
The model maintains the game's state in the simplest way possible.
"""
import enum

from datetime import date
from pathlib import Path
from typing import Optional, List, Tuple


class Accuracy(enum.Enum):
    """Enum representing the accuracy of a given character in a guess."""

    ABSENT = 0
    EXISTS = 1
    CORRECT = 2


class WordleModel:
    MAX_GUESSES = 6

    def __init__(self) -> None:
        """Responsible for loading the vocabulary and choosing today's winning
        word.
        """
        self.previous_guesses: List[Tuple[str, List[Accuracy]]] = []

        # load vocabulary
        self.vocabulary = []
        vocab_path = Path("/usr/share/dict/american-english")
        with open(vocab_path) as vocab_file:
            lines = vocab_file.readlines()
            for line in lines:
                word = line.strip()
                is_alpha = all(
                    [c.isalpha() for c in word]
                )  # excludes conjunctive words and foreign words with special characters
                is_proper_noun = any([c.isupper() for c in word])
                is_five_letters = len(word) == 5
                if is_alpha and not is_proper_noun and is_five_letters:
                    self.vocabulary.append(word)

        # choose winning word based on date
        today = date.today()
        date_hash = hash(today)
        index = date_hash % len(self.vocabulary)
        self.winning_word = self.vocabulary[index]

        self.did_win: Optional[bool] = None

    def guess(self, word: str) -> Optional[List[Accuracy]]:
        """Handles guesses. The game must still be ongoing and the guessed
        word must be a part of the vocabulary and have not been guessed
        previously.

        :param word: string
        :return: None if guess was invalid. Otherwise returns the outcome of'
        the guess as represented by a list of Accuracy's for each character in
        the guess.
        """
        if not self._is_valid_guess(word):
            return None

        outcome = []
        for i, char in enumerate(word):
            if char not in self.winning_word:
                outcome.append(Accuracy.ABSENT)
            elif char == self.winning_word[i]:
                outcome.append(Accuracy.CORRECT)
            else:
                outcome.append(Accuracy.EXISTS)

        self.previous_guesses.append((word, outcome))

        if word == self.winning_word:
            self.did_win = True
        elif len(self.previous_guesses) == WordleModel.MAX_GUESSES:
            self.did_win = False

        return outcome

    def _is_valid_guess(self, word: str) -> bool:
        """Private method used to determine whether a given word constitutes a valid guess.

        :param word: string to check.
        :return: boolean value representing whether or not the guess was a
        valid input.
        """
        if self.did_win is not None:
            return False
        if len(self.previous_guesses) == WordleModel.MAX_GUESSES:
            return False
        if word not in self.vocabulary:
            return False
        if word in [guessed_word for guessed_word, outcome in self.previous_guesses]:
            return False
        return True


if __name__ == "__main__":
    model = WordleModel()
