# gui.py
import tkinter as tk
from copy import deepcopy

from game_engine import *

CELL_SIZE = 80


HIGHLIGHT_COLOR = "#90CAF9"

SQUARE_COLORS = {
    EMPTY: "#f5f5dc",   # light beige
    BLOCKED: "#444444", # dark gray
    PLAYER_WHITE: "#FFFFFF",  # white
    PLAYER_BLACK: "#000000"   # black
}

PLAYER_LABELS = {
    PLAYER_WHITE: "W",
    PLAYER_BLACK: "B"
}

class MoveNode:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.move = move              # the move that led to this state (None for root)
        self.parent = parent
        self.children = []            # list of MoveNode
        self.alg_move = None          # cache the algebraic notation

        if move and parent:
            self.alg_move = self._move_to_alg(move)

    def _move_to_alg(self, move):
        r, c = move
        return chr(ord('A') + c) + str(BOARD_SIZE - r)

class IsolationGUI:
    def __init__(self, root, player_white=None, player_black=None, move_delay_ms=300):
        self.root = root
        self.initial_state = IsolationState.initial_state()
        
        # Players: None = human, otherwise = bot with .choose_move(state) method
        self.players = {
            PLAYER_WHITE: player_white,
            PLAYER_BLACK: player_black
        }
        
        self.move_delay_ms = move_delay_ms
        self.root_node = MoveNode(deepcopy(self.initial_state))
        self.current_path = [self.root_node]   # list of nodes → current position is last one
        self.mode = 'play'                                 # 'play' or 'analysis'
        self.label_offset = 30                             # space for coordinates
        self.path_index = 0
        
        # UI setup
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)
        
        self.canvas = tk.Canvas(
            self.main_frame,
            width=BOARD_SIZE * CELL_SIZE + 2 * self.label_offset,
            height=BOARD_SIZE * CELL_SIZE + 2 * self.label_offset
        )
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Sidebar
        sidebar = tk.Frame(self.main_frame, width=220)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        self.move_listbox = tk.Listbox(
            sidebar, 
            width=35, 
            height=20, 
            font=("Courier", 12),
            selectbackground="#d0e8ff"
        )
        self.move_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        
        nav = tk.Frame(sidebar)
        nav.pack(pady=5)
        tk.Button(nav, text="<<", width=4, command=self.first).pack(side=tk.LEFT)
        tk.Button(nav, text="<",  width=4, command=self.prev).pack(side=tk.LEFT)
        tk.Button(nav, text=">",  width=4, command=self.next).pack(side=tk.LEFT)
        tk.Button(nav, text=">>", width=4, command=self.last).pack(side=tk.LEFT)
        
        self.mode_btn = tk.Button(sidebar, text="Analysis Mode", command=self.toggle_mode, state=tk.DISABLED)
        self.mode_btn.pack(pady=10)
        
        self.status = tk.Label(root, text="White to move", font=("Arial", 14))
        self.status.pack(pady=5)
        
        self.redraw()

    @property
    def current_node(self):
        return self.current_path[self.path_index]

    @property
    def current_state(self):
        return self.current_node.state

    def is_human_turn(self):
        return self.players[self.current_state.current_player] is None

    def current_player(self):
        return self.players.get(self.current_state.current_player)

    def coord_to_alg(self, r, c):
        col = chr(ord('A') + c)
        row = BOARD_SIZE - r  # 1 at bottom, BOARD_SIZE at top
        return f"{col}{row}"

    def toggle_mode(self):
        if self.mode == 'play':
            if not (self.current_state.is_initial() or self.current_state.is_terminal()):
                return # safety - shouldn't happen but...
            self.mode = 'analysis'
            self.mode_btn.config(text="Back to Game View")
        else:
            self.mode = 'play'
            self.mode_btn.config(text="Analyze Game")
        self.redraw()

    def can_enter_analysis(self):
        return self.current_state.is_initial() or self.current_state.is_terminal()

    def first(self):
        self.path_index = 0
        self.redraw()

    def prev(self):
        if self.path_index > 0:
            self.path_index -= 1
            self.redraw()

    def next(self):
        if self.path_index < len(self.current_path)-1:
            self.path_index += 1
            self.redraw()

    def last(self):
        self.path_index = len(self.current_path)-1
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")

        display_state = self.current_state
        self.legal = display_state.legal_moves()
        offset = self.label_offset

        # Enable analysis only at root or terminal
        self.mode_btn.config(
            state=tk.NORMAL if self.can_enter_analysis() else tk.DISABLED
        )

        # ----------------------------
        # Coordinates
        # ----------------------------
        for r in range(BOARD_SIZE):
            y = offset + r * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_text(
                offset // 2, y,
                text=str(BOARD_SIZE - r),
                font=("Arial", 12)
            )

        for c in range(BOARD_SIZE):
            x = offset + c * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_text(
                x,
                offset + BOARD_SIZE * CELL_SIZE + offset // 2,
                text=chr(ord('A') + c),
                font=("Arial", 12)
            )

        # ----------------------------
        # Board
        # ----------------------------
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x0 = offset + c * CELL_SIZE
                y0 = offset + r * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                cell = display_state.get_square(r, c)

                if cell in (PLAYER_WHITE, PLAYER_BLACK):
                    color = SQUARE_COLORS[EMPTY]
                else:
                    color = SQUARE_COLORS[cell]

                # Highlight legal moves only if at end of current path
                if self.mode == 'play' and self.path_index == len(self.current_path)-1 or self.mode == 'analysis':
                    if (r, c) in self.legal:
                        color = HIGHLIGHT_COLOR

                self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=color,
                    outline="black",
                    width=2
                )

                if cell in (PLAYER_WHITE, PLAYER_BLACK):
                    self._draw_piece(r, c, PLAYER_LABELS[cell], display_state, offset)

        # ----------------------------
        # Status text
        # ----------------------------
        if display_state.is_terminal():
            winner = display_state.winner()
            if winner == PLAYER_WHITE:
                text = "Game Over — White wins"
            elif winner == PLAYER_BLACK:
                text = "Game Over — Black wins"
            else:
                text = "Game Over — Draw"
        elif len(self.current_path) == 1:
            text = "Start position — White to move"
        else:
            text = (
                "White to move"
                if display_state.current_player == PLAYER_WHITE
                else "Black to move"
            )

        self.status.config(text=text)

        # ----------------------------
        # Move list (derived from path)
        # ----------------------------
        self.move_listbox.delete(0, tk.END)

        moves = [n.alg_move for n in self.current_path[1:]]
        for i in range(0, len(moves), 2):
            turn = i // 2 + 1
            w = moves[i]
            b = moves[i + 1] if i + 1 < len(moves) else ""
            self.move_listbox.insert(tk.END, f"{turn:2d}.  {w:5}    {b:5}")

        # Highlight current ply in analysis mode
        if moves:
            ply = self.path_index - 1
            if ply >= 0:
                row = ply // 2
                self.move_listbox.selection_clear(0, tk.END)
                self.move_listbox.selection_set(row)
                self.move_listbox.see(row)

        # ----------------------------
        # Bot autoplay
        # ----------------------------
        if self.mode == 'play' and not display_state.is_terminal():
            self.root.after(self.move_delay_ms, self._try_bot_move)

    def _draw_piece(self, r, c, label, state, offset):
        x = offset + c * CELL_SIZE + CELL_SIZE // 2
        y = offset + r * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 10
        cell = state.get_square(r, c)
        color = SQUARE_COLORS[cell]
        outline = "black"
        
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline=outline, width=3)
        if label:
            text_color = "black" if cell == PLAYER_WHITE else "white"
            self.canvas.create_text(x, y, text=label, font=("Arial", 18, "bold"), fill=text_color)

    def on_click(self, event):
        if self.mode == 'play' and self.path_index != len(self.current_path) - 1: return

        if self.mode == 'analysis':
            if not self.is_human_turn():
                return
            offset = self.label_offset
            c = (event.x - offset) // CELL_SIZE
            r = (event.y - offset) // CELL_SIZE
            
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                move = (r, c)
                if move in self.current_state.legal_moves():
                    self.apply_move_in_current_path(move)

        elif self.mode == 'play':
            if self.current_state.is_terminal(): return
            if not self.is_human_turn(): return
            
            offset = self.label_offset
            c = (event.x - offset) // CELL_SIZE
            r = (event.y - offset) // CELL_SIZE
            
            move = (r, c)
            if move in self.current_state.legal_moves():
                self.apply_move_in_current_path(move)
                self.redraw()

    def rebuild_current_path(self, node):
        self.current_path = []
        while node:
            self.current_path.append(node)
            node = node.parent
        self.current_path.reverse()

    def apply_move_in_current_path(self, move):
        if move not in self.current_state.legal_moves():
            return False

        del self.current_path[self.path_index+1:]

        # also delete children beyond this node
        self.current_node.children.clear()

        new_state = self.current_state.apply_move(move)
        new_node = MoveNode(deepcopy(new_state), move, self.current_node)

        self.current_node.children.append(new_node)
        self.current_path.append(new_node)
        self.path_index += 1

        self.redraw()
        return True
    
    # def go_to_path_index(self, index):
    #     """Jump to position index along current path (0 = start)"""
    #     if 0 <= index < len(self.current_path):
    #         self.current_path = self.current_path[:index+1]
    #         self.move_history = [n.alg_move for n in self.current_path[1:]]
    #         self.redraw()

    def _try_bot_move(self):
        if self.path_index != len(self.current_path) - 1:
            return
        if self.mode != 'play': return
        if self.current_state.is_terminal(): return

        bot = self.current_player()
        if bot is None: return

        move = bot.choose_move(self.current_state)
        if move:
            self.apply_move_in_current_path(move)
            self.redraw()
