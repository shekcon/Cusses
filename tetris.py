import curses
from random import randint
from time import time, sleep


class Tetris:
    """
        Bonus part:
            - Objects:
                                        x
                                        x
                  x | x   | xx | xx  |  x
                xxx | xxx | xx |  xx |  x

            - Rotation.
            - Display for the next on the score screen.
    """

    complex_blocks = (((0, 0), (1, 0), (1, -1), (1, -2)),  # => (0, 0) (0, -1) (-1, -1) (-2, -1)
                      # => (0, 0) (0, -1) (1, -1) (2, -1)
                      ((0, 0), (1, 0), (1, 1), (1, 2)),
                      # => (0, 0) (0, -1) (1, 0) (1, -1)
                      ((0, 0), (1, 0), (0, 1), (1, 1)),
                      # => (0, 0) (1, 0) (1, -1) (2, -1)
                      ((0, 0), (0, 1), (1, 1), (1, 2)),
                      ((0, 0), (1, 0), (2, 0), (3, 0)))  # => (0, 0) (0, -1) (0, -2) (0, -3)
    num_blocks = len(complex_blocks)

    def __init__(self):
        key_int = (259, 258, 260, 261, 32, 410)
        key_func = ("up_arrow", "down_arrow", "left_arrow", "right_arrow",
                    "space", "resize_window")
        self.mapping = {n: key_func[i] for i, n in enumerate(key_int)}
        self._init_cli()
        self.height, self.width = self.stdscr.getmaxyx()
        self.columns = self.width // 2
        self.rows = self.height
        self.matrix = [[" "] * self.columns for _ in range(self.rows)]
        self.level = 0.01

    def _init_cli(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.noecho()
        curses.curs_set(0)
        self.score = 0
        self.stdscr.keypad(True)
        self.stdscr.timeout(0)

    def _draw_score(self):
        size_score = self.width - self.columns - 1
        for i in range(self.rows):
            self.stdscr.addstr(i, self.columns, "||%s" %
                               (" " * (size_score - 2)))
        middle = self.columns + (size_score - 5) // 2
        self.stdscr.addstr(self.rows // 2 - 5, middle + 2,
                           "Score:", curses.color_pair(1))
        self.stdscr.addstr(self.rows // 2 - 4, middle + 2, "%s" %
                           self.score, curses.color_pair(1))

    def _generate_block(self):
        col = randint(2, self.columns - 3)
        self.row, self.old_row = 0, 0
        self.col, self.old_col = col, col
        self.block = self.complex_blocks[randint(0, self.num_blocks - 1)]
        if self._can_move(self.block, 0, 0):
            self._update()
        else:
            self.finish = True

    def _save_old_pos(self):
        self.old_row = self.row
        self.old_col = self.col

    def _has_score(self):
        for y, x in self.block:
            self.matrix[self.old_row + y][self.old_col + x] = "X"
        line_destroy = [i for i, line in enumerate(
            self.matrix) if line.count("X") == self.columns]
        if line_destroy:
            for line in line_destroy[::-1]:
                self.matrix.pop(line)
            for _ in line_destroy:
                self.matrix.insert(0, [" "for col in range(self.columns)])
            self.score += len(line_destroy)
            self._draw_board()
            self._draw_score()

    def _can_move(self, block, row, col):
        if self.col + col < 0:
            return False
        try:
            for y, x in block:
                if self.matrix[self.row + y + row][self.col + x + col] == "X":
                    return False
            return True
        except IndexError:
            pass
        return False

    def _draw_board(self):
        for i, line in enumerate(self.matrix):
            self.stdscr.addstr(i, 0, ''.join(line))

    def _update(self):
        for y, x in self.block:
            self.stdscr.addstr(self.old_row + y, self.old_col + x, " ")
        for y, x in self.block:
            self.stdscr.addstr(self.row + y, self.col + x, "X")
        self.stdscr.refresh()

    def _move_down(self):
        self._save_old_pos()
        if self._can_move(self.block, 1, 0):
            self.row += 1
        else:
            self._has_score()
            self._generate_block()
        self._update()

    def start_game(self):
        self._generate_block()
        self._draw_score()
        self.finish = False
        start = time()
        while not self.finish:
            if time() - start >= self.level:
                self._move_down()
                start = time()
            key = self.stdscr.getch()
            if key in self.mapping.keys():
                self._save_old_pos()
                getattr(self, self.mapping[key])()
                self._update()
        self._end_game()

    def _end_game(self):
        self.stdscr.addstr(self.rows // 2, self.columns //
                           2 - 5, "GAME OVER", curses.color_pair(1))
        self.stdscr.addstr(self.rows // 2 + 1, self.columns //
                           2 - 5, "Your score: %s" % self.score, curses.color_pair(1))
        self.stdscr.refresh()
        sleep(1)
        self.stdscr.nodelay(False)
        self.stdscr.getch()

    def left_arrow(self):
        if self._can_move(self.block, 0, -1):
            self.col -= 1

    def right_arrow(self):
        if self._can_move(self.block, 0, 1):
            self.col += 1

    def up_arrow(self):
        pass

    def down_arrow(self):
        self._move_down()

    def space(self):
        rotation = []
        for y, x in self.block:
            rotation.append((x, -y))
        for y, x in self.block:
            self.stdscr.addstr(self.row + y, self.col + x, " ")
        self.block = tuple(rotation)

    def resize_window(self):
        self.height, self.width = self.stdscr.getmaxyx()
        self._draw_score()
        self._draw_board()
