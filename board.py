# board.py
ROWS = 6
COLUMNS = 7
EMPTY = 0

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

# ai_minimax.py
import math
import random
from board import *
from evaluation import score_position

PLAYER = 1
AI = 2

def is_terminal_node(board):
    return check_win(board, PLAYER) or check_win(board, AI) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, AI):
                return (None, 1000000000)
            elif check_win(board, PLAYER):
                return (None, -1000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, col, AI)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, col, PLAYER)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# evaluation.py
from board import *

WINDOW_LENGTH = 4

def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0
    # Score center
    center_array = [board[r][COLUMNS//2] for r in range(ROWS)]
    score += center_array.count(piece) * 3

    # Score horizontal
    for r in range(ROWS):
        row_array = board[r]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMNS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# game.py
from board import *
from ai_minimax import minimax

PLAYER = 1
AI = 2

def play():
    board = create_board()
    game_over = False
    turn = 0  # 0 = Player, 1 = AI

    while not game_over:
        print_board(board)
        if turn == 0:
            col = int(input("Player 1 Make your Selection (0-6): "))
            if is_valid_location(board, col):
                drop_piece(board, col, PLAYER)
                if check_win(board, PLAYER):
                    print("PLAYER 1 WINS!")
                    game_over = True
        else:
            col, _ = minimax(board, 4, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                drop_piece(board, col, AI)
                if check_win(board, AI):
                    print("AI WINS!")
                    game_over = True

        turn += 1
        turn = turn % 2

def print_board(board):
    for row in board:
        print(row)


