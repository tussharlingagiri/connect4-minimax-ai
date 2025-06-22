# ai_minimax.py

import math
import random
from constants import PLAYER, AI
from game_board import get_valid_locations, drop_piece, check_win
from evaluation import score_position

def is_terminal_node(board):
    return check_win(board, PLAYER) or check_win(board, AI) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, AI):
                return (None, float('inf'))
            elif check_win(board, PLAYER):
                return (None, -float('inf'))
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
