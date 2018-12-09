import curses
from random import randint


class Tetris:

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

    def start_game(self):
        self._generate_block()
        self._draw_score()
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
            self.move_down()

    def _draw_score(self):
        size_score = self.width - self.columns - 1
        for i in range(self.rows):
            self.stdscr.addstr(i, self.columns, "||%s" %
                               (" " * (size_score - 2)))
        middle = self.columns + (size_score - 5) // 2
        self.stdscr.addstr(self.rows // 2 - 5, middle, "Score:")
        self.stdscr.addstr(self.rows // 2 - 4, middle, "%s" % self.score)

    def _generate_block(self):
        col = randint(0, self.columns - 1)
        self.row, self.old_row = 0, 0
        self.col, self.old_col = col, col
        self._update()

    def _save_old_pos(self):
        self.old_row = self.row
        self.old_col = self.col

    def up_arrow(self):
        pass

    def down_arrow(self):
        self.speed = 5

    def move_down(self):
        self._save_old_pos()
        if self._can_move(1, 0):
            self.row += 1
        else:
            self.matrix[self.old_row][self.old_col] = "X"
            self._is_has_score()
            self._generate_block()
        self._update()

    def _is_has_score(self):
        for i, line in enumerate(self.matrix):
            if line.count("X") == self.columns:
                self._clean_matrix(i)
                self._draw_board()
                self.score += 1
                self._draw_score()
                break

    def _can_move(self, x, y):
        if self.col + y < 0:
            return False
        try:
            return self.matrix[self.row + x][self.col + y] != "X"
        except IndexError:
            pass
        return False

    def _clean_matrix(self, line):
        self.matrix.pop(line)
        self.matrix.insert(0, [" "for col in range(self.columns)])

    def _draw_board(self):
        for i, line in enumerate(self.matrix):
            self.stdscr.addstr(i, 0, ''.join(line))

    def left_arrow(self):
        if self._can_move(0, -1):
            self.col -= 1

    def right_arrow(self):
        if self._can_move(0, 1):
            self.col += 1

    def space(self):
        # for rotation
        pass

    def _update(self):
        self.stdscr.addstr(self.old_row, self.old_col, " ")
        self.stdscr.addstr(self.row, self.col, "X")
        self.stdscr.refresh()
        # self.debug()

    # def debug(self):
    #     with open('log', "a+") as f:
    #         f.write("old (%s, %s) new (%s, %s) \n" %
    #                 (self.old_row, self.old_col, self.row, self.col))

    def resize_window(self):
        self.height, self.width = self.stdscr.getmaxyx()
        self._draw_score()
        self._draw_board()
