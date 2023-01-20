import curses

from view.wordle_ui import WordleUI


class WordleController:
    def __init__(self):
        self.wordle_ui = WordleUI()

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
                self.wordle_ui.return_was_pressed()
            else:
                self.wordle_ui.key_was_pressed(chr(input_code).upper())


if __name__ == "__main__":
    WordleController()
