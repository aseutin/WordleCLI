import curses
from curses.textpad import Textbox, rectangle


# TODO: prompt user to resize terminal window if something fails


class Screen:
    def __init__(self):
        # Setting up curses
        self.stdscr = curses.initscr()  # find screen dimensions and basic props
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)

        curses.noecho()  # prevent keys from echoing to stdout
        curses.cbreak()  # read key inputs before enter is hit
        self.stdscr.keypad(
            True
        )  # interpret key input and translate to curses special chars (ex: curses.KEY_LEFT)
        self.stdscr.clear()

        self.screen_width = curses.COLS - 1
        self.screen_height = curses.LINES - 1

        self.timer = 0  # TODO: use actual time  # TODO: not in use

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

        screen.add_text(window, 0, 0, y_translated_contents)

    # def replace_window_contents(self, window, text):
    #     window.clear()
    #     self.add_text(window, 0, 0, text)
    #     window.refresh()

    def create_box(self, x1, y1, x2, y2):
        width = x2 - x1
        height = y2 - y1
        window = curses.newwin(height, width, y1, x1)
        rectangle(self.stdscr, y1 - 1, x1 - 1, y2, x2)
        self.stdscr.refresh()

        return window

    def create_box_row(self, y1, box_height, box_width, num_cols, padding=1):
        boxes = []
        num_x_gaps = num_cols - 1
        x_span = (num_cols * box_width) + (num_x_gaps * padding)
        x0 = (self.screen_width - x_span) // 2

        for col in range(num_cols):
            x1 = x0 + (col * box_width) + (col * padding)
            box = self.create_box(x1, y1, x1 + box_width, y1 + box_height)
            boxes.append(box)

        return boxes

    def create_box_grid(self, y0, box_height, box_width, num_rows, num_cols, padding=1):
        """Given a starting y position, create a grid of boxes that are
        horizontally centered in the screen.
        """
        boxes = []

        for row in range(num_rows):
            y1 = y0 + (row * box_height) + (row * padding)
            box_row = self.create_box_row(
                y1, box_height, box_width, num_cols, padding=padding
            )
            boxes.append(box_row)

        return boxes

    def create_centered_box_grid(
        self, y0, box_height, box_width, num_rows, num_cols, padding=1
    ):
        num_y_gaps = num_rows - 1
        y_span = (num_rows * box_height) + (num_y_gaps * padding)
        y0 = (self.screen_height - y_span) // 2
        return self.create_box_grid(
            y0, box_height, box_width, num_rows, num_cols, padding=padding
        )

    def create_banner(self, y, height, contents, buffer=2):
        banner_window = self.create_box(
            buffer, y, self.screen_width - buffer, y + height
        )
        self.add_centered_text(banner_window, contents)

    def close(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()


screen = Screen()
screen.add_text(screen.stdscr, 1, 1, "Developed by Alexander Seutin")

greetings = """▌ ▌▞▀▖▛▀▖▛▀▖▌  ▛▀▘ ▞▀▖▌  ▜▘ ▞▀▖  ▞▀▖
▌▖▌▌ ▌▙▄▘▌ ▌▌  ▙▄  ▌  ▌  ▐   ▗▘  ▌▞▌
▙▚▌▌ ▌▌▚ ▌ ▌▌  ▌   ▌ ▖▌  ▐  ▗▘ ▗▖▛ ▌
▘ ▘▝▀ ▘ ▘▀▀ ▀▀▘▀▀▘ ▝▀ ▀▀▘▀▘ ▀▀▘▝▘▝▀"""
banner = screen.create_banner(3, 4, greetings)

qwerty_grid = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["\u23CE", "Z", "X", "C", "V", "B", "N", "N", "M", "\u232B"],
]

qwerty_window_map = {}

guess_box_height = 1
guess_box_width = 3
guess_box_padding = 2
screen.create_centered_box_grid(
    12, guess_box_height, guess_box_width, 6, 5, padding=guess_box_padding
)

key_box_height = 1
key_box_width = 3
key_box_padding = 2
footer_offset = 1
top_row = screen.create_box_row(
    screen.screen_height - 3 * (key_box_height + key_box_padding) - footer_offset,
    key_box_height,
    key_box_width,
    10,
    padding=key_box_padding,
)
for i, key_window in enumerate(top_row):
    qwerty_window_map[qwerty_grid[0][i]] = key_window
    screen.add_centered_text(key_window, qwerty_grid[0][i])

middle_row = screen.create_box_row(
    screen.screen_height - 2 * (key_box_height + key_box_padding) - footer_offset,
    key_box_height,
    key_box_width,
    9,
    padding=key_box_padding,
)
for i, key_window in enumerate(middle_row):
    qwerty_window_map[qwerty_grid[1][i]] = key_window
    screen.add_centered_text(key_window, qwerty_grid[1][i])

bottom_row = screen.create_box_row(
    screen.screen_height - 1 * (key_box_height + key_box_padding) - footer_offset,
    key_box_height,
    key_box_width,
    10,
    padding=key_box_padding,
)
for i, key_window in enumerate(bottom_row):
    qwerty_window_map[qwerty_grid[2][i]] = key_window
    screen.add_centered_text(key_window, qwerty_grid[2][i])

while True:
    input_code = screen.stdscr.getch()
    for character, character_window in qwerty_window_map.items():
        if chr(input_code).upper() == character:
            try:
                for i in range(0, 255):
                    character_window.bkgd(" ", curses.color_pair(1))
                    character_window.refresh()
            except curses.ERR:
                # End of screen reached
                pass
        # else:
        #     try:
        #         for i in range(0, 255):
        #             character_window.bkgd(curses.color_pair(0))
        #     except curses.ERR:
        #         # End of screen reached
        #         pass
    if chr(input_code) == "\n":
        break

screen.close()
