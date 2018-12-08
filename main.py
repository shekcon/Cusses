#! /usr/bin/env python3

from tetris import Tetris, curses
from random import randint
def cli(game):
    game.init_cli()
    k = 0
    while True:
        height, width = game.stdscr.getmaxyx()
        game.cursor_x = max(0, game.cursor_x)
        game.cursor_y = min(game.cursor_y, height-1)
        game.move()
        k = game.stdscr.getch(game.cursor_y, game.cursor_x)
        if k in game.mapping.keys():
            getattr(game, game.mapping[k])()
        game.stdscr.refresh()
    curses.endwin()
    game.end_cli()

if __name__ == '__main__':
    game = Tetris()
    cli(game)
