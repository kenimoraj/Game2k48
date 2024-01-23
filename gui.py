from tkinter import *
from game_model import Board
from math import fabs, log2
from copy import deepcopy

NUMBER_FONT_NAME = "Courier"
NUMBER_FONT_STYLE = "bold"
TILE_COLORS = {
    2: "#ff6666",
    4: "#ffb266",
    8: "#ffff66",
    16: "#b2ff66",
    32: "#66ff66",
    64: "#66ffb2",
    128: "#66ffff",
    256: "#66b2ff",
    512: "#6666ff",
    1024: "#b266ff",
    2048: "#ff66ff"
}

CANVAS_BACKGROUND = "grey"
CANVAS_SIZE = 600
SCOREBOARD_HEIGHT = 60
SCOREBOARD_BACKGROUND = "black"
SCOREBOARD_FONT_COLOR = "white"
SCOREBOARD_FONT_SIZE = 40
EMPTY_TILE_OUTLINE_COLOR = "black"
EMPTY_TILE_PADDING = 2

WAIT_MS = 20
N = 10
MOVEMENT_TIME_MS = 75


class ScoreboardCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = self.create_text(CANVAS_SIZE // 2, SCOREBOARD_HEIGHT // 2, text="Score: 0",
                                      fill=SCOREBOARD_FONT_COLOR,
                                      font=(NUMBER_FONT_NAME, SCOREBOARD_FONT_SIZE, "bold"))

    def update_score(self, score):
        self.itemconfig(self.score, text=f"Score: {score}")

class BoardCanvas(Canvas):

    def __init__(self, *args, board: Board, scoreboard: ScoreboardCanvas, **kwargs):
        super().__init__(*args, **kwargs)

        self.board = board
        self.tile_size = CANVAS_SIZE // self.board.dimension
        self.scoreboard = scoreboard
        self.drawn_tiles: dict[tuple[int, int]: tuple[int, int]] = {}
        self.draw_background()
        self.display_board()
        self.movement_is_on = False

    def draw_background(self):
        n = self.board.dimension
        padding = EMPTY_TILE_PADDING # (CANVAS_SIZE // self.board.dimension) // 4
        for i in range(n):
            for j in range(n):
                x1, y1, x2, y2 = self.coords_for_pos(i, j)
                x1 += padding
                x2 -= padding
                y1 += padding
                y2 -= padding
                self.create_rectangle(x1, y1, x2, y2, fill=EMPTY_TILE_OUTLINE_COLOR)

    def display_board(self):
        n = self.board.dimension
        for i in range(n):
            for j in range(n):
                value_ij = self.board.tile_matrix[i][j]
                if value_ij > 0:
                    self.draw_tile(value=value_ij, row=i, col=j)

    def draw_tile(self, value: int, row: int, col: int):
        x1, y1, x2, y2 = self.coords_for_pos(row, col)
        tile_center_x = (x1 + x2) // 2
        tile_center_y = (y1 + y2) // 2
        if value in TILE_COLORS:
            color = TILE_COLORS[value]
        else:
            color = TILE_COLORS[2048]

        font_size_orig = (x2 - x1) // 2
        font_size_perc: float = (100 - 15*(len(str(value)) - 1)) / 100
        font_size = int(font_size_orig * font_size_perc)
        square = self.create_rectangle(x1, y1, x2, y2, fill=color)
        txt = self.create_text(tile_center_x, tile_center_y, text=str(value),
                         font=(NUMBER_FONT_NAME, font_size, NUMBER_FONT_STYLE))
        self.drawn_tiles[(square, txt)] = (row, col)

    def coords_for_pos(self, row: int, col: int) -> tuple[int, int, int, int]:

        x1 = col * self.tile_size
        y1 = row * self.tile_size
        x2 = x1 + self.tile_size
        y2 = y1 + self.tile_size

        return x1, y1, x2, y2

    def move_tiles(self, movement: str):
        if self.movement_is_on:
            return
        self.movement_is_on = True
        # self.board.print()
        self.board.move(movement)
        # print(self.board.movement_map)
        self.animate_all(MOVEMENT_TIME_MS)



    def animate_all(self, time_left):
        counter = 0
# W petli po tilesach ruszyc kazdym troche, kazdy ruszony to licznik+1
        for (square, txt) in self.drawn_tiles:
            c_row, c_col = self.drawn_tiles[(square, txt)]
            t_row, t_col = self.board.movement_map[(c_row, c_col)]
            t_x1, t_y1, t_x2, t_y2 = self.coords_for_pos(t_row, t_col)
            # t_cx = (t_x1 + t_x2) // 2
            # t_cy = (t_y1 + t_y2) // 2

            c_x1, c_y1, c_x2, c_y2 = [int(c) for c in self.coords(square)]
            # c_cx, c_cy = self.coords(txt)
            dx: int
            dy: int
            step: int = int(max(fabs(c_x1 - t_x1), fabs(c_y1 - t_y1))) // ((time_left // WAIT_MS) + 1)
            if fabs(t_x1 - c_x1) >= step:
                if t_x1 > c_x1:
                    dx = step
                else:
                    dx = -step
            else:
                dx = 0

            if fabs(t_y1 - c_y1) >= step:
                if t_y1 > c_y1:
                    dy = step
                else:
                    dy = -step
            else:
                dy = 0
            # print(square,txt,dx,dy)
            if dx != 0 or dy != 0:
                self.move(square, dx, dy)
                self.move(txt, dx, dy)
                counter += 1
        if counter > 0:
            self.after(WAIT_MS, self.animate_all, max(time_left-WAIT_MS,0))
        else:
            for (square, txt) in self.drawn_tiles:
                self.delete(square)
                self.delete(txt)
            self.drawn_tiles = {}
            self.display_board()
            self.scoreboard.update_score(self.board.score)
            self.movement_is_on = False
            if not self.board.game_is_on:
                self.game_over()

    def game_over(self):

        self.create_text(CANVAS_SIZE // 2, CANVAS_SIZE // 2, text="GAME OVER", font=("Courier", 70, "bold"), fill="#ff00ff")

    def reset(self):
        dimension = self.board.dimension
        n_init_tiles = self.board.n_init_tiles
        self.board = Board(dimension, n_init_tiles)
        self.scoreboard.update_score(0)
        for (square, txt) in self.drawn_tiles:
            self.delete(square)
            self.delete(txt)
        self.delete('all')
        self.draw_background()
        self.drawn_tiles = {}
        self.display_board()


class GameGUI:
    def __init__(self, board):
        window = Tk()
        window.config(bg="black")
        sbc = ScoreboardCanvas(width=CANVAS_SIZE, height=SCOREBOARD_HEIGHT, bg=SCOREBOARD_BACKGROUND,
                               highlightthickness=0)
        sbc.grid(row=0, column=0)
        bc = BoardCanvas(width=CANVAS_SIZE, height=CANVAS_SIZE, bg=CANVAS_BACKGROUND,
                         board=board, scoreboard=sbc)

        bc.grid(row=1, column=0)

        window.bind("<KeyPress-Left>", lambda _: bc.move_tiles("LEFT"))
        window.bind("<KeyPress-Up>", lambda _: bc.move_tiles("UP"))
        window.bind("<KeyPress-Right>", lambda _: bc.move_tiles("RIGHT"))
        window.bind("<KeyPress-Down>", lambda _: bc.move_tiles("DOWN"))
        window.bind("<KeyPress-space>", lambda _: bc.reset())
        window.mainloop()


