# `BettingManager` Class Documentation

## Overview

The `BettingManager` class is responsible for managing the betting phase of each street in a poker game. It tracks which players still need to act (`pending_betters`), manages bet sizes, applies player actions (call, raise, fold, blinds), and updates the pot and player states accordingly. This class acts as the operational core of turn-based betting logic in the engine.

---

## Instance Variables

### `table`

- **Type**: `Table`
- **Description**: A reference to the current game table to access players, pot, and player states.
- **Example**: 
```python
# Check the current pot value through the table reference
manager = BettingManager(table, blind=50)
print(manager.table.pot.value)  # 300
```

---

### `current_bet`

- **Type**: `int`
- **Description**: The current amount players must call to stay in the hand.
- **Example**: 
```python
# Check the current bet amount
manager = BettingManager(table, blind=50)
manager._raise_bet(100)
print(manager.current_bet)  # 100
```

---

### `blind`

- **Type**: `int`
- **Description**: The small blind amount; big blind is always `2 * blind`.
- **Example**: 
```python
# Check blind amounts
manager = BettingManager(table, blind=50)
print(f"Small blind: {manager.blind}")     # Small blind: 50
print(f"Big blind: {manager.blind * 2}")   # Big blind: 100
```

---

### `pending_betters`

- **Type**: `List[Player]`
- **Description**: Players who have not yet acted in the current betting round.
- **Example**: 
```python
# Check number of players still to act
manager = BettingManager(table, blind=50)
manager.reset_betting_round()
print(len(manager.pending_betters))  # 2
```

---

## Methods

### `__init__(table, blind)`

- **Use Case**: Initializes the betting manager with a reference to the game table and blind size.
- **Example**: 
```python
# Create a new betting manager
table = Table()
manager = BettingManager(table, blind=50)
print(manager.blind)  # 50
```

---

### `reset_betting_round()`

- **Use Case**: Resets `current_bet` to 0, repopulates `pending_betters`, and resets player contributions for a new street.
- **Example**: 
```python
# Reset for a new betting round
manager = BettingManager(table, blind=50)
manager.current_bet = 100
manager.reset_betting_round()
print(manager.current_bet)  # 0
```

---

### `apply_player_action(current_player, action, raise_amount=None)`

- **Use Case**: Applies the given action (`CALL`, `RAISE`, `FOLD`, `SMALL_BLIND`, `BIG_BLIND`) to the current player.
- **Example**: 
```python
# Apply a call action
player = table.current_player
manager = BettingManager(table, blind=50)
manager.current_bet = 100
manager.apply_player_action(player, Action.CALL)
print(player.contribution)  # 100
```

---

### `_blind(current_player, blind)`

- **Use Case**: Handles blind posting and updates pot.
- **Example**: 
```python
# Post small blind
player = table.current_player
manager = BettingManager(table, blind=50)
manager._blind(player, 50)
print(player.contribution)  # 50
print(manager.table.pot.value)  # 50
```

---

### `_fold(current_player)`

- **Use Case**: Folds the player and removes them from `pending_betters`.
- **Example**: 
```python
# Fold a player
player = table.current_player
manager = BettingManager(table, blind=50)
manager._fold(player)
print(player.state)  # PlayerState.FOLDED
print(player in manager.pending_betters)  # False
```

---

### `_raise(current_player, raise_amount)`

- **Use Case**: Forces player to first call the current bet, then raise it. Pot is updated and other players become pending again.
- **Example**: 
```python
# Raise the current bet
player = table.current_player
manager = BettingManager(table, blind=50)
manager.current_bet = 100
manager._raise(player, 200)
print(manager.current_bet)  # 300
print(player.contribution)  # 300
```

---

### `_call(current_player)`

- **Use Case**: Pays the difference between `current_bet` and the player's current contribution, then removes player from `pending_betters`.
- **Example**: 
```python
# Call the current bet
player = table.current_player
manager = BettingManager(table, blind=50)
manager.current_bet = 100
manager._call(player)
print(player.contribution)  # 100
print(player in manager.pending_betters)  # False
```

---

### `is_betting_over() -> bool`

- **Use Case**: Returns `True` if there are no pending betters or only one active player remains.
- **Example**: 
```python
# Check if betting round is complete
manager = BettingManager(table, blind=50)
manager.reset_betting_round()
for player in manager.pending_betters:
    manager._fold(player)
print(manager.is_betting_over())  # True
```

---

### `_remove_better(current_player)`

- **Use Case**: Removes the given player from `pending_betters`.
- **Example**: 
```python
# Remove a player from pending betters
player = table.current_player
manager = BettingManager(table, blind=50)
manager.reset_betting_round()
manager._remove_better(player)
print(player in manager.pending_betters)  # False
```

---

### `_add_betters(current_player)`

- **Use Case**: Adds all other active players to `pending_betters` when a player raises.
- **Example**: 
```python
# Add players back to pending betters after a raise
player = table.current_player
manager = BettingManager(table, blind=50)
manager.pending_betters = []
manager._add_betters(player)
print(len(manager.pending_betters))  # Number of active players - 1
```

---

### `_raise_bet(amount)`

- **Use Case**: Increments the `current_bet` value by the raise amount.
- **Example**: 
```python
# Raise the current bet
manager = BettingManager(table, blind=50)
manager.current_bet = 100
manager._raise_bet(150)
print(manager.current_bet)  # 250
```

---
