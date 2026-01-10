from game_engine import IsolationState, PLAYER_WHITE, PLAYER_BLACK
from bots.example_bots import RandomBot, GreedyBot, MinimaxBot

import multiprocessing as mp

def play_game(botWhite, botBlack):
    state = IsolationState.initial_state()
    bots = {PLAYER_WHITE: botWhite, PLAYER_BLACK: botBlack}

    while not state.is_terminal():
        player = state.current_player
        bot = bots[player]
        move = bot.choose_move(state)
        if move is None:
            break
        state = state.apply_move(move)

    winner = state.winner()
    return winner

def run_tournament(botA, botB, n_games=1000):
    # Track results separately for the two matchups
    results = {
        "BotA_white": 0,  # BotA wins as White
        "BotA_black": 0,  # BotA wins as Black
        "BotB_white": 0,
        "BotB_black": 0
    }

    for i in range(n_games):
        botA.reset_rng()
        botB.reset_rng()

        if i % 2 == 0:
            white_bot, black_bot = botA, botB
        else:
            white_bot, black_bot = botB, botA

        winner = play_game(white_bot, black_bot)

        if winner == PLAYER_WHITE:
            if white_bot is botA:
                results["BotA_white"] += 1
            else:
                results["BotB_white"] += 1
        elif winner == PLAYER_BLACK:
            if black_bot is botA:
                results["BotA_black"] += 1
            else:
                results["BotB_black"] += 1
    return results

def play_single_game(args):
    # Unpack the 5-tuple here (cleaner and more robust)
    game_index, botA_cls, botA_kwargs, botB_cls, botB_kwargs = args
    
    # Create fresh instances with the correct parameters
    botA = botA_cls(**botA_kwargs)
    botB = botB_cls(**botB_kwargs)
    
    botA.reset_rng()
    botB.reset_rng()

    if game_index % 2 == 0:
        white_bot, black_bot = botA, botB
        white_key = "BotA_white"
        black_key = "BotB_black"
    else:
        white_bot, black_bot = botB, botA
        white_key = "BotB_white"
        black_key = "BotA_black"

    winner = play_game(white_bot, black_bot)

    if winner == PLAYER_WHITE:
        return white_key, 1
    elif winner == PLAYER_BLACK:
        return black_key, 1
    else:
        return None, 0

def run_tournament_parallel(botA_cls, botA_kwargs, botB_cls, botB_kwargs,
                            n_games=1000, processes=None):
    if processes is None:
        processes = max(1, mp.cpu_count() - 1)

    # Prepare tasks: each task carries the kwargs for that bot
    tasks = [
        (i, botA_cls, botA_kwargs, botB_cls, botB_kwargs)
        for i in range(n_games)
    ]

    results = {
        "BotA_white": 0, "BotA_black": 0,
        "BotB_white": 0, "BotB_black": 0
    }

    with mp.Pool(processes=processes) as pool:
        for key, score in pool.imap_unordered(play_single_game, tasks):
            if key is not None:
                results[key] += score

    return results

def print_tournament_results(results):
    # BotA
    botA_white_wins = results["BotA_white"]
    botA_black_wins = results["BotA_black"]
    botA_total_wins = botA_white_wins + botA_black_wins

    # BotB
    botB_white_wins = results["BotB_white"]
    botB_black_wins = results["BotB_black"]
    botB_total_wins = botB_white_wins + botB_black_wins

    # Total wins by color
    total_white_wins = botA_white_wins + botB_white_wins
    total_black_wins = botA_black_wins + botB_black_wins

    n_games = total_white_wins + total_black_wins
    games_per_color = n_games // 2

    print("\nTournament Summary")
    print("-" * 50)
    print(f"BotA wins as White: {botA_white_wins} ({botA_white_wins / games_per_color * 100:.1f}%)")
    print(f"BotA wins as Black: {botA_black_wins} ({botA_black_wins / games_per_color * 100:.1f}%)")
    print(f"BotA overall wins: {botA_total_wins} ({botA_total_wins / n_games * 100:.1f}%)\n")

    print(f"BotB wins as White: {botB_white_wins} ({botB_white_wins / games_per_color * 100:.1f}%)")
    print(f"BotB wins as Black: {botB_black_wins} ({botB_black_wins / games_per_color * 100:.1f}%)")
    print(f"BotB overall wins: {botB_total_wins} ({botB_total_wins / n_games * 100:.1f}%)\n")

    print(f"Total White wins: {total_white_wins} ({total_white_wins / n_games * 100:.1f}%)")
    print(f"Total Black wins: {total_black_wins} ({total_black_wins / n_games * 100:.1f}%)")
    print("-" * 50)