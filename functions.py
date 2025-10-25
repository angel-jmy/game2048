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
    N = len(row)
    new_row = row[:]
    i, j = 0, 1
    while i < N and j < N:
    	if new_row[i] > 0:
    		i += 1
    		j += 1
    	elif new_row[i] == new_row[j] == 0:
    		j += 1
    	else:
    		new_row[i], new_row[j] = new_row[j], new_row[i]
    		i += 1
    		j += 1

    return new_row


def merge_row_left(row: List[int]) -> Tuple[List[int], int]:
    """Merge equal adjacent tiles from left to right, once per tile.
    Returns (new_row, score_gained).
    Typical pipeline per move: compress -> merge -> compress.
    Examples:
        [2,2,2,0] -> ([4,2,0,0], 4)
        [2,2,2,2] -> ([4,4,0,0], 8)
    """
    scores = 0
    row0 = compress_row_left(row)
    N = len(row0)
    new_row, new_len = [], 0
    i = 0
    while i < N:
    	if i + 1 < N and row0[i] == row0[i + 1] > 0:
    		score = 2 * row0[i]
    		scores += score
    		new_len += 1
    		new_row.append(score)
    		i += 2
    	elif i + 1 < N and row0[i] != row0[i + 1]:
    		new_len += 1
    		new_row.append(row0[i])
    		i += 1
    	elif i == N - 1:
    		new_len += 1
    		new_row.append(row0[i])
    		i += 1
    	else:
    		break

    new_row.extend([0] * (N - new_len))

    return new_row, scores


# -----------------------------
# Board transforms
# -----------------------------

def transpose(board: List[List[int]]) -> List[List[int]]:
    """Return the matrix transpose of the board."""
    N = len(board)
    new_board = copy_board(board)
    for i in range(N):
    	for j in range(i + 1):
    		new_board[i][j], new_board[j][i] = new_board[j][i], new_board[i][j]

    return new_board


def reverse_rows(board: List[List[int]]) -> List[List[int]]:
    """Return a new board with each row reversed (mirror horizontally)."""
    N = len(board)
    new_board = copy_board(board)
    for row in new_board:
    	for i in range(N // 2):
    		row[i], row[N - i - 1] = row[N - i - 1], row[i]

    return new_board


# -----------------------------
# Directional moves — compose row ops + transforms
# Each returns (new_board, score_gained, moved_flag)
# `moved_flag` is True iff the board actually changed.
# -----------------------------

def move_left(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Apply a LEFT move to the entire board using compress/merge pipeline."""
    new_board, scores = [], 0
    for row in board: 
    	new_row, score = merge_row_left(row)
    	new_board.append(new_row)
    	scores += score

    return new_board, scores, board_changed(board, new_board)


def move_right(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Derived via reverse_rows + move_left + reverse_rows."""
    reverse_board = reverse_rows(board)
    new_board, scores, flag = move_left(reverse_board)
    new_board = reverse_rows(new_board)

    return new_board, scores, flag


def move_up(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Derived via transpose + move_left + transpose."""
    trans_board = transpose(board)
    new_board, scores, flag = move_left(trans_board)
    new_board = transpose(new_board)

    return new_board, scores, flag


def move_down(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Derived via transpose + move_right + transpose."""
    trans_board = transpose(board)
    new_board, scores, flag = move_right(trans_board)
    new_board = transpose(new_board)

    return new_board, scores, flag


# -----------------------------
# Game state checks
# -----------------------------

def board_changed(before: List[List[int]], after: List[List[int]]) -> bool:
    """Return True if two boards differ anywhere."""
    return before != after


def won(board: List[List[int]], target: int = TARGET_TILE) -> bool:
    """Return True if any tile >= target (default 2048)."""
    for row in board:
    	for val in row:
    		if val >= target:
    			return True
    return False


def has_move(board: List[List[int]]) -> bool:
    """Return True if any empty cell exists or any adjacent pair can merge.
    Used to detect game-over when False.
    """
    cells = get_empty_cells(board)
    if cells:
    	return True
    
    N = len(board)
    for i in range(N - 1):
    	for j in range(N - 1):
    		if board[i][j] == board[i + 1][j]:
    			return True
    		if board[i][j] == board[i][j + 1]:
    			return True

    return False


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
    
    sep = "+------+------+------+------+"  # horizontal divider
    lines = [sep]
    for row in board:
        row_str = "|".join(f"{x:^6}" if x != 0 else "      " for x in row)
        lines.append(f"|{row_str}|")
        lines.append(sep)
    return "\n".join(lines)

