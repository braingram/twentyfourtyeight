import tfe

from tfe.game.board import _ALL_TILE_VALUES

import pytest


def test_just_move():
    b = tfe.Board([
        [0, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ])
    b._move(tfe.LEFT)
    assert b.tiles == [
        [0, 0, 0, 0],
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]


def test_combine():
    b = tfe.Board([
        [0, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 0, 0],
    ])
    b._move(tfe.DOWN)
    assert b.tiles == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 4, 0, 0],
    ]


def test_spawn():
    b = tfe.Board([
        [0, 4, 8, 16],
        [2, 4, 8, 16],
        [2, 4, 8, 16],
        [2, 4, 8, 16],
    ])
    b._spawn()
    assert b.tiles[0][0] != 0


def test_spawn_gameover():
    b = tfe.Board([
        [2, 4, 8, 16],
        [2, 4, 8, 16],
        [2, 4, 8, 16],
        [2, 4, 8, 16],
    ])
    with pytest.raises(tfe.GameOver):
        b._spawn()


@pytest.mark.parametrize("v1", _ALL_TILE_VALUES)
def test_number_combine(v1):
    v2 = v1 * 2
    b = tfe.Board([
        [v1, v1, v1, v1],
        [0,   0, v1,  0],
        [v2, v1, v1,  0],
        [ 0,  0,  0,  0],
    ])
    b._move(tfe.LEFT)
    assert b.tiles == [
        [v2, v2,  0,  0],
        [v1,  0,  0,  0],
        [v2, v2,  0,  0],
        [ 0,  0,  0,  0],
    ]


def test_full_move():
    b = tfe.Board()

    # a tile should have something
    assert len(list(b._iter_empty_coords())) == 15

    b.move(tfe.LEFT)
    # a new tile should be filled
    assert len(list(b._iter_empty_coords())) == 14


def test_reverse_rows():
    b = tfe.Board([
        [ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12],
        [13, 14, 15, 16],
    ])
    b._reverse_rows()
    assert b.tiles == [
        [ 4,  3,  2,  1],
        [ 8,  7,  6,  5],
        [12, 11, 10,  9],
        [16, 15, 14, 13],
    ]


def test_clockwise():
    b = tfe.Board([
        [ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12],
        [13, 14, 15, 16],
    ])
    b._clockwise()
    assert b.tiles == [
        [13,  9,  5,  1],
        [14, 10,  6,  2],
        [15, 11,  7,  3],
        [16, 12,  8,  4],
    ]


def test_counter_clockwise():
    b = tfe.Board([
        [ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12],
        [13, 14, 15, 16],
    ])
    b._counter_clockwise()
    assert b.tiles == [
        [ 4,  8, 12, 16],
        [ 3,  7, 11, 15],
        [ 2,  6, 10, 14],
        [ 1,  5,  9, 13],
    ]
