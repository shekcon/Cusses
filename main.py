#! /usr/bin/env python3
from tetris import Tetris, curses


def main():
    game = Tetris()
    # try:
    game.start_game()
    # except Exception:
    #     pass
    curses.endwin()


if __name__ == '__main__':
    main()
