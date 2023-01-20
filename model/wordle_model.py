import enum

from datetime import date
from pathlib import Path


class WordleModel:
    MAX_GUESSES = 6

    def __init__(self):
        self.previous_guesses = []

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

        self.did_win = None

    def guess(self, word):
        if not self.is_valid_guess(word):
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

    def is_valid_guess(self, word):
        if self.did_win is not None:
            return False
        if len(self.previous_guesses) == WordleModel.MAX_GUESSES:
            return False
        if word not in self.vocabulary:
            return False
        if word in [guessed_word for guessed_word, outcome in self.previous_guesses]:
            return False
        return True


class Accuracy(enum.Enum):
    ABSENT = 0
    EXISTS = 1
    CORRECT = 2


if __name__ == "__main__":
    model = WordleModel()
