from console_version import Console_2k48
from gui import GameGUI
from game_model import Board
import os

DEFAULT_BOARD_DIMENSION = 4
DEFAULT_INIT_TILES = 2
DEFAULT_NEW_TILES = 1
CLEAR = 'cls'

def input_choice(prompt: str, choices: list[str]):

    s = input(f"{prompt} ({"|".join(choices)}): ")
    while s not in choices:
        print("Wrong value, try again.")
        s = input(f"{prompt} ({"|".join(choices)}): ")
    return s



if os.name == "posix":
    CLEAR = 'clear'

os.system(CLEAR)
try:
    dimension = int(input("Pick N to generate an NxN board: "))
    n_init_tiles = int(input("How many tiles do you want to start with? "))
    board = Board(dimension, n_init_tiles)
    print(f"Generated board of size "
          f"{dimension}x{dimension} "
          f"and {n_init_tiles} initial tiles.")
except ValueError as ve:
    print(ve)
    dimension = DEFAULT_BOARD_DIMENSION
    n_init_tiles = DEFAULT_INIT_TILES
    board = Board(dimension, n_init_tiles)
    print(f"Generated DEFAULT board of size "
          f"{dimension}x{dimension} "
          f"and {n_init_tiles} initial tiles.")

ver = input_choice("Which version do you want to play?", ["gui", "console"])
if ver == "gui":
    GameGUI(board)
else:
    Console_2k48(board)
