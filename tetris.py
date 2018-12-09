import curses
from random import randint


class Tetris:
    """
        Bonus part:
            - Objects:
                                        x
                                        x
                  x | x   | xx | xx  |  x |  x
                xxx | xxx | xx |  xx |  x | xxx

            - Rotation.
            - Display for the next on the score screen.
    """

    complex_blocks = (((0, 0), (1, 0), (1, -1), (1, -2)),
                       ((0, 0), (1, 0), (1, 1), (1, 2)),
                       ((0, 0), (1, 0), (0, 1), (1, 1)),
                       ((0, 0), (0, 1), (1, 1), (1, 2)),
                       ((0, 0), (1, 0), (2, 0), (3, 0)),
                       ((0, 0), (1, 0), (1, 1), (1, -1))
                       )
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

    def _init_cli(self):
        self.stdscr = curses.initscr()
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
        self.middle = self.columns + (size_score - 5) // 2

        self.stdscr.addstr(self.rows // 2 - 5, self.middle, "Score:")
        self.stdscr.addstr(self.rows // 2 - 4, self.middle, "%s" % self.score)

    def _generate_block(self):
        col = randint(2, self.columns - 3)
        self.row, self.old_row = 0, 0
        self.col, self.old_col = col, col

        if hasattr(self, 'next_block'):
            for y, x in self.next_block:
                self.stdscr.addstr(self.rows//2 - 10 + y, self.middle + x, " ")
            self.block = self.next_block
        else:
            self.block = self.complex_blocks[randint(0, self.num_blocks - 1)]
        self.next_block = self.complex_blocks[randint(0, self.num_blocks - 1)]
        for y, x in self.next_block:
            self.stdscr.addstr(self.rows//2 - 10 + y, self.middle + x, "X")
        self._update()

    def _save_old_pos(self):
        self.old_row = self.row
        self.old_col = self.col

    def _has_score(self):
        for y, x in self.block:
            self.matrix[self.old_row + y][self.old_col + x] = "X"
        line_destroy = [i for i, line in enumerate(self.matrix) if line.count("X") == self.columns]
        if line_destroy:
            for line in line_destroy[::-1]:
                self.matrix.pop(line)
            for _ in line_destroy:
                self.matrix.insert(0, [" "for col in range(self.columns)])
                self.score += 1
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
        self._draw_score()
        self._generate_block()
        self.finish = False
        while not self.finish:
            self.speed = 50
            count = 0
            while count <= self.speed:
                key = self.stdscr.getch()
                if key in self.mapping.keys():
                    self._save_old_pos()
                    getattr(self, self.mapping[key])()
                    self._update()
                curses.napms(10)
                count += 1
            self._move_down()

    def left_arrow(self):
        if self._can_move(self.block, 0, -1):
            self.col -= 1

    def right_arrow(self):
        if self._can_move(self.block, 0, 1):
            self.col += 1

    def up_arrow(self):
        pass

    def down_arrow(self):
        self.speed = 5

    def space(self):
        rotation = []
        for y, x in self.block:
            rotation.append((x, -y))
        if not self._can_move(rotation, 0, 0):
            return
        for y, x in self.block:
            self.stdscr.addstr(self.row + y, self.col + x, " ")
        self.block = tuple(rotation)

    def resize_window(self):
        self.height, self.width = self.stdscr.getmaxyx()
        self._draw_score()
        self._draw_board()
