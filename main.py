"""
main.py — 2048 Game Controller

Handles the user loop, input, exception handling, and basic text rendering.
Imports logic from functions.py.
"""

from functions import (
    new_board, move_left, move_right, move_up, move_down,
    spawn_tile, has_move, won, as_text_grid, InvalidMove
)

# Starting the game

def main():
    board = new_board()
    score = 0

    print("~~~🔥 Game 2048 🔥~~~")
    print("Use W ↑/A ↓/S ←/D → to move; Q to quit; R to restart.\n")

    # Game loop
    while True:
        print(as_text_grid(board))
        print(f"👀 Score: {score}\n")

        # Read user input

        key = input("💫 Move (W ↑/A ↓/S ←/D →, R to restart, Q to quit): ").strip().lower()

        try:
            if key == "a":
                board, gained, moved = move_left(board)
            elif key == "d":
                board, gained, moved = move_right(board)
            elif key == "w":
                board, gained, moved = move_up(board)
            elif key == "s":
                board, gained, moved = move_down(board)
            elif key == "r":
                print("⏳Restarting...")
                print("🙌 New Game 🙌")
                board = new_board()
                score = 0
                continue
            elif key == "q":
                print("(„• ֊ •„)੭ Thanks for playing!")
                break
            else:
                raise InvalidMove("Invalid key. Use W/A/S/D, R, or Q.")

            # -----------------------------
            # Post-move handling
            # -----------------------------
            if not moved:
                raise InvalidMove("This move cannot change the board. Try something else!")

            score += gained
            spawn_tile(board)  # Add a new 2
            if won(board):
                print(as_text_grid(board))
                print(f"🎉🥳🎊 You won! Final score: {score}")
                while True:
                    again = input("🤗 Play again? (y/n): ").strip().lower()
                    if again == "y":
                        board, score = new_board(), 0
                        break
                    elif again == "n":
                        print("(„• ֊ •„)੭ Thanks for playing!")
                        return
                    else:
                        print("⚠︎ Please enter 'y' or 'n'!")

            if not has_move(board):
                print(as_text_grid(board))
                print(f"🥺🥀❤️‍🩹 Game over! Final score: {score}")
                while True:
                    again = input("🤗 Play again? (y/n): ").strip().lower()
                    if again == "y":
                        board, score = new_board(), 0
                        break
                    elif again == "n":
                        print("(„• ֊ •„)੭ Thanks for playing!")
                        return
                    else:
                        print("⚠︎ Please enter 'y' or 'n'!")

        except InvalidMove as e:
            print(f"⚠︎ {e}\n")
            # just reprint board and continue next iteration
            continue


if __name__ == "__main__":
    main()
