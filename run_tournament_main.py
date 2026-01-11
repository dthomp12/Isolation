import time
from functools import partial
import multiprocessing as mp

from automation_helpers import run_tournament, print_tournament_results, run_tournament_parallel
from bots.example_bots import RandomBot, GreedyBot, MinimaxBot
from bots.Bryant_bots import BlindGreedy, DiagonalBot, CornerBot, EdgeBot, AgroGreedy, WeightedMM


if __name__ == "__main__":
    # Create your bots here (may need to import new ones)
    # bot_a = GreedyBot()
    # bot_b = BlindGreedy()

    # How many games they should play (each plays white half this amount)
    num_games = 500

    print(f"Starting parallel tournament: {num_games} games")
    print(f"Bot A = GreedyBot")
    print(f"Bot B = BlindGreedy")
    print(f"Using up to {mp.cpu_count()-1} processes\n")

    # Run in parallel
    start_time = time.perf_counter()
    results = run_tournament_parallel(
        botA_cls=MinimaxBot,
        botA_kwargs={},
        botB_cls=WeightedMM,
        botB_kwargs={},
        n_games=num_games,
        processes=10
    )
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print(f"\nTournament completed in {elapsed:.2f} seconds, or {elapsed / num_games:.3f} seconds per game")

    print_tournament_results(results)