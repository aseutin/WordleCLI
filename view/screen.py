import curses
from curses.textpad import Textbox, rectangle


# TODO: prompt user to resize terminal window if something fails

DEFAULT_PADDING_X = 3
DEFAULT_PADDING_Y = 2


class Screen:
    def __init__(self):
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

    def add_text(self, window, x, y, message):
        window.addstr(y, x, message)
        window.refresh()

    def add_centered_text(self, window, message):
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

    def add_box(self, x1, y1, x2, y2):
        width = x2 - x1
        height = y2 - y1
        window = curses.newwin(height, width, y1, x1)
        rectangle(self.stdscr, y1 - 1, x1 - 1, y2, x2)
        self.stdscr.refresh()

        return window

    def add_banner(self, y, height, contents, padding_x=DEFAULT_PADDING_X):
        banner_window = self.add_box(
            padding_x, y, self.screen_width - padding_x, y + height
        )
        self.add_centered_text(banner_window, contents)

    def add_box_row(
        self, y1, box_height, box_width, num_cols, padding_x=DEFAULT_PADDING_X
    ):
        boxes = []
        num_x_gaps = num_cols - 1
        x_span = (num_cols * box_width) + (num_x_gaps * padding_x)
        x0 = (self.screen_width - x_span) // 2

        for col in range(num_cols):
            x1 = x0 + (col * box_width) + (col * padding_x)
            box = self.add_box(x1, y1, x1 + box_width, y1 + box_height)
            boxes.append(box)

        return boxes

    def add_box_grid(
        self,
        y0,
        box_height,
        box_width,
        num_rows,
        num_cols,
        padding_x=DEFAULT_PADDING_X,
        padding_y=DEFAULT_PADDING_Y,
    ):
        """Given a starting y position, create a grid of boxes that are
        horizontally centered in the screen.
        """
        boxes = []

        for row in range(num_rows):
            y1 = y0 + (row * box_height) + (row * padding_y)
            box_row = self.add_box_row(
                y1, box_height, box_width, num_cols, padding_x=padding_x
            )
            boxes.append(box_row)

        return boxes

    def add_centered_box_grid(
        self,
        y0,
        box_height,
        box_width,
        num_rows,
        num_cols,
        padding_x=DEFAULT_PADDING_X,
        padding_y=DEFAULT_PADDING_Y,
    ):
        num_y_gaps = num_rows - 1
        y_span = (num_rows * box_height) + (num_y_gaps * padding_y)
        y0 = (self.screen_height - y_span) // 2
        return self.add_box_grid(
            y0,
            box_height,
            box_width,
            num_rows,
            num_cols,
            padding_x=padding_x,
            padding_y=padding_y,
        )

    def close(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
