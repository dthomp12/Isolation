
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
NUM_SQUARES = BOARD_SIZE * BOARD_SIZE

FULL_BOARD_MASK = (1 << NUM_SQUARES) - 1

DIRECTIONS = (
    (-1,  0), (1,  0), (0, -1), (0,  1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
)

# Precompute rays as bitmasks for each square & direction
def precompute_rays_bitmask(size=BOARD_SIZE):
    rays = [[0]*8 for _ in range(NUM_SQUARES)]
    for r in range(size):
        for c in range(size):
            sq = r*size + c
            for d, (dr, dc) in enumerate(DIRECTIONS):
                nr, nc = r + dr, c + dc
                mask = 0
                while 0 <= nr < size and 0 <= nc < size:
                    mask |= 1 << (nr*size + nc)
                    nr += dr
                    nc += dc
                rays[sq][d] = mask
    return rays

RAYS_BITS = precompute_rays_bitmask()

class IsolationState:
    __slots__ = ["white_bb", "black_bb", "blocked_bb", "white_sq", "black_sq", "current_player", "turn"]

    def __init__(self, white_bb, black_bb, blocked_bb,
                 white_sq, black_sq, current_player, turn=0):
        self.white_bb = white_bb
        self.black_bb = black_bb
        self.blocked_bb = blocked_bb
        self.white_sq = white_sq
        self.black_sq = black_sq
        self.current_player = current_player
        self.turn = turn

    @staticmethod
    def initial_state():
        white_sq = (BOARD_SIZE // 2 - 1) * BOARD_SIZE + (BOARD_SIZE // 2 - 1)
        black_sq = (BOARD_SIZE // 2 + 1) * BOARD_SIZE + (BOARD_SIZE // 2 + 1)
        white_bb = 1 << white_sq
        black_bb = 1 << black_sq
        blocked_bb = 0
        return IsolationState(white_bb, black_bb, blocked_bb,
                              white_sq, black_sq, PLAYER_WHITE)

    def clone(self):
        return IsolationState(
            self.white_bb, self.black_bb, self.blocked_bb,
            self.white_sq, self.black_sq, self.current_player, self.turn
        )

    def opponent(self, player):
        return PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE

    def _pos_bb(self, player):
        return self.white_bb if player == PLAYER_WHITE else self.black_bb

    def _all_occupied(self):
        return self.white_bb | self.black_bb | self.blocked_bb

    def legal_moves(self, player=None):
        if player is None:
            player = self.current_player

        moves = []
        player_sq = self.white_sq if player == PLAYER_WHITE else self.black_sq
        opp_sq = self.black_sq if player == PLAYER_WHITE else self.white_sq

        occupied = self._all_occupied()

        # Precompute opponent attack mask
        opp_attack_mask = 0
        for ray in RAYS_BITS[opp_sq]:
            opp_attack_mask |= ray

        # Iterate over rays from player position
        for ray in RAYS_BITS[player_sq]:
            # Mask ray with empty squares
            ray_moves = ray & ~occupied
            # Remove unsafe squares
            ray_moves &= ~opp_attack_mask

            # Extract bits efficiently
            while ray_moves:
                lsb = ray_moves & -ray_moves
                sq = (lsb).bit_length() - 1
                r, c = divmod(sq, BOARD_SIZE)
                moves.append((r, c))
                ray_moves ^= lsb  # remove lowest bit

        return moves

    def apply_move(self, move):
        r, c = move
        sq = r * BOARD_SIZE + c
        player = self.current_player
        opp = self.opponent(player)

        new_white_bb = self.white_bb
        new_black_bb = self.black_bb
        new_blocked_bb = self.blocked_bb
        new_white_sq = self.white_sq
        new_black_sq = self.black_sq

        old_sq = self.white_sq if player == PLAYER_WHITE else self.black_sq
        new_blocked_bb |= 1 << old_sq

        if player == PLAYER_WHITE:
            new_white_bb = 1 << sq
            new_white_sq = sq
        else:
            new_black_bb = 1 << sq
            new_black_sq = sq

        return IsolationState(
            new_white_bb, new_black_bb, new_blocked_bb,
            new_white_sq, new_black_sq, opp, self.turn + 1
        )

    def is_terminal(self):
        return len(self.legal_moves()) == 0

    def winner(self):
        if not self.is_terminal():
            return None

        return self.opponent(self.current_player)
    
    # --- Bitboard helpers for square access ---

    def get_square(self, r, c):
        """Return EMPTY, PLAYER_WHITE, or PLAYER_BLACK at (r,c)"""
        sq = r * BOARD_SIZE + c
        bit = 1 << sq
        if self.white_bb & bit:
            return PLAYER_WHITE
        elif self.black_bb & bit:
            return PLAYER_BLACK
        elif self.blocked_bb & bit:
            return BLOCKED
        else:
            return EMPTY

    def set_square(self, r, c, value):
        """Set the square (r,c) to EMPTY, PLAYER_WHITE, PLAYER_BLACK, or BLOCKED"""
        sq = r * BOARD_SIZE + c
        bit = 1 << sq

        # Clear any piece on that square first
        self.white_bb &= ~bit
        self.black_bb &= ~bit
        self.blocked_bb &= ~bit

        # Set new value
        if value == PLAYER_WHITE:
            self.white_bb |= bit
        elif value == PLAYER_BLACK:
            self.black_bb |= bit
        elif value == BLOCKED:
            self.blocked_bb |= bit
        # EMPTY does nothing else

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