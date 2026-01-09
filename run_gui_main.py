import tkinter as tk

from bots.example_bots import RandomBot, GreedyBot, MinimaxBot
from gui import IsolationGUI

# # To play with two humans:
# playerWhite = None
# playerBlack = None

# To play against a bot:
# playerWhite = None
# playerBlack = None

# # To watch two bots play:
playerWhite = RandomBot()
playerBlack = RandomBot()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Isolation+")
    IsolationGUI(root, playerWhite, playerBlack, move_delay_ms=50)
    root.mainloop()