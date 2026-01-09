import numpy as np

# game_engine.py
__all__ = [
    "IsolationState",
    "EMPTY", "BLOCKED",
    "PLAYER_WHITE", "PLAYER_BLACK",
    "BOARD_SIZE", "RAYS"
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

def precompute_rays(size):
    rays = [[] for _ in range(size*size)]
    for r in range(size):
        for c in range(size):
            sq = r*size + c
            for dr, dc in DIRECTIONS:
                ray = []
                nr, nc = r+dr, c+dc
                while 0 <= nr < size and 0 <= nc < size:
                    ray.append(nr*size + nc)
                    nr += dr
                    nc += dc
                rays[sq].append(ray)
    return rays

RAYS = precompute_rays(BOARD_SIZE)

# print(RAYS)

class IsolationState:
    __slots__ = ["board", "white_pos", "black_pos", "current_player", "turn"]

    def __init__(self, board, white_pos, black_pos, current_player, turn=0):
        self.board = board # 1D numpy array of size BOARD_SIZE**2
        self.white_pos = white_pos # linear index
        self.black_pos = black_pos # linear index
        self.current_player = current_player
        self.turn = turn

    @staticmethod
    def initial_state(size=BOARD_SIZE):
        """Return initial board state with white moving first."""
        board = np.zeros(size*size, dtype=np.int8)
        white_pos = (size//2 - 1)*size + (size//2 - 1)
        black_pos = (size//2 + 1)*size + (size//2 + 1)
        board[white_pos] = PLAYER_WHITE
        board[black_pos] = PLAYER_BLACK
        return IsolationState(board, white_pos, black_pos, PLAYER_WHITE)

    def get_square(self, r, c):
        return self.board[r * BOARD_SIZE + c]
    
    def set_square(self, r, c, value):
        self.board[r * BOARD_SIZE + c] = value

    def clone(self):
        return IsolationState(
            self.board.copy(),
            self.white_pos,
            self.black_pos,
            self.current_player,
            self.turn
        )
        # new_board = [row[:] for row in self.board]
        # white_pos = tuple(self.white_pos)
        # black_pos = tuple(self.black_pos)
        # return IsolationState(new_board, white_pos, black_pos, self.current_player, self.turn)

    def in_bounds(self, r, c):
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    @staticmethod
    def opponent(player):
        """Return the other player."""
        return PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE

    def legal_moves(self, player=None):
            if player is None:
                player = self.current_player

            pos = self.white_pos if player == PLAYER_WHITE else self.black_pos
            moves = []

            # Opponent position
            opp_pos = self.black_pos if player == PLAYER_WHITE else self.white_pos

            # For each precomputed ray
            for ray in RAYS[pos]:
                for sq in ray:
                    if self.board[sq] != EMPTY:
                        break

                    # Convert linear index back to (r,c) for the bot
                    r, c = divmod(sq, BOARD_SIZE)

                    # Simple "not attacked" check
                    safe = True
                    for opp_ray in RAYS[opp_pos]:
                        if sq in opp_ray:
                            safe = False
                            break
                    if safe:
                        moves.append((r, c))

            return moves

    def is_terminal(self):
        return not self.legal_moves(self.current_player)

    def winner(self):
        if not self.is_terminal():
            return None

        return self.opponent(self.current_player)

    def apply_move(self, move):
            r, c = move
            sq = r*BOARD_SIZE + c
            player = self.current_player
            opp = self.opponent(player)

            new_board = self.board.copy()
            old_pos = self.white_pos if player == PLAYER_WHITE else self.black_pos
            new_board[old_pos] = BLOCKED
            new_board[sq] = player

            white_pos = self.white_pos if player == PLAYER_BLACK else sq
            black_pos = self.black_pos if player == PLAYER_WHITE else sq

            return IsolationState(new_board, white_pos, black_pos, opp, self.turn+1)

import time

if __name__ == "__main__":
    # Benchmarking Times:
    #
    # Base time for 10,000 calls to legal_moves in starting position
    # 1.19 s
    #
    # Just by making positions + direction tuples: 
    # 1.16 seconds
    #
    # Now, removing apply_move from is_safe_move (no copying whole board)
    # 0.89 seconds
    #
    # Precomputed movement rays from each position
    # 0.42 seconds
    #
    # Converting board to 1D
    # 0.085 seconds

    state = IsolationState.initial_state()

    N = 10_000
    # N = 1

    total_legal = 0.0
    total_apply = 0.0

    start = time.perf_counter()
    for _ in range(N):
        t0 = time.perf_counter()
        moves = state.legal_moves()
        t1 = time.perf_counter()
        total_legal += t1 - t0

        if moves:
            t0 = time.perf_counter()
            state.apply_move(moves[0])
            t1 = time.perf_counter()
            total_apply += t1 - t0
    end = time.perf_counter()

    print(f"Total time: {end - start:.4f} seconds")
    print(f"Time spent in legal_moves: {total_legal:.4f} seconds")
    print(f"Time spent in apply_move: {total_apply:.4f} seconds")