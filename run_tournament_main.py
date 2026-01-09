import time

from automation_helpers import run_tournament, print_tournament_results
from bots.example_bots import RandomBot, GreedyBot, MinimaxBot


if __name__ == "__main__":
    # Create your bots here (may need to import new ones)
    bot_a = RandomBot()
    bot_b = RandomBot()

    # bot_a = MinimaxBox(depth=1)
    # bot_b = MinimaxBox(depth=3)

    # How many games they should play (each plays white half this amount)
    num_games = 1000

    start_time = time.perf_counter()
    results = run_tournament(bot_a, bot_b, num_games)
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"\nTournament completed in {elapsed:.2f} seconds, or {elapsed / num_games:.3f} seconds per game")

    print_tournament_results(results)