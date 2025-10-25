from __future__ import annotations

from typing import List, Tuple, Iterable, Optional
import random
import copy

# -----------------------------
# Constants & Exceptions
# -----------------------------
GRID_SIZE: int = 4
START_TILES: int = 2
TARGET_TILE: int = 2048 


class InvalidMove(Exception):
    """Raised when a move command is invalid or produces no change (optional)."""
# -----------------------------
# Board creation & utilities
# -----------------------------

def new_board(size: int = GRID_SIZE, start_tiles: int = START_TILES, *, rng: Optional[random.Random] = None) -> List[List[int]]:
    """Return a fresh size×size board with `start_tiles` random 2s placed.
    Args:
        size: board dimension (default 4)
        start_tiles: number of initial tiles to spawn (default 2)
        rng: optional Random instance for deterministic tests
    """

    if size <= 0:
    	raise ValueError("Grid size must be positive")

    '''Initialize the board'''
    board = [[0 for _ in range(size)] for _ in range(size)]

    r = rng or random

	max_tiles = size * size
	n_to_place = max(0, min(start_tiles, max_tiles))
	if n_to_place == 0:
		return board

	positions = r.sample(range(max_tiles), n_to_place)
	for pos in positions:
		r_idx = pos // size
		c_idx = pos % size
		board[r_idx][c_idx] = 2

	return board


def copy_board(board: List[List[int]]) -> List[List[int]]:
    """Deep-copy the board (list of lists)."""
    return [row[:] for row in board]


def get_empty_cells(board: List[List[int]]) -> List[Tuple[int, int]]:
    """Return coordinates (r, c) of empty cells (value == 0)."""
    cells = []
    size = len(board)
    for i in range(size):
    	for j in range(size):
    		if board[i][j] == 0:
	    		cells.append((i, j))
	return cells


def spawn_tile(board: List[List[int]], *, rng: Optional[random.Random] = None) -> bool:
    """Place a new tile with value 2 on a random empty cell. Return True if placed, False if board is full.

    Side-effect: mutates `board`.
    """
    cells = get_empty_cells(board)
    if not cells:
    	return False

    r = rng or random
    row, col = r.choice(cells)
    board[row][col] = 2
    return True


# -----------------------------
# Row operations (left-normalized)
# Always implement LEFT first, then derive other directions via transforms.
# -----------------------------

def compress_row_left(row: List[int]) -> List[int]:
    """Slide all non-zero numbers to the left, preserving order; pad with zeros to length GRID_SIZE.
    Examples:
        [0,0,2,2] -> [2,2,0,0]
        [2,0,2,0] -> [2,2,0,0]
    Pure function: does not mutate input row.
    """
    raise NotImplementedError


def merge_row_left(row: List[int]) -> Tuple[List[int], int]:
    """Merge equal adjacent tiles from left to right, once per tile.
    Returns (new_row, score_gained).
    Typical pipeline per move: compress -> merge -> compress.
    Examples:
        [2,2,2,0] -> ([4,2,0,0], 4)
        [2,2,2,2] -> ([4,4,0,0], 8)
    """
    raise NotImplementedError


# -----------------------------
# Board transforms
# -----------------------------

def transpose(board: List[List[int]]) -> List[List[int]]:
    """Return the matrix transpose of the board."""
    raise NotImplementedError


def reverse_rows(board: List[List[int]]) -> List[List[int]]:
    """Return a new board with each row reversed (mirror horizontally)."""
    raise NotImplementedError


# -----------------------------
# Directional moves — compose row ops + transforms
# Each returns (new_board, score_gained, moved_flag)
# `moved_flag` is True iff the board actually changed.
# -----------------------------

def move_left(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Apply a LEFT move to the entire board using compress/merge pipeline."""
    raise NotImplementedError


def move_right(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Derived via reverse_rows + move_left + reverse_rows."""
    raise NotImplementedError


def move_up(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Derived via transpose + move_left + transpose."""
    raise NotImplementedError


def move_down(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Derived via transpose + move_right + transpose."""
    raise NotImplementedError


# -----------------------------
# Game state checks
# -----------------------------

def board_changed(before: List[List[int]], after: List[List[int]]) -> bool:
    """Return True if two boards differ anywhere."""
    raise NotImplementedError


def won(board: List[List[int]], target: int = TARGET_TILE) -> bool:
    """Return True if any tile >= target (default 2048)."""
    raise NotImplementedError


def has_move(board: List[List[int]]) -> bool:
    """Return True if any empty cell exists or any adjacent pair can merge.
    Used to detect game-over when False.
    """
    raise NotImplementedError


# -----------------------------
# Optional helpers (nice-to-have, can skip at first)
# -----------------------------

def score_of(board: List[List[int]]) -> int:
    """Compute a score heuristic (e.g., sum of merges or sum of tiles).
    You can track score incrementally during moves instead.
    """
    raise NotImplementedError


def as_text_grid(board: List[List[int]]) -> str:
    """Return a simple fixed-width ASCII grid for debugging / console UI."""
    raise NotImplementedError
