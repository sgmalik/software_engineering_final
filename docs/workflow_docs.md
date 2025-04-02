# 🧩 Project Workflow & Architecture Overview

This document provides a high-level understanding of the poker engine project, describing how the various modules interact across the **game logic**, **CPU AI**, **hand evaluation**, and **GUI** layers.

---

## 📂 Project Structure

```yaml

src/
├── game_engine/                    # Core poker game logic
│   ├── card.py                    # Card class and operations
│   ├── deck.py                    # Deck management and shuffling
│   ├── player.py                  # Player state and actions
│   ├── constants.py               # Game-wide constants
│   ├── pot.py                     # Pot management
│   ├── table.py                   # Game table state
│   ├── betting_manager.py         # Betting round logic
│   ├── dealer.py                  # Game flow control
│   ├── engine.py                  # Main game engine
│   ├── hand_evaluator.py          # Hand strength evaluation
│   ├── game_evaluator.py          # Game outcome determination
│   └── cpu/                       # CPU opponent implementations
│       ├── baselineCPU.py         # Basic CPU strategy
│       ├── equityCPU.py           # Equity-based decisions
│       ├── expectedValueCPU.py    # EV calculations
│       └── potOddsCPU.py         # Pot odds strategy
├── gui/                           # GUI rendering components
│   ├── button.py                  # Interactive buttons
│   ├── chip.py                    # Chip visualization
│   ├── gui_card.py                # Card rendering
│   ├── numtext.py                 # Numeric displays
│   ├── slider.py                  # Sliding controls
│   └── util.py                    # GUI utilities
└── main.py                        # Entry point for the application

```

---

## 🔁 High-Level Workflow

### 1. 🖥 `main.py` (Pygame Loop)
- Initializes Pygame, sets up display and global UI lists.
- Starts on the **Home screen** via `change_to_main_menu()`.
- Reacts to input events (e.g. clicks, keys) and routes those to GUI components.
- Delegates game control to the `Engine` object when the game is running.

---

### 2. 🧠 `Engine` Class (Controller Layer)
- Acts as the **interface between GUI and game logic**.
- Exposes clean methods for:
  - `start_game()`
  - `player_action()`
  - `cpu_action()`
  - `start_next_street()` / `start_next_round()`
  - `current_state_of_game()` → Returns structured game state to GUI.
- Internally delegates to:
  - `Dealer` (for betting/street control)
  - `GameEvaluator` (to determine winners)
  - `HandEvaluator` (to calculate hand strength)

---

### 3. 🃏 `Dealer` Class
- Controls game progression across **streets** (`PREFLOP`, `FLOP`, `TURN`, `RIVER`).
- Uses `BettingManager` to track pending betters and apply actions.
- Interfaces directly with the `Table` to manipulate players, deck, and pot.
- Exposes `is_round_over()` to know when to end a round.

---

### 4. 💸 `BettingManager`
- Updates table state when a player performs an action (`CALL`, `RAISE`, `FOLD`, etc).
- Manages:
  - `current_bet` tracking
  - `pending_betters` list (players who need to respond to bets)
  - Handles betting logic (calls, raises, folds)
- Called exclusively by `Dealer`.

---

### 5. 🪑 `Table` Class
- Holds the shared game state: `players`, `deck`, `pot`, `community_cards`.
- Can:
  - Deal hole cards and community cards.
  - Advance player turns via `next_player()`.
  - Return list of `active_players()`.
- Is passed around to all modules (dealer, evaluator, engine) for state management.

---

## ♠️ Core Components

### `Player`
- Represents a single player.
- Tracks:
  - `stack`
  - `hole_cards`
  - `action_histories`
  - `state` (e.g. FOLDED, ACTIVE)
- Supports betting, stack updates, state checks, and action recording.

### `Deck`
- Manages a list of 52 `Card` objects.
- Supports drawing, shuffling, restoring, and sorting cards by rank.

### `Pot`
- Tracks the total chips in the main pot (side pots unimplemented).

---

## 🧠 CPU AI Layer

### `cpu/` folder
- Contains several CPU player implementations that inherit from `BasePokerPlayer`.
- Each implements:
  - `declare_action()` → returns an action based on strategy
  - Other PyPokerEngine lifecycle hooks

**CPU Strategies**:
- `baselineCPU`: No-op placeholder
- `equityCPU`: Makes decisions using estimated equity from draw-based "outs"
- `expectedValueCPU`: Evaluates expected profitability (EV) of each move
- `potOddsCPU`: Compares pot odds to estimated equity

> These can be swapped into the game dynamically by assigning them to CPU seats during player initialization.

---

## 🧠 Evaluation Layer

### `HandEvaluator`
- Static class for computing a hand's rank and kickers.
- Returns a dictionary like:
  `{ "strength": { "hand_rank": 3, "primary_cards_rank": [5,3] }, "kickers": [7] }`

### `GameEvaluator`
- Uses `HandEvaluator` to determine the winner(s).
- Intended to support side pots and multiple player resolution.
- Will eventually redistribute the pot using `add_money_to_winners()`.

---

## 🖼 GUI Layer

### GUI Classes (`gui/`)
- **Button, Slider, Chip, GUI_Card, NumText**: modular GUI components
- `util.py`:
  - Manages screen state transitions: `HOME`, `SETTINGS`, `GAME`
  - Builds buttons, chips, and text displays based on game state
  - Synchronizes user interaction with game state (e.g. bet amounts)

---

## 🔄 Data Flow

```text
[Pygame GUI] 
    ↕ user input → buttons/sliders
    ↕ draw updates ← engine state

[Engine] 
    ↕ controls Dealer & GameEvaluator
    ↕ produces displayable game state
    ↕ wraps player and CPU actions

[Dealer]
    ↕ manages streets, players, betting via BettingManager

[Table]
    ↕ stores all shared state (players, pot, deck)

[Evaluator Layer]
    ↕ used by Engine → returns winners, hand strengths
```
