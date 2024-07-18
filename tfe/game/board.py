import random

from enum import Enum

from ._row_stepper import step_row
from ._renderer import render_tiles


class GameOver(Exception):
    pass


_ALL_TILE_VALUES = [2 ** i for i in range(1, 11)]
Direction = Enum("Direction", ["UP", "DOWN", "LEFT", "RIGHT"])

def _make_blank_board():
    return [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]


class Board:
    def __init__(self, tiles=None):
        if tiles is None:
            self.tiles = _make_blank_board()
            [self._spawn() for i in range(3)]
        else:
            self.tiles = tiles

    def _iter_empty_coords(self):
        for (r, row) in enumerate(self.tiles):
            for (c, v) in enumerate(row):
                if not v:
                    yield r, c

    def _spawn(self):
        coords = list(self._iter_empty_coords())
        if not coords:
            raise GameOver("No empty tiles!")
        r, c = random.choice(coords)
        self.tiles[r][c] = random.choice([2, 4])

    def _reverse_rows(self):
        self.tiles = [r[::-1] for r in self.tiles]

    def _counter_clockwise(self):
        """
        0, 3 -> 0, 0
        1, 3 -> 0, 1
        2, 3 -> 0, 2
        3, 3 -> 0, 3

        0, 0 -> 3, 0
        0, 1 -> 2, 0
        0, 2 -> 1, 0
        """
        new_tiles = _make_blank_board()
        for (r, row) in enumerate(self.tiles):
            for (c, v) in enumerate(row):
                cp = r
                rp = 3 - c
                new_tiles[rp][cp] = v
        self.tiles = new_tiles

    def _clockwise(self):
        """
        0, 0 -> 0, 3
        0, 1 -> 1, 3
        0, 2 -> 2, 3

        0, 3 -> 3, 3
        1, 3 -> 3, 2
        2, 3 -> 3, 1
        3, 3 -> 3, 0
        """
        new_tiles = _make_blank_board()
        for (r, row) in enumerate(self.tiles):
            for (c, v) in enumerate(row):
                cp = 3 - r
                rp = c
                new_tiles[rp][cp] = v
        self.tiles = new_tiles

    def _make_left(self, direction):
        if direction == Direction.LEFT:
            return
        if direction == Direction.RIGHT:
            self._reverse_rows()
        if direction == Direction.UP:
            self._counter_clockwise()
        if direction == Direction.DOWN:
            self._clockwise()

    def _make_unleft(self, direction):
        if direction == Direction.LEFT:
            return
        if direction == Direction.RIGHT:
            self._reverse_rows()
        if direction == Direction.UP:
            self._clockwise()
        if direction == Direction.DOWN:
            self._counter_clockwise()

    def _go_left(self):
        self.tiles = [step_row(row) for row in self.tiles]

    def _move(self, direction):
        # for ease of coding, only go left
        self._make_left(direction)
        self._go_left()
        self._make_unleft(direction)

    def move(self, direction):
        self._move(direction)
        self._spawn()

    @property
    def score(self):
        return sum((sum(row) for row in self.tiles))
    
    def __str__(self):
        return render_tiles(self.tiles)

    def __repr__(self):
        return str(self)
