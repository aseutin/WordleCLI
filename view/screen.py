"""
Custom wrapper built around curses. This exposes everything needed to allow
the wordle_ui to build the interface.
"""
import curses

from curses.textpad import Textbox, rectangle
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any


DEFAULT_PADDING_X = 3
DEFAULT_PADDING_Y = 2


class Screen:
    def __init__(self) -> None:
        """Responsible for curses related housekeeping."""
        # Setting up curses
        self.stdscr = curses.initscr()  # find screen dimensions and basic props
        self.stdscr.clear()

        # Recording props
        self.screen_width = curses.COLS - 1
        self.screen_height = curses.LINES - 1

        # Setting up color palette
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)

        # Setting up user input
        curses.noecho()  # prevent keys from echoing to stdout
        curses.cbreak()  # read key inputs before enter is hit
        self.stdscr.keypad(
            True
        )  # interpret key input and translate to curses special chars (ex: curses.KEY_LEFT)

    def add_text(self, window: Window, x: int, y: int, message: str) -> None:
        """Responsible for adding text to an existing curses window.
        Note: Curses cannot write text to a window that does not have enough
        room to display said text.

        :param window: curses window to write to.
        :param x: row relative to top left of curses window.
        :param y: column relative to top left of curses window.
        :param message: text to display in the curses window.
        """
        try:
            window.addstr(y, x, message)
            window.refresh()
        except:
            raise RuntimeError(
                "Terminal window is too small, please resize your window to at least 70x50 before trying again."
            )

    def add_centered_text(self, window: Window, message: str) -> None:
        """Responsible for adding text to an existing curses window. This will
        center the text in both x and y by adding spaces to the beginning of each line and adding newlines to the start of the entire message.

        :param window: curses window to write to.
        :message: text to display to the curses window.
        """
        rows, cols = window.getmaxyx()

        lines = message.split("\n")
        longest_line_length = max([len(line) for line in lines])
        extra_spaces = cols - longest_line_length
        x_padding = " " * (extra_spaces // 2)
        x_translated_contents = "\n".join([x_padding + line for line in lines])

        extra_lines = rows - len(lines)
        y_padding = "\n" * (extra_lines // 2)
        y_translated_contents = y_padding + x_translated_contents

        self.add_text(window, 0, 0, y_translated_contents)

    def add_box(self, x1: int, y1: int, x2: int, y2: int) -> Window:
        """Creates a new curses window at provided coordinates and draws a
        border around the new box.

        :param x1: row relative to top left of curses window.
        :param y1: column relative to top left of curses window.
        :param x2: row relative to top left of curses window.
        :param y2: column relative to top left of curses window.
        :return: newly created curses window.
        """
        width = x2 - x1
        height = y2 - y1
        window = curses.newwin(height, width, y1, x1)
        rectangle(self.stdscr, y1 - 1, x1 - 1, y2, x2)
        self.stdscr.refresh()

        return window

    def add_banner(
        self, y: int, height: int, message: str, padding_x: int = DEFAULT_PADDING_X
    ) -> Window:
        """Creates a new curses window with a border at provided row (y).
        This window will span the entire width of the screen (with padding).
        This window will also contain the provided message in the center.

        :param y: starting row to display the banner (top position).
        :param height: height of the banner in number of lines.
        :message: text to display to the curses window.
        :padding_x: optional integer specifying how much blank space to leave
        around the banner.
        :return: newly created curses window.
        """
        banner_window = self.add_box(
            padding_x, y, self.screen_width - padding_x, y + height
        )
        self.add_centered_text(banner_window, message)
        return banner_window

    def add_box_row(
        self,
        y: int,
        box_height: int,
        box_width: int,
        num_cols: int,
        padding_x: int = DEFAULT_PADDING_X,
    ) -> List[Window]:
        """Creates a row of bordered boxes. The entire row will be centered
        horizontally on screen and will include padding between each box.

        :param y: starting row to display the row (top position).
        :param box_height: height of each box in number of lines.
        :param box_width: width of each box in number of spaces.
        :param num_cols: number of boxes to add.
        :param padding_x: optional integer specifying how many blank spaces to
        leave between each box.
        :return: list of newly added boxes in order from left to right.
        """
        boxes = []
        num_x_gaps = num_cols - 1
        x_span = (num_cols * box_width) + (num_x_gaps * padding_x)
        x0 = (self.screen_width - x_span) // 2

        for col in range(num_cols):
            x1 = x0 + (col * box_width) + (col * padding_x)
            box = self.add_box(x1, y, x1 + box_width, y + box_height)
            boxes.append(box)

        return boxes

    def add_box_grid(
        self,
        y,
        box_height,
        box_width,
        num_rows,
        num_cols,
        padding_x=DEFAULT_PADDING_X,
        padding_y=DEFAULT_PADDING_Y,
    ) -> List[List[Window]]:
        """Creates a grid of bordered boxes. The entire grid will be centered
        horizontally on screen and will include padding between each box in
        both directions.

        :param y: starting row to display the grid (top position).
        :param box_height: height of each box in number of lines.
        :param box_width: width of each box in number of spaces.
        :param num_rows: number of rows to add.
        :param num_cols: number of cols to add.
        :param padding_x: optional integer specifying how many blank spaces to
        leave between each box.
        :param padding_y: optional integer specifying how many blank lines to
        leave between each box.
        :return: matrix of newly added boxes.
        """
        boxes = []

        for row in range(num_rows):
            y1 = y + (row * box_height) + (row * padding_y)
            box_row = self.add_box_row(
                y1, box_height, box_width, num_cols, padding_x=padding_x
            )
            boxes.append(box_row)

        return boxes

    def add_centered_box_grid(
        self,
        box_height,
        box_width,
        num_rows,
        num_cols,
        padding_x=DEFAULT_PADDING_X,
        padding_y=DEFAULT_PADDING_Y,
    ) -> List[List[Window]]:
        """Creates a grid of bordered boxes. The entire grid will be centered
        horizontally and vertically on screen and will include padding between
        each box in both directions.

        :param box_height: height of each box in number of lines.
        :param box_width: width of each box in number of spaces.
        :param num_rows: number of rows to add.
        :param num_cols: number of cols to add.
        :param padding_x: optional integer specifying how many blank spaces to
        leave between each box.
        :param padding_y: optional integer specifying how many blank lines to
        leave between each box.
        :return: matrix of newly added boxes.
        """
        num_y_gaps = num_rows - 1
        y_span = (num_rows * box_height) + (num_y_gaps * padding_y)
        y = (self.screen_height - y_span) // 2
        return self.add_box_grid(
            y,
            box_height,
            box_width,
            num_rows,
            num_cols,
            padding_x=padding_x,
            padding_y=padding_y,
        )

    def close(self) -> None:
        """Closes the underlying curses screen and ends the session."""
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
