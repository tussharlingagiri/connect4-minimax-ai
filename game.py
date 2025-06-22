from board import *
from ai_minimax import minimax
from logger import create_logger, log_move
import math

PLAYER = 1
AI = 2

def play():
    board = create_board()
    game_over = False
    turn = 0  # 0 = Player, 1 = AI
    log_file, log_path = create_logger()

    while not game_over:
        print_board(board)
        if turn == 0:
            try:
                col = int(input("Player 1 Make your Selection (0-6): "))
            except ValueError:
                print("🚫 Invalid input. Please enter a number between 0 and 6.")
                continue
            if col < 0 or col > 6:
                print("🚫 Invalid column. Please choose between 0 and 6.")
                continue
            if is_valid_location(board, col):
                drop_piece(board, col, PLAYER)
                log_move(log_file, PLAYER, col)
                if check_win(board, PLAYER):
                    print_board(board)
                    print("🎉 PLAYER 1 WINS!")
                    log_file.write("🎉 PLAYER 1 WINS!\n")
                    game_over = True
        else:
            col, _ = minimax(board, 4, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                drop_piece(board, col, AI)
                log_move(log_file, AI, col)
                if check_win(board, AI):
                    print_board(board)
                    print("🤖 AI WINS!")
                    log_file.write("🤖 AI WINS!\n")
                    game_over = True

        turn = (turn + 1) % 2

    log_file.close()

def print_board(board):
    print("\n".join(str(row) for row in board))
    print()
