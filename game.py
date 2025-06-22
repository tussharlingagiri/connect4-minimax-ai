from board import *
from ai_minimax import minimax
import math

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
                    print_board(board)
                    print("PLAYER 1 WINS!")
                    game_over = True
        else:
            col, _ = minimax(board, 4, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                drop_piece(board, col, AI)
                if check_win(board, AI):
                    print_board(board)
                    print("AI WINS!")
                    game_over = True

        turn = (turn + 1) % 2

def print_board(board):
    print("\n".join(str(row) for row in board))
    print()
