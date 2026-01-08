import math

from game_engine import IsolationState, PLAYER_WHITE, PLAYER_BLACK
from bots.bot_base import Bot_Base_Class

class RandomBot(Bot_Base_Class):
    def choose_move(self, state : IsolationState):
        moves = state.legal_moves()
        return self.rng.choice(moves) if moves else None

# This bot is the same as using the MinimaxBot with the evaluate_greedy function at a depth of 1
class GreedyBot(Bot_Base_Class):
    def choose_move(self, state: IsolationState):
        player = state.current_player
        best_score = float("-inf")
        best_moves = []

        for move in state.legal_moves():
            next_state = state.apply_move(move)
            my_moves = len(next_state.legal_moves(player))
            opp_moves = len(next_state.legal_moves(IsolationState.opponent(player)))
            score = my_moves - opp_moves

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        if best_moves:
            return self.rng.choice(best_moves)
        return None

# Example evaluation function: Difference in legal moves in the position
def evaluate_greedy(state, player):
    """
    Heuristic: difference in legal moves
    """
    opp = PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE
    return len(state.legal_moves(player)) - len(state.legal_moves(opp))

class MinimaxBot(Bot_Base_Class):
    def __init__(self, depth=3, eval_func=evaluate_greedy, seed=None):
        super().__init__(seed)
        self.depth = depth
        self.eval_func = eval_func

    def choose_move(self, state):
        self.player = state.current_player

        def minimax(state, depth, alpha, beta, maximizing):
            if depth == 0 or state.is_terminal():
                return self.eval_func(state, self.player), None

            moves = state.legal_moves(state.current_player)
            if not moves:
                return self.eval_func(state, self.player), None

            best_moves = []
            if maximizing:
                max_eval = -math.inf
                for move in moves:
                    child = state.apply_move(move)
                    eval_score, _ = minimax(child, depth-1, alpha, beta, False)

                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_moves = [move]
                    elif eval_score == max_eval:
                        best_moves.append(move)

                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break

                chosen_move = self.rng.choice(best_moves)
                return max_eval, chosen_move

            else:  # minimizing
                min_eval = math.inf
                for move in moves:
                    child = state.apply_move(move)
                    eval_score, _ = minimax(child, depth-1, alpha, beta, True)

                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_moves = [move]
                    elif eval_score == min_eval:
                        best_moves.append(move)

                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break

                chosen_move = self.rng.choice(best_moves)
                return min_eval, chosen_move

        _, move = minimax(state, self.depth, -math.inf, math.inf, state.current_player == self.player)
        return move
    
class TemplateBot(Bot_Base_Class):
    def choose_move(self, state):
        # Here goes your code
        pass