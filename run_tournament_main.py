import time

from tournament_helpers import run_tournament
from bots.example_bots import RandomBot, GreedyBot, MinimaxBot

if __name__ == "__main__":
    # Create your bots here (may need to import new ones)
    bot_a = MinimaxBot(depth=2)
    bot_b = MinimaxBot(depth=4)

    # How many games they should play (each plays white half this amount)
    num_games = 100

    start_time = time.time()
    run_tournament(bot_a, bot_b, num_games)
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\nTournament completed in {elapsed:.2f} seconds, or {elapsed / num_games:.2f} seconds per game")