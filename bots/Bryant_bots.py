import math

from game_engine import IsolationState, PLAYER_WHITE, PLAYER_BLACK
from bots.bot_base import Bot_Base_Class

class DiagonalBot(Bot_Base_Class):
    def choose_move(self, state : IsolationState):
        best_score = math.inf
        best_moves = []
      
        player = state.current_player

        for move in state.legal_moves():
            score = abs(move[0] - move[1])
            next_state = state.apply_move(move)
            my_moves = next_state.legal_moves()
            

            if len(my_moves) <= 1:
                score += math.inf

            if score < best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        if best_moves:
            return self.rng.choice(best_moves)
        return None

class CornerBot(Bot_Base_Class):
    def choose_move(self, state : IsolationState):
        best_score = -math.inf
        best_moves = []

        player = state.current_player

        for move in state.legal_moves():
            score = move[0] + move[1]
            next_state = state.apply_move(move)
            my_moves = next_state.legal_moves()

            if len(my_moves) <= 1:
                score -= math.inf

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        if best_moves:
            return self.rng.choice(best_moves)
        return None

class EdgeBot(Bot_Base_Class):
    def choose_move(self, state : IsolationState):
        movematrix = [00,20,20,20,20,20,00,
                      20,10,10,10,10,10,20,
                      20,10,00,00,00,40,20,
                      20,10,00,00,00,10,20,
                      20,10,00,00,00,10,20,
                      20,10,10,10,10,10,20,
                      00,20,20,20,20,20,00]
        best_score = -math.inf
        best_moves = []

        player = state.current_player

        for move in state.legal_moves():
            score = movematrix[move[1] + 7*move[0]]
            next_state = state.apply_move(move)
            my_moves = next_state.legal_moves()
            opp_moves = next_state.legal_moves(state.opponent(player))

            if len(opp_moves) <=3:
                score = math.inf

            if len(my_moves) <= 1:
                score = -math.inf

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        if best_moves:
            return self.rng.choice(best_moves)
        return None

    
def blind_greedy(state, player):
    """
    Heuristic: Tries to maximize own moves
    """
    # If game is over and we won, give massive weight
    if state.is_terminal():
        if state.winner() == player:
            return math.inf
        else:
            return -math.inf

    return len(state.legal_moves(player))

class BlindGreedy(Bot_Base_Class):
    def __init__(self, depth=3, eval_func=blind_greedy, seed=None):
        super().__init__(seed)
        self.depth = depth
        self.eval_func = eval_func

    def choose_move(self, state):
        self.player = state.current_player

        def minimax(state, depth, alpha, beta, maximizing):
            if depth == 0 or state.is_terminal():
                return self.eval_func(state, self.player), None

            moves = state.legal_moves(state.current_player)
            self.rng.shuffle(moves)
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

def agro_greedy(state, player):
    """
    Heuristic: Tries to pin opponent
    """
    # If game is over and we won, give massive weight
    if state.is_terminal():
        if state.winner() == player:
            return math.inf
        else:
            return -math.inf

    return -len(state.legal_moves(state.opponent(player)))

class AgroGreedy(Bot_Base_Class):
    def __init__(self, depth=3, eval_func=agro_greedy, seed=None):
        super().__init__(seed)
        self.depth = depth
        self.eval_func = eval_func

    def choose_move(self, state):
        self.player = state.current_player

        def minimax(state, depth, alpha, beta, maximizing):
            if depth == 0 or state.is_terminal():
                return self.eval_func(state, self.player), None

            moves = state.legal_moves(state.current_player)
            self.rng.shuffle(moves)
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

def weighted_greedy(state, player):
    """
    Heuristic: difference in legal moves with weights applied
    """
    # If game is over and we won, give massive weight
    if state.is_terminal():
        if state.winner() == player:
            return math.inf
        else:
            return -math.inf
    opp = state.opponent(player)
    val = len(13*state.legal_moves(player)) - 19*len(state.legal_moves(opp))
    return val



class WeightedMM(Bot_Base_Class):
    def __init__(self, depth=3, eval_func=weighted_greedy, seed=None):
        super().__init__(seed)
        self.depth = depth
        self.eval_func = eval_func

    def choose_move(self, state):
        self.player = state.current_player

        def minimax(state, depth, alpha, beta, maximizing):
            if depth == 0 or state.is_terminal():
                return self.eval_func(state, self.player), None

            moves = state.legal_moves(state.current_player)
            self.rng.shuffle(moves)
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
    

def weighted_greedy(state, player):
    """
    Heuristic: difference in legal moves with weights applied
    """
    # If game is over and we won, give massive weight
    if state.is_terminal():
        if state.winner() == player:
            return math.inf
        else:
            return -math.inf
    opp = state.opponent(player)
    val = len(13*state.legal_moves(player)) - 19*len(state.legal_moves(opp))

    return val



class WeightedMM(Bot_Base_Class):
    def __init__(self, depth=3, eval_func=weighted_greedy, seed=None):
        super().__init__(seed)
        self.depth = depth
        self.eval_func = eval_func


    def choose_move(self, state):
        self.player = state.current_player

        if state.turn in range(0,2):
            self.depth = 4
        elif state.turn in range(2,6):
            self.depth = 4
        elif state.turn in range(6,8):
            self.depth = 5
        elif state.turn > 7:
            self.depth = 9


        def minimax(state, depth, alpha, beta, maximizing):
            if depth == 0 or state.is_terminal():
                return self.eval_func(state, self.player), None

            moves = state.legal_moves(state.current_player)
            self.rng.shuffle(moves)
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
    
