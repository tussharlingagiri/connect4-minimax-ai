# simulate.py
import random
import time
from board import create_board, drop_piece, is_valid_location, get_valid_locations, check_win, AI, PLAYER
from ai_minimax import minimax


def random_move(board):
    valid_locations = get_valid_locations(board)
    return random.choice(valid_locations)


def simulate_game(ai_depth):
    board = create_board()
    game_over = False
    turn = random.choice([0, 1])  # Randomly start with AI or Random Player
    move_log = []
    winner = None

    while not game_over:
        if turn == 0:
            # Random player
            col = random_move(board)
            if is_valid_location(board, col):
                drop_piece(board, col, PLAYER)
                if check_win(board, PLAYER):
                    winner = "random"
                    game_over = True
        else:
            # AI player
            col, _ = minimax(board, ai_depth, -float("inf"), float("inf"), True)
            if is_valid_location(board, col):
                drop_piece(board, col, AI)
                if check_win(board, AI):
                    winner = "ai"
                    game_over = True

        if len(get_valid_locations(board)) == 0:
            game_over = True
            if winner is None:
                winner = "tie"

        turn = (turn + 1) % 2
    return winner


def simulate_many_games(n_games=100, ai_depth=4):
    results = {"ai": 0, "random": 0, "tie": 0}
    for i in range(n_games):
        result = simulate_game(ai_depth)
        results[result] += 1
        print(f"Game {i+1}/{n_games}: {result}")
    return results


if __name__ == "__main__":
    depth = 4
    games = 50
    results = simulate_many_games(n_games=games, ai_depth=depth)
    print(f"\nSimulated {games} games at depth {depth}")
    print("AI Wins:", results['ai'])
    print("Random Wins:", results['random'])
    print("Ties:", results['tie'])
