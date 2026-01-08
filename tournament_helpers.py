from game_engine import IsolationState, PLAYER_WHITE, PLAYER_BLACK
from bots.example_bots import RandomBot, GreedyBot, MinimaxBot

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
    matchup = {
        "A_white": {"A_wins": 0, "B_wins": 0, "draws": 0},
        "B_white": {"A_wins": 0, "B_wins": 0, "draws": 0}
    }

    for i in range(n_games):
        botA.reset_rng()
        botB.reset_rng()

        # Alternate starting player
        if i % 2 == 0:
            white_bot, black_bot = botA, botB
            key = "A_white"
        else:
            white_bot, black_bot = botB, botA
            key = "B_white"

        winner = play_game(white_bot, black_bot)  # returns PLAYER_WHITE, PLAYER_BLACK, or None

        if winner == PLAYER_WHITE:
            if white_bot is botA:
                matchup[key]["A_wins"] += 1
            else:
                matchup[key]["B_wins"] += 1
        elif winner == PLAYER_BLACK:
            if black_bot is botA:
                matchup[key]["A_wins"] += 1
            else:
                matchup[key]["B_wins"] += 1
        else:
            matchup[key]["draws"] += 1

    # Print results
    print(f"\nTournament Results ({n_games} games total):")
    print("-" * 60)
    for key, data in matchup.items():
        total_games = data["A_wins"] + data["B_wins"] + data["draws"]
        A_pct = data["A_wins"] / total_games * 100
        B_pct = data["B_wins"] / total_games * 100
        draw_pct = data["draws"] / total_games * 100
        matchup_name = "BotA White / BotB Black" if key == "A_white" else "BotB White / BotA Black"
        print(f"{matchup_name}:")
        print(f"  BotA wins: {data['A_wins']} ({A_pct:.1f}%)")
        print(f"  BotB wins: {data['B_wins']} ({B_pct:.1f}%)")
        print(f"  Draws: {data['draws']} ({draw_pct:.1f}%)\n")
    print("-" * 60)

    return matchup