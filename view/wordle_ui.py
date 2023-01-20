import curses

from view.screen import Screen
from view.screen import DEFAULT_PADDING_Y


class WordleUI:
    def __init__(self):
        self.screen = Screen()

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
        self.screen.add_centered_box_grid(12, guess_box_height, guess_box_width, 6, 5)

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
        if key in self.qwerty_window_map:
            character_window = self.qwerty_window_map[key]
            character_window.bkgd(
                " ", curses.color_pair(1) | curses.A_BOLD
            )  # TODO: check this
            character_window.refresh()

            # TODO: is this useful?
            # try:
            #     character_window.bkgd(" ", curses.color_pair(1))
            #     character_window.refresh()
            # except curses.ERR:
            #     # End of screen reached
            #     pass

    def backspace_was_pressed(self):
        # TODO: handle in unique way
        self.key_was_pressed("\u232B")

    def return_was_pressed(self):
        # TODO: handle in unique way
        self.key_was_pressed("\u23CE")

    def close(self):
        self.screen.close()
