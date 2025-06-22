# game_board.py

from constants import ROWS, COLUMNS, EMPTY

def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def drop_piece(board, col, piece):
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY:
            board[row][col] = piece
            return True
    return False

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_valid_locations(board):
    return [c for c in range(COLUMNS) if is_valid_location(board, c)]

def check_win(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Negative diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False
