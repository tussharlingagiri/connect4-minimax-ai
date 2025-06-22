# Step 1: Enhance ai_minimax.py with timing support

import time
import math
from board import get_valid_locations, is_valid_location, drop_piece, check_win, copy_board, AI

# Scoring function should be in evaluation.py
from evaluation import score_position

def minimax(board, depth, alpha, beta, maximizingPlayer):
    start_time = time.time()
    valid_locations = get_valid_locations(board)
    is_terminal = check_win(board, 1) or check_win(board, 2) or len(valid_locations) == 0

    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, AI):
                return (None, 100000000000000), time.time() - start_time
            elif check_win(board, 1):
                return (None, -10000000000000), time.time() - start_time
            else:  # Game is over, no more valid moves
                return (None, 0), time.time() - start_time
        else:  # Depth is zero
            return (None, score_position(board, AI)), time.time() - start_time

    if maximizingPlayer:
        value = -math.inf
        best_col = valid_locations[0]
        for col in valid_locations:
            b_copy = copy_board(board)
            drop_piece(b_copy, col, AI)
            new_score, _ = minimax(b_copy, depth-1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, time.time() - start_time

    else:  # Minimizing player
        value = math.inf
        best_col = valid_locations[0]
        for col in valid_locations:
            b_copy = copy_board(board)
            drop_piece(b_copy, col, 1)
            new_score, _ = minimax(b_copy, depth-1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, time.time() - start_time
