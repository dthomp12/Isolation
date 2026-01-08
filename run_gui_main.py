import tkinter as tk

from bots.example_bots import RandomBot, GreedyBot, MinimaxBot
from gui import IsolationGUI

# playerWhite = None
# playerBlack = MinimaxBot(depth=1)

playerWhite = MinimaxBot(depth=1, seed=42)
playerBlack = MinimaxBot(depth=4, seed=42)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Isolation+")
    IsolationGUI(root, playerWhite, playerBlack, move_delay_ms=200)
    root.mainloop()