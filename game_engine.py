import numpy as np

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

DIRECTIONS = (
    (-1,  0), (1,  0), (0, -1), (0,  1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
)

class IsolationState:
    __slots__ = ["board", "white_pos", "black_pos", "current_player", "turn"]

    def __init__(self, board, white_pos, black_pos, current_player, turn=0):
        self.board = board
        self.white_pos = white_pos
        self.black_pos = black_pos
        self.current_player = current_player
        self.turn = turn

    @staticmethod
    def initial_state(size=BOARD_SIZE):
        """Return initial board state with white moving first."""
        board = np.zeros((size, size), dtype=np.int8)
        # positions = np.zeros((3, 2), dtype=np.int8)

        # positions[PLAYER_WHITE] = (size // 2 - 1, size // 2 - 1)
        # positions[PLAYER_BLACK] = (size // 2 + 1, size // 2 + 1)
        # board[tuple(positions[PLAYER_WHITE])] = PLAYER_WHITE
        # board[tuple(positions[PLAYER_BLACK])] = PLAYER_BLACK
        white_pos = (size // 2 - 1, size // 2 - 1)
        black_pos = (size // 2 + 1, size // 2 + 1)
        board[white_pos] = PLAYER_WHITE
        board[black_pos] = PLAYER_BLACK
        return IsolationState(board, white_pos, black_pos, PLAYER_WHITE)

    # def clone(self):
    #     """Shallow copy of board + positions, preserve current player and turn."""
    #     new_board = [row[:] for row in self.board]
    #     white_pos = tuple(self.white_pos)
    #     black_pos = tuple(self.black_pos)
    #     return IsolationState(new_board, white_pos, black_pos, self.current_player, self.turn)

    def clone(self):
        return IsolationState(
            self.board.copy(),
            self.white_pos,
            self.black_pos,
            self.current_player,
            self.turn
        )

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
        
    def attacked_squares(self, player):
        """Return all squares that `player` could move to."""
        r, c = self.white_pos if player == PLAYER_WHITE else self.black_pos
        attacked = set()

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc):
                attacked.add((nr, nc))
                if self.board[nr][nc] != EMPTY:
                    break
                nr += dr
                nc += dc
        
        return attacked
    
    def is_safe_move(self, move, player=None):
        if player is None:
            player = self.current_player

        next_state = self.apply_move(move)
        opponent = self.opponent(player)

        player_pos = (
            next_state.white_pos
            if player == PLAYER_WHITE
            else next_state.black_pos
        )

        return player_pos not in next_state.attacked_squares(opponent)

    def legal_moves(self, player=None):
        if player is None:
            player = self.current_player

        r, c = self.white_pos if player == PLAYER_WHITE else self.black_pos
        
        moves = []

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc) and self.board[nr][nc] == EMPTY:
                move = (nr, nc)
                
                if self.is_safe_move(move, player):
                    moves.append(move)

                nr += dr
                nc += dc

        return moves
    
    # def legal_moves(self, player=None):
    #     if player is None:
    #         player = self.current_player
    #     r, c = self.positions[player]
    #     moves = []
    #     for dr, dc in DIRECTIONS:
    #         nr, nc = r + dr, c + dc
    #         while self.in_bounds(nr, nc) and self.board[nr][nc] == EMPTY:
    #             moves.append((nr, nc))
    #             nr += dr
    #             nc += dc
    #     return moves

    def is_terminal(self):
        return not self.legal_moves(self.current_player)

    def winner(self):
        if not self.is_terminal():
            return None

        return self.opponent(self.current_player)

    def apply_move(self, move):
        player = self.current_player
        opp = self.opponent(player)

        new = self.clone()
        r0, c0 = new.white_pos if player == PLAYER_WHITE else new.black_pos
        r1, c1 = move

        # Block old square
        new.board[r0][c0] = BLOCKED

        # Move player piece
        new.board[r1][c1] = player
        if player == PLAYER_WHITE:
            new.white_pos = (r1, c1)
            ro, co = new.black_pos
        else:
            new.black_pos = (r1, c1)
            ro, co = new.white_pos

        # Ensure opponent piece remains correct
        new.board[ro][co] = opp

        # Switch turn
        new.current_player = opp
        new.turn += 1
        return new

import time

if __name__ == "__main__":
    # Benchmarking Times:
    #
    # Base time for 10,000 calls to legal_moves in starting position
    # 1.19 s
    #
    # Just by making the board a numpy arrays, and positions + direction tuples: 
    # 1.88 seconds
    #
    #
    #
    #
    #
    #

    state = IsolationState.initial_state()

    N = 10_000
    # N = 25

    start = time.perf_counter()
    for _ in range(N):
        moves = state.legal_moves()
        if moves:
            state.apply_move(moves[0])
    end = time.perf_counter()

    print(f"Current time to get legal_moves 10,000 times : {end - start:.4f} seconds")