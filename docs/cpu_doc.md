# 🧠 CPU Player Strategies Documentation

This document outlines the different CPU opponents implemented for the poker engine, explaining their internal logic, strategic basis, and the framework they operate within using the PyPokerEngine architecture.

---

## 🧹 Architecture: `BasePokerPlayer` Interface

Each CPU player inherits from `BasePokerPlayer` and must implement the following key methods:

- `declare_action(valid_actions, hole_card, round_state)`
- `receive_game_start_message(game_info)`
- `receive_round_start_message(round_count, hole_card, seats)`
- `receive_street_start_message(street, round_state)`
- `receive_game_update_message(new_action, round_state)`
- `receive_round_result_message(winners, hand_info, round_state)`

These methods provide the hooks necessary for the CPU to interact with the game engine and make decisions during each phase of the game.

---

## 🧠 Implemented CPU Types

### 1. `baselineCPU`

**Goal**: Skeleton implementation with placeholder methods.

- Does **not** currently contain any decision-making logic.
- Serves as a starting point or scaffolding for new strategies.
- Can be extended or copied to begin building smarter opponents.

---

### 2. `equityCPU`

**Strategy**: Uses a simplified equity estimation based on "outs" to determine how strong its hand is.

**Core Concepts:**

- Outs: Number of cards that improve the hand significantly.
- Equity Estimate: `equity = outs * 4`, capped at 100%.

**Decision Thresholds:**

- If `equity` > 50% → Raise
- If 25% < `equity` ≤ 50% → Call
- If `equity` ≤ 25% → Fold

**Highlights:**

- Implements flush draw, straight draw, and overcard detection heuristics.
- Assumes maximum 9 outs for flush and up to 8 for straight draws.
- Great starting point for basic probabilistic play.

---

### 3. `expectedValueCPU`

**Strategy**: Makes decisions based on Expected Value (EV).

**Core Formula:**

```python

EV = (equity * pot_size) - ((1 - equity) * amount_to_call)

```

**Decision Logic:**

- If `EV` > 0 → Raise or Call
- Else → Fold

**Highlights:**

- Equity is computed the same way as in `equityCPU`.
- This CPU integrates pot size and call amount to assess profitability.
- Demonstrates a step toward `GTO (Game Theory Optimal)` behavior.

---

### 4. `potOddsCPU`

**Strategy**: Makes decisions based on Pot Odds vs Equity.

**Core Formula:**

```python

pot_odds = amount_to_call / (pot_size + amount_to_call)

```

**Decision Logic:**

- If `equity` ≥ `pot_odds` → Call or Raise
- Else → Fold

**Highlights:**

- Combines calculated pot odds with estimated equity.
- Models real-world betting decisions based on expected returns.

---

## 🎓 Design Philosophy

- These CPUs are intentionally designed to showcase progressively deeper poker logic.
- Use the `emulator` module from PyPokerEngine to simulate thousands of hands for training smarter strategies.
- Future enhancements may include:
  - Bluff detection
  - Opponent modeling
  - Reinforcement Learning (RL) or Deep Q-Learning agents

---

## 🔧 Useful Heuristics Implemented

| Concept        | Description                                                             |
| -------------- | ----------------------------------------------------------------------- |
| Equity         | % chance to win/improve hand using outs                                 |
| Expected Value | Weighs possible gain vs loss based on probabilities and bet size        |
| Pot Odds       | Determines whether a call is justified based on bet vs pot ratio        |
| Implied Odds   | Takes future rounds into account; can be used for deeper strategic play |

---

## 📌 Recommendations for Further Development

- Convert current `count_outs()` logic into a shared utility module.
- Use the PyPokerEngine emulator to simulate full games and collect training data.
- Use a decision tree, rule engine, or ML model for more nuanced behavior.
