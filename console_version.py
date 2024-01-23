import os

from game_model import Board
from os import system

MOVE_DICT = {
    "w": "UP",
    "a": "LEFT",
    "s": "DOWN",
    "d": "RIGHT"
}
CLEAR = 'cls'
def game_input(prompt: str, options: list[str]) -> str:

    done: bool = False
    ans: str = ""
    while not done:
        s = input(f"{prompt} ({'|'.join(options)}) ")
        if s in options:
            done = True
            ans = s
    return ans


class Console_2k48:

    def __init__(self, board):

        if os.name == 'posix':
            global CLEAR
            CLEAR = 'clear'
        self.board = board

        self.game()

    def game(self):
        try:
            while self.board.game_is_on:
                os.system(CLEAR)
                self.board.print()
                choice = game_input("Pick a move.", ["w", "s", "a", "d"])
                self.board.move(MOVE_DICT[choice])
        except KeyboardInterrupt:
            pass
        finally:
            print(f"\nGame ended with score {self.board.score}")


