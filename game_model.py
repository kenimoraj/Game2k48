import random


class Board:

    def __init__(self, dimension, n_init_tiles):

        if n_init_tiles > dimension * dimension:
            raise ValueError(f"Too many initial tiles. Board dimensions are {dimension}x{dimension}.")

        self.dimension = dimension
        self.n_init_tiles = n_init_tiles
        self.tile_matrix: list[list[int]] = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]
        self.empty_spaces: list[tuple[int, int]] = [(i, j) for i in range(self.dimension)
                                                    for j in range(self.dimension)]
        self.movement_map: dict[tuple[int, int]: tuple[int, int]] = {}

        self.score = 0

        for _ in range(self.n_init_tiles):
            self.new_tile()

        self.game_is_on = True

    def update_empty_spaces(self):
        new_empty_spaces: list[tuple[int, int]] = [(i, j) for i in range(self.dimension) for j in range(self.dimension)
                                                   if self.tile_matrix[i][j] == 0]
        self.empty_spaces = new_empty_spaces

    def new_tile(self):

        (row, col) = random.choice(self.empty_spaces)

        value: int
        r = random.random()
        if r > 0.1:
            value = 2
        else:
            value = 4

        self.tile_matrix[row][col] = value
        self.empty_spaces.remove((row, col))

        # print(f"New tile at {row},{col}")

    def print(self):

        # cell_padding = len(str(self.get_max_value())) + 2
        cell_padding = len(str("65536")) + 2
        top_bottom_border = "="*(2+(cell_padding + 1)*self.dimension+1)
        print(top_bottom_border)
        for i in range(self.dimension):
            print("||", end="")
            for j in range(self.dimension):
                content = str(self.tile_matrix[i][j])
                if content == "0":
                    content = ""

                print(content.center(cell_padding), end="")
                print("|", end="")
            print("|")
        print(top_bottom_border)
        print(f"Score: {self.score}")

    def get_max_value(self) -> int:

        result: int = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.tile_matrix[i][j] > result:
                    result = self.tile_matrix[i][j]

        return result

    def move(self, movement: str):

        if movement not in ["LEFT", "RIGHT", "UP", "DOWN"]:
            raise ValueError("Wrong movement!")

        if movement == "LEFT":
            self.movement_map = {}
            for rownum in range(self.dimension):
                # remove zeros and append them to the end
                row = self.tile_matrix[rownum]
                n_empty_spaces_in_row = len([s for s in self.empty_spaces if s[0] == rownum])
                orig_pos = [(rownum, j) for j in range(len(row)) if row[j] > 0]

                for _ in range(n_empty_spaces_in_row):
                    row.remove(0)
                    row.append(0)
                for ix in range(len(orig_pos)):
                    # if orig_pos[ix][1] != ix:
                    self.movement_map[orig_pos[ix]] = (rownum, ix)

                # handle doubles
                for i in range(1, self.dimension):
                    if row[i - 1] == row[i]:

                        to_shift = {k: v for (k, v) in self.movement_map.items()
                                    if v[0] == rownum and v[1] >= i}
                        for key in to_shift:
                            self.movement_map[key] = (rownum, self.movement_map[key][1] - 1)
                        row[i - 1] *= 2
                        self.score += row[i - 1]
                        row.remove(row[i])
                        row.append(0)

            self.update_empty_spaces()
            something_happened: bool = False
            for m in self.movement_map:
                if m != self.movement_map[m]:
                    something_happened = True
                    break

            if len(self.empty_spaces) > 0 and something_happened:
                self.new_tile()

            self.game_is_on = self.its_possible_to_move()

            # print(self.movement_map)
        elif movement == "RIGHT":
            self.reflect()
            self.move("LEFT")
            self.reflect()
        elif movement == "UP":
            self.transpose()
            self.move("LEFT")
            self.transpose()
        elif movement == "DOWN":
            self.transpose()
            self.move("RIGHT")
            self.transpose()

    def reflect(self):

        for row in self.tile_matrix:
            row.reverse()
        self.update_empty_spaces()

        new_movement_map = {(k[0], self.dimension - 1 - k[1]): (v[0], self.dimension - 1 - v[1])
                            for (k, v) in self.movement_map.items()}

        self.movement_map = new_movement_map

    def transpose(self):
        self.tile_matrix = [[self.tile_matrix[i][j] for i in range(self.dimension)] for j in range(self.dimension)]
        self.update_empty_spaces()

        new_movement_map = {(k[1], k[0]): (v[1], v[0])
                            for (k, v) in self.movement_map.items()}

        self.movement_map = new_movement_map

    def its_possible_to_move(self):
        if len(self.empty_spaces) > 0:
            return True

        # checking for doubles in rows
        for row in self.tile_matrix:
            for i in range(1, self.dimension):
                if row[i] == row[i-1]:
                    return True

        # checking for doubles in cols
        for row in [[self.tile_matrix[i][j] for i in range(self.dimension)] for j in range(self.dimension)]:
            for i in range(1, self.dimension):
                if row[i] == row[i-1]:
                    return True

        # If all fails
        return False