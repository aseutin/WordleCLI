import curses

from view.screen import Screen
from view.screen import DEFAULT_PADDING_Y


class WordleUI:
    def __init__(self):
        self.screen = Screen()

        self.is_accepting_input = True  # switch to false once game it over

        # Setting up header
        self.screen.add_text(self.screen.stdscr, 1, 1, "Developed by Alexander Seutin")
        title = r"""
         __      __                   __   ___
        /\ \  __/\ \                 /\ \ /\_ \
        \ \ \/\ \ \ \    ___   _ __  \_\ \\//\ \      __
         \ \ \ \ \ \ \  / __`\/\`'__\/'_` \ \ \ \   /'__`\
          \ \ \_/ \_\ \/\ \L\ \ \ \//\ \L\ \ \_\ \_/\  __/
           \ `\___x___/\ \____/\ \_\\ \___,_\/\____\ \____\
            '\/__//__/  \/___/  \/_/ \/__,_ /\/____/\/____/
        """
        banner = self.screen.add_banner(3, 9, title)

        # Setting up user input grid
        guess_box_height = 1
        guess_box_width = 3
        self.guess_box_grid = self.screen.add_centered_box_grid(
            12, guess_box_height, guess_box_width, 6, 5
        )

        self.current_row = 0
        self.current_col = 0
        self.current_input = ""

        # Setting up keyboard grid
        qwerty_grid = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["\u23CE", "Z", "X", "C", "V", "B", "N", "N", "M", "\u232B"],
        ]
        self.qwerty_window_map = {}

        key_box_height = 1
        key_box_width = 3
        footer_offset = 1

        top_row = self.screen.add_box_row(
            self.screen.screen_height
            - 3 * (key_box_height + DEFAULT_PADDING_Y)
            - footer_offset,
            key_box_height,
            key_box_width,
            10,
        )
        for i, key_window in enumerate(top_row):
            self.qwerty_window_map[qwerty_grid[0][i]] = key_window
            self.screen.add_centered_text(key_window, qwerty_grid[0][i])

        middle_row = self.screen.add_box_row(
            self.screen.screen_height
            - 2 * (key_box_height + DEFAULT_PADDING_Y)
            - footer_offset,
            key_box_height,
            key_box_width,
            9,
        )
        for i, key_window in enumerate(middle_row):
            self.qwerty_window_map[qwerty_grid[1][i]] = key_window
            self.screen.add_centered_text(key_window, qwerty_grid[1][i])

        bottom_row = self.screen.add_box_row(
            self.screen.screen_height
            - 1 * (key_box_height + DEFAULT_PADDING_Y)
            - footer_offset,
            key_box_height,
            key_box_width,
            10,
        )
        for i, key_window in enumerate(bottom_row):
            self.qwerty_window_map[qwerty_grid[2][i]] = key_window
            self.screen.add_centered_text(key_window, qwerty_grid[2][i])

    def key_was_pressed(self, key):
        if not self.is_accepting_input:
            return

        if key in self.qwerty_window_map:
            if self.current_col <= 4:
                current_input_window = self.guess_box_grid[self.current_row][
                    self.current_col
                ]
                self.screen.add_centered_text(current_input_window, key)
                self.current_input += key
                self.current_col += 1

    def backspace_was_pressed(self):
        if not self.is_accepting_input:
            return

        if self.current_col >= 1:
            self.current_col -= 1
            current_input_window = self.guess_box_grid[self.current_row][
                self.current_col
            ]
            current_input_window.clear()
            current_input_window.refresh()
            self.current_input = self.current_input[:-1]

    def get_current_input(self):
        return self.current_input.strip().lower()

    def move_on_to_next_row(self, previous_guess_colors):
        """Expects a list containing indexes for the desired color_pair for
        each of the previously guessed characters.
        """

        for i, color_pair_index in enumerate(previous_guess_colors):
            input_window_at_index = self.guess_box_grid[self.current_row][i]
            key_at_index = self.current_input[i]

            # update input window color
            input_window_at_index.bkgd(
                " ", curses.color_pair(color_pair_index) | curses.A_BOLD
            )
            input_window_at_index.refresh()

            # update key window color
            key_window_at_index = self.qwerty_window_map[key_at_index]
            key_window_at_index.bkgd(
                " ", curses.color_pair(color_pair_index) | curses.A_BOLD
            )
            key_window_at_index.refresh()

        if not self.is_accepting_input:
            return

        if self.current_row <= 4:
            self.current_row += 1
            self.current_col = 0
            self.current_input = ""

    def game_over(self):
        self.is_accepting_input = False

    def close(self):
        self.screen.close()
