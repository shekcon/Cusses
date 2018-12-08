import curses


class Tetris:

    def __init__(self):
        key_int = (259, 258, 260, 261, 32)
        key_func = ("up_arrow", "down_arrow", "left_arrow", "right_arrow",
                    "space")
        self.mapping = {n: key_func[i] for i, n in enumerate(key_int)}
        self.cursor_y = 0
        self.cursor_x = 0
        self.old_x = 0
        self.old_y = 0

    def init_cli(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.noecho()
        curses.curs_set(0)
        self.stdscr.keypad(True)

    def up_arrow(self):
        pass

    def down_arrow(self):
        self.old_y = self.cursor_y
        self.cursor_y += 1

    def left_arrow(self):
        self.old_x = self.cursor_x
        self.cursor_x -= 1

    def right_arrow(self):
        self.old_x = self.cursor_x
        self.cursor_x += 1

    def space(self):
        # for rotation
        pass

    def move(self):
        self.stdscr.delch(self.cursor_y, self.old_x)
        self.stdscr.delch(self.old_y, self.cursor_x)
        self.stdscr.addstr(self.cursor_y, self.cursor_x, "X")
