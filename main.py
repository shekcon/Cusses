#! /usr/bin/env python3
from tetris import Tetris, curses


def main():
    game = Tetris()
    game.start_game()
    # try:
    #
    # except Exception:
    #     pass
    curses.endwin()


if __name__ == '__main__':
    main()
