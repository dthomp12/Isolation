# gui.py
import tkinter as tk

from game_engine import *

CELL_SIZE = 80

BOARD_COLOR = "#f5f5dc"   # light beige
BLOCKED_COLOR = "#444444" # dark gray
HIGHLIGHT_COLOR = "#90CAF9"

PLAYER_COLORS = {
    PLAYER_WHITE: "#FFFFFF",  # white
    PLAYER_BLACK: "#000000"   # black
}

PLAYER_LABELS = {
    PLAYER_WHITE: "W",
    PLAYER_BLACK: "B"
}


class IsolationGUI:
    def __init__(self, root, playerWhite=None, playerBlack=None, move_delay_ms=100):
        self.root = root
        self.state = IsolationState.initial_state()

        self.bots = {
            PLAYER_WHITE: playerWhite,
            PLAYER_BLACK: playerBlack
        }

        self.move_delay_ms = move_delay_ms
        self.legal = []

        self.canvas = tk.Canvas(
            root,
            width=BOARD_SIZE * CELL_SIZE,
            height=BOARD_SIZE * CELL_SIZE
        )
        self.canvas.pack()

        self.status = tk.Label(root, text="", font=("Arial", 14))
        self.status.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.redraw()

    def current_bot(self):
        return self.bots.get(self.state.current_player)

    def redraw(self):
        self.canvas.delete("all")
        self.legal = self.state.legal_moves()

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x0 = c * CELL_SIZE
                y0 = r * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                cell = self.state.get_square(r, c)

                # Determine cell color
                if cell == EMPTY:
                    color = BOARD_COLOR
                elif cell == BLOCKED:
                    color = BLOCKED_COLOR
                else:
                    color = PLAYER_COLORS[cell]

                # Highlight legal moves
                if (r, c) in self.legal:
                    color = HIGHLIGHT_COLOR

                # Optional: highlight current player piece border
                if cell in (PLAYER_WHITE, PLAYER_BLACK):
                    outline_color = "gold" if self.state.current_player == cell else "black"
                else:
                    outline_color = "black"

                self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=color,
                    outline=outline_color,
                    width=2
                )

                # Draw piece label
                if cell in (PLAYER_WHITE, PLAYER_BLACK):
                    self.draw_piece(r, c, PLAYER_LABELS[cell])

        # Update status text
        if self.state.is_terminal():
            winner = self.state.winner()
            if winner == PLAYER_WHITE:
                self.status.config(text="Game Over! Winner: White")
            elif winner == PLAYER_BLACK:
                self.status.config(text="Game Over! Winner: Black")
            else:
                self.status.config(text="Game Over! Draw")
        else:
            player = "White" if self.state.current_player == PLAYER_WHITE else "Black"
            self.status.config(text=f"Turn: {player}")

        # Schedule bot move if needed
        self.root.after(self.move_delay_ms, self.maybe_bot_move)

    def draw_piece(self, r, c, label=None):
        """
        Draw a piece as a filled circle on the board.
        r, c: row and column
        label: optional 'W' or 'B'
        """
        # Center coordinates
        x = c * CELL_SIZE + CELL_SIZE // 2
        y = r * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 8  # padding from edges

        cell = self.state.get_square(r,c)
        color = PLAYER_COLORS[cell]

        # Draw circle with border
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline="gold" if self.state.current_player == cell else PLAYER_COLORS[self.state.current_player],
            width=2
        )

        # Optional label inside piece
        if label:
            # Choose contrasting color for label
            text_color = "black" if cell == PLAYER_WHITE else "white"
            self.canvas.create_text(
                x, y,
                text=label,
                font=("Arial", 16, "bold"),
                fill=text_color
            )

    def on_click(self, event):
        if self.state.is_terminal():
            return

        if self.current_bot() is not None:
            return

        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE

        if (r, c) in self.legal:
            self.state = self.state.apply_move((r, c))
            self.redraw()

    def maybe_bot_move(self):
        if self.state.is_terminal():
            return

        bot = self.current_bot()
        if bot is None:
            return

        move = bot.choose_move(self.state)
        if move is not None:
            self.state = self.state.apply_move(move)
            self.redraw()
