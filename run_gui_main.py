import tkinter as tk

from bots.example_bots import RandomBot, GreedyBot, MinimaxBot
from bots.Bryant_bots import BlindGreedy, DiagonalBot, CornerBot, EdgeBot, WeightedMM
from gui import IsolationGUI

# # To play with two humans:
# playerWhite = None
# playerBlack = None

# To play against a bot:
playerWhite = None
playerBlack = WeightedMM()

# # To watch two bots play:
# playerWhite = MinimaxBot(depth=6)
# playerBlack = MinimaxBot(depth=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Isolation+")
    IsolationGUI(root, playerWhite, playerBlack, move_delay_ms=1000)
    root.mainloop()