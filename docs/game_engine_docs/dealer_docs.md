# `Dealer` Class Documentation

## Overview

The `Dealer` class manages game progression through the different poker streets (`PREFLOP`, `FLOP`, `TURN`, `RIVER`). It controls round setup, card dealing, blind posting, and betting state transitions. It serves as the orchestrator between `Table`, `BettingManager`, and game flow logic in `engine.py`.

---

## Instance Variables

### `current_street`

- **Type**: `Street`
- **Description**: Tracks the current phase of the hand.
- **Example**: 
```python
# Check the current street
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer.next_street()
print(dealer.current_street == Street.FLOP)  # True
```

---

### `blind`

- **Type**: `int`
- **Description**: The small blind value for the current hand.
- **Example**: 
```python
# Check blind value
dealer = Dealer(initial_stack=1000, small_blind=50)
print(dealer.blind)  # 50
print(dealer.blind * 2)  # 100 (big blind)
```

---

### `initial_stack`

- **Type**: `int`
- **Description**: The chip stack each player starts with.
- **Example**: 
```python
# Check initial stack size
dealer = Dealer(initial_stack=1000, small_blind=50)
print(dealer.initial_stack)  # 1000
print(dealer.table.players[0].stack)  # 1000
```

---

### `table`

- **Type**: `Table`
- **Description**: Manages the players, pot, and community cards.
- **Example**: 
```python
# Check table state
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer._start_preflop()
print(dealer.table.pot.value)  # 300
print(len(dealer.table.players))  # 2
```

---

### `betting_manager`

- **Type**: `BettingManager`
- **Description**: Handles all betting logic and state transitions for player actions.
- **Example**: 
```python
# Check betting manager state
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer._start_preflop()
print(dealer.betting_manager.current_bet)  # 200
print(len(dealer.betting_manager.pending_betters))  # 2
```

---

## Methods

### `__init__(initial_stack, small_blind)`

- **Use Case**: Sets up the table, betting manager, blind, and current street.
- **Example**: 
```python
# Initialize a new dealer
dealer = Dealer(initial_stack=1000, small_blind=50)
print(dealer.initial_stack)  # 1000
print(dealer.blind)  # 50
print(dealer.current_street)  # Street.PREFLOP
```

---

### `next_street()`

- **Use Case**: Advances the game to the next street (e.g., `PREFLOP → FLOP`, etc.).
- **Example**: 
```python
# Advance to next street
dealer = Dealer(initial_stack=1000, small_blind=50)
initial_street = dealer.current_street
dealer.next_street()
print(f"{initial_street} -> {dealer.current_street}")  # PREFLOP -> FLOP
```

---

### `start_street()`

- **Use Case**: Begins a new street by resetting betting and dealing any required community cards.
- **Example**: 
```python
# Start a new street
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer.next_street()  # Move to FLOP
dealer.start_street()
print(len(dealer.table.community_cards))  # 3
```

---

### `_start_preflop()`

- **Use Case**: Deals hole cards to players and posts blinds to begin the hand.
- **Example**: 
```python
# Start preflop round
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer._start_preflop()
print(len(dealer.table.players[0].hole_cards))  # 2
print(dealer.table.pot.value)  # 75 (small blind + big blind)
```

---

### `_start_flop()`

- **Use Case**: Deals 3 community cards.
- **Example**: 
```python
# Deal the flop
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer._start_flop()
print(len(dealer.table.community_cards))  # 3
```

---

### `_start_turn()`

- **Use Case**: Deals 1 community card.
- **Example**: 
```python
# Deal the turn
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer._start_flop()
dealer._start_turn()
print(len(dealer.table.community_cards))  # 4
```

---

### `_start_river()`

- **Use Case**: Deals 1 community card.
- **Example**: 
```python
# Deal the river
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer._start_flop()
dealer._start_turn()
dealer._start_river()
print(len(dealer.table.community_cards))  # 5
```

---

### `is_round_over() -> bool`

- **Use Case**: Determines if the round is over (either everyone has acted on the river or all but one player has folded).
- **Example**: 
```python
# Check if round is over
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer._start_preflop()
dealer.apply_action(Action.FOLD)  # One player folds
print(dealer.is_round_over())  # True
```

---

### `apply_action(action: Action, raise_amount: Optional[int] = None)`

- **Use Case**: Wrapper to apply a player action through the `BettingManager`.
- **Example**: 
```python
# Apply a raise action
dealer = Dealer(initial_stack=1000, small_blind=50)
dealer._start_preflop()
initial_pot = dealer.table.pot.value
dealer.apply_action(Action.RAISE, raise_amount=200)
print(f"Pot: {initial_pot} -> {dealer.table.pot.value}")  # Shows pot increase
```

---
