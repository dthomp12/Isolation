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
    rays = [[None] * len(DIRECTIONS) for _ in range(size * size)]

    for r in range(size):
        for c in range(size):
            sq = r * size + c
            for d, (dr, dc) in enumerate(DIRECTIONS):
                ray = []
                nr, nc = r + dr, c + dc
                while 0 <= nr < size and 0 <= nc < size:
                    ray.append((nr, nc))
                    nr += dr
                    nc += dc
                rays[sq][d] = ray

    return rays

RAYS = precompute_rays(BOARD_SIZE)

# print(RAYS)

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
        board = [[EMPTY for _ in range(size)] for _ in range(size)]

        white_pos = (size // 2 - 1, size // 2 - 1)
        black_pos = (size // 2 + 1, size // 2 + 1)
        board[white_pos[0]][white_pos[1]] = PLAYER_WHITE
        board[black_pos[0]][black_pos[1]] = PLAYER_BLACK
        return IsolationState(board, white_pos, black_pos, PLAYER_WHITE)

    # def clone(self):
    #     """Shallow copy of board + positions, preserve current player and turn."""
    #     new_board = [row[:] for row in self.board]
    #     white_pos = tuple(self.white_pos)
    #     black_pos = tuple(self.black_pos)
    #     return IsolationState(new_board, white_pos, black_pos, self.current_player, self.turn)

    def clone(self):
        # return IsolationState(
        #     self.board.copy(),
        #     self.white_pos,
        #     self.black_pos,
        #     self.current_player,
        #     self.turn
        # )
        new_board = [row[:] for row in self.board]
        white_pos = tuple(self.white_pos)
        black_pos = tuple(self.black_pos)
        return IsolationState(new_board, white_pos, black_pos, self.current_player, self.turn)

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

        # Player and opponent positions
        r, c = self.white_pos if player == PLAYER_WHITE else self.black_pos
        ro, co = self.black_pos if player == PLAYER_WHITE else self.white_pos

        sq = r * BOARD_SIZE + c
        opp_sq = ro * BOARD_SIZE + co

        moves = []

        # Generate moves from player rays
        for ray in RAYS[sq]:
            for nr, nc in ray:
                if self.board[nr][nc] != EMPTY:
                    break

                # ---- safety check via opponent rays ----
                safe = True
                for opp_ray in RAYS[opp_sq]:
                    for tr, tc in opp_ray:
                        if self.board[tr][tc] == BLOCKED:
                            break
                        if (tr, tc) == (nr, nc):
                            safe = False
                            break
                        if self.board[tr][tc] != EMPTY:
                            break
                    if not safe:
                        break

                if safe:
                    moves.append((nr, nc))

        return moves

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
    # Just by making positions + direction tuples: 
    # 1.16 seconds
    #
    # Now, removing apply_move from is_safe_move (no copying whole board)
    # 0.89 seconds
    #
    # Precomputed movement rays from each position
    # 0.42 seconds
    #

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
            state.apply_move(moves[0])  # must assign new state
            t1 = time.perf_counter()
            total_apply += t1 - t0
    end = time.perf_counter()

    print(f"Total time: {end - start:.4f} seconds")
    print(f"Time spent in legal_moves: {total_legal:.4f} seconds")
    print(f"Time spent in apply_move: {total_apply:.4f} seconds")