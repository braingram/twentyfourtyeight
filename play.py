from pynput import keyboard

import tfe

KEYMAP = {
    keyboard.Key.up: tfe.UP,
    keyboard.Key.down: tfe.DOWN,
    keyboard.Key.left: tfe.LEFT,
    keyboard.Key.right: tfe.RIGHT,
}

global board
print("Arrow keys to move, q to quit\n")
board = tfe.Board()
print(board)

def on_press(key):
    if getattr(key, "char", "") == "q":
        return False
    global board
    if key in KEYMAP:
        try:
            board.move(KEYMAP[key])
        except tfe.GameOver:
            print("Game over!")
            print(f"Final score: {board.score}")
            return False
    print(board)


with keyboard.Listener(on_press=on_press, suppress=True) as listener:
    listener.join()
