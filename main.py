from game import play
import sys

def menu():
    print("\n🎮 Welcome to Connect 4 with Minimax AI!")
    print("1. Play: Human vs AI")
    print("2. Exit")

    choice = input("Enter your choice (1-2): ")

    if choice == '1':
        play()
    elif choice == '2':
        print("Goodbye!")
        sys.exit()
    else:
        print("Invalid choice. Try again.")
        menu()

if __name__ == "__main__":
    menu()
