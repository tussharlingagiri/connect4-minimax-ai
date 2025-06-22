import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def create_logger():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"game_{timestamp}.txt")
    return open(log_path, "w"), log_path

def log_move(log_file, player, column):
    entry = f"{'Player 1' if player == 1 else 'AI':<10} -> Column {column}"
    log_file.write(entry + "\n")
    log_file.flush()
