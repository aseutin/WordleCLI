import curses

from model.wordle_model import WordleModel, Accuracy
from view.wordle_ui import WordleUI


ACCURACY_TO_COLOR_PAIR = {
    Accuracy.ABSENT.name: 1,
    Accuracy.EXISTS.name: 2,
    Accuracy.CORRECT.name: 3,
}


class WordleController:
    def __init__(self):
        self.wordle_ui = WordleUI()
        self.wordle_model = WordleModel()

        # Listen for user input
        while True:
            input_code = self.wordle_ui.screen.stdscr.getch()

            if input_code == 27:  # escape key
                self.wordle_ui.close()
                break
            elif (
                chr(input_code) in ("KEY_BACKSPACE", "\b", "\x7f") or input_code == 263
            ):  # witnessed different codes in different environments
                self.wordle_ui.backspace_was_pressed()
            elif chr(input_code) == "\n":
                current_input = self.wordle_ui.get_current_input()
                outcome = self.wordle_model.guess(current_input)
                if outcome is not None:
                    color_pairs = [
                        ACCURACY_TO_COLOR_PAIR[accuracy.name] for accuracy in outcome
                    ]
                    self.wordle_ui.move_on_to_next_row(color_pairs)
                if self.wordle_model.did_win is not None:
                    self.wordle_ui.game_over()
            else:
                self.wordle_ui.key_was_pressed(chr(input_code).upper())


if __name__ == "__main__":
    WordleController()
