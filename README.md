# Isolation Game AI

Welcome to the **Isolation Game AI** repository! This project lets you play and experiment with AI bots in a simple two-player board game called *Isolation*. You can create your own bots, test them against built-in bots, and run tournaments to see which strategies perform best.

---

## Table of Contents
1. [About the Game](#about-the-game)  
2. [Folder Structure](#folder-structure)  
3. [Getting Started](#getting-started)  
4. [How to Play](#how-to-play)  
5. [Creating Your Own Bot](#creating-your-own-bot)  
6. [Running Simulations](#running-simulations)  
7. [Tips and Tricks](#tips-and-tricks)  

---

## About the Game

**Isolation** is a two-player strategy game:

- Played on a square board (default 7×7).  
- Each player starts with one piece.  
- On your turn, move your piece like a queen in chess (any number of squares in any direction).  
- After moving, the square you left becomes **blocked**.  
- Goal: trap your opponent so they cannot move.  
- Game ends when a player has no legal moves. Rules may allow for draws if both are trapped.

---

## Folder Structure

```

bots/
├── bot_base.py       # Base class for all bots
└── example_bots.py   # Example bots: GreedyBot, RandomBot, MinimaxBot

game_engine.py        # Core game logic
gui.py                # GUI for manual or bot play
run_gui_main.py       # Launch GUI
tournament_helpers.py # Functions for running tournaments

````

---

## Getting Started

### Requirements
- Python 3.8 or higher
- Tkinter (for GUI)
- Optional: `numpy` for more advanced bots

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/isolation-ai.git
cd isolation-ai
````

2. Run the GUI to play manually or watch bots:

```bash
python run_gui_main.py
```

---

## How to Play

### GUI Mode

* Click on a highlighted square to move your piece.
* Bots automatically move on their turn if assigned.
* GUI shows current player, blocked squares, and game outcome.

### Simulation Mode

* Run tournaments between bots in the console:

```python
from bots.example_bots import GreedyBot, MinimaxBot
from tournament_helpers import run_tournament

bot_a = MinimaxBot(depth=2, seed=42)
bot_b = GreedyBot(seed=42)

run_tournament(bot_a, bot_b, n_games=100)
```

---

## Creating Your Own Bot

1. **Create a Python class** in `bots/` that inherits from `Bot_Base_Class`:

```python
from bots.bot_base import Bot_Base_Class
from game_engine import IsolationState

class MyBot(Bot_Base_Class):
    def choose_move(self, state: IsolationState):
        moves = state.legal_moves()
        if moves:
            return moves[0]  # always pick the first legal move
        return None
```

2. **Use your bot** in GUI or simulations:

```python
from bots.example_bots import RandomBot
from tournament_helpers import run_tournament

my_bot = MyBot(seed=42)
run_tournament(my_bot, RandomBot(), n_games=50)
```

**Tips:**

* Use `state.legal_moves()` to see available moves.
* Simulate moves with `state.apply_move(move)` to check the resulting board.
* Add heuristics: “maximize my moves, minimize opponent moves.”
* Use the `seed` parameter for deterministic tie-breaking.

---

## Running Simulations

`run_tournament(botA, botB, n_games=...)` pits two bots against each other multiple times.
Output includes:

* Wins for each bot as White
* Wins for each bot as Black
* Overall draw percentage

Example:

```python
from bots.example_bots import GreedyBot, MinimaxBot
from tournament_helpers import run_tournament

bot_a = GreedyBot(seed=42)
bot_b = MinimaxBot(depth=3, seed=42)

run_tournament(bot_a, bot_b, n_games=200)
```

---

## Tips and Tricks

* **Start simple:** Try `GreedyBot` before `MinimaxBot`.
* **Visual debugging:** Use the GUI to watch bots and understand their moves.
* **Experiment:** Change board size, bot depth, or evaluation functions.
* **Reproducibility:** Use the `seed` parameter for deterministic behavior.

---