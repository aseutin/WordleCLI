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

        # choose winning_word based on date
        today = date.today()
        date_hash = hash(today)
        index = date_hash % len(self.vocabulary)
        self.winning_word = self.vocabulary[index]

        self.did_win = None

    def guess(self, word):
        if len(self.previous_guesses) == WordleModel.MAX_GUESSES:
            return None
        if word not in self.vocabulary:
            return None
        if self.did_win == True:
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


class Accuracy(enum.Enum):
    ABSENT = 0
    EXISTS = 1
    CORRECT = 2


if __name__ == "__main__":
    model = WordleModel()
