"""
The Controller's responsibility is to handle communication between the view
and the model. This allows each of those two pieces to be defined cleanly and
remain agnostic to the way in which the other will make use of it.
"""
import curses

from model.wordle_model import WordleModel, Accuracy
from view.wordle_ui import WordleUI


# Define preset mapping from model's correctness enum to the view's color pair
# options (see screen.py's color pairs)
ACCURACY_TO_COLOR_PAIR = {
    Accuracy.ABSENT.name: 1,
    Accuracy.EXISTS.name: 2,
    Accuracy.CORRECT.name: 3,
}


class WordleController:
    def __init__(self) -> None:
        """The controller starts listening for user input right away. It is
        responsible for handling all requests from the user, handing updates to
        the model, and telling the view how to reflect the updated state.
        """

        self.wordle_ui = WordleUI()
        self.wordle_model = WordleModel()

        # Listen for user input indefinitely
        while True:
            input_code = self.wordle_ui.get_input_character_code()

            if input_code == 27:  # escape key
                self.wordle_ui.close()
                break
            elif (
                chr(input_code) in ("KEY_BACKSPACE", "\b", "\x7f") or input_code == 263
            ):  # witnessed different codes in different environments
                self.wordle_ui.backspace_was_pressed()
            elif chr(input_code) == "\n":  # enter key
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
