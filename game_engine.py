# game_engine.py
__all__ = [
    "IsolationState",
    "EMPTY", "BLOCKED",
    "PLAYER_WHITE", "PLAYER_BLACK",
    "BOARD_SIZE"
]

# Board pieces
EMPTY = 0
BLOCKED = -1
PLAYER_WHITE = 1  # first player
PLAYER_BLACK = 2  # second player

BOARD_SIZE = 7

DIRECTIONS = [
    (-1,  0), (1,  0), (0, -1), (0,  1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

class IsolationState:
    __slots__ = ["board", "positions", "current_player", "turn"]

    def __init__(self, board, positions, current_player, turn=0):
        self.board = board
        self.positions = positions
        self.current_player = current_player
        self.turn = turn

    @staticmethod
    def initial_state(size=BOARD_SIZE):
        """Return initial board state with white moving first."""
        board = [[EMPTY for _ in range(size)] for _ in range(size)]
        positions = {
            PLAYER_WHITE: (size // 2, size // 2 - 1),
            PLAYER_BLACK: (size // 2, size // 2 + 1)
        }
        board[positions[PLAYER_WHITE][0]][positions[PLAYER_WHITE][1]] = PLAYER_WHITE
        board[positions[PLAYER_BLACK][0]][positions[PLAYER_BLACK][1]] = PLAYER_BLACK
        return IsolationState(board, positions, PLAYER_WHITE)

    def clone(self):
        """Shallow copy of board + positions, preserve current player and turn."""
        new_board = [row[:] for row in self.board]
        new_positions = self.positions.copy()
        return IsolationState(new_board, new_positions, self.current_player, self.turn)

    def in_bounds(self, r, c):
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    @staticmethod
    def opponent(player):
        """Return the other player."""
        if player == PLAYER_WHITE:
            return PLAYER_BLACK
        elif player == PLAYER_BLACK:
            return PLAYER_WHITE
        else:
            raise ValueError(f"Invalid player: {player}")

    def legal_moves(self, player=None):
        if player is None:
            player = self.current_player
        r, c = self.positions[player]
        moves = []
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc) and self.board[nr][nc] == EMPTY:
                moves.append((nr, nc))
                nr += dr
                nc += dc
        return moves

    def is_terminal(self):
        return len(self.legal_moves()) == 0

    def winner(self):
        if not self.is_terminal():
            return None

        white_moves = self.legal_moves(PLAYER_WHITE)
        black_moves = self.legal_moves(PLAYER_BLACK)

        if not white_moves and not black_moves:
            return None  # Draw
        elif not self.legal_moves(self.current_player):
            return self.opponent(self.current_player)
        else:
            return self.current_player

    def apply_move(self, move):
        player = self.current_player
        opp = self.opponent(player)

        new = self.clone()
        r0, c0 = new.positions[player]
        r1, c1 = move

        # Block old square
        new.board[r0][c0] = BLOCKED

        # Move player piece
        new.board[r1][c1] = player
        new.positions[player] = (r1, c1)

        # Ensure opponent piece remains correct
        ro, co = new.positions[opp]
        new.board[ro][co] = opp

        # Switch turn
        new.current_player = opp
        new.turn += 1
        return new
