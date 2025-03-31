# `Player` Class Documentation

## Overview

The `Player` class models an individual poker player within a poker engine. It manages the player's stack, hole cards, state (e.g., active, folded, all-in), and their action history during a hand. This class is designed to interface with a broader poker simulation framework and supports core operations such as betting, tracking contributions, and maintaining per-street action histories.

---

## Instance Variables

### `hole_cards`

- **Type**: `List[Card]`
- **Description**: The two private cards dealt to the player.
- **Example**:

  ```python
  player.hole_cards  # [Card('H', 'A'), Card('D', 'K')]
  ```

### `stack`

- **Type**: `int`
- **Description**: The amount of chips the player currently has available.
- **Example**:

  ```python
  player.stack  # 1500
  ```

### `state`

- **Type**: `PlayerState`
- **Description**: The current game state of the player (e.g., ACTIVE, FOLDED, ALLIN).
- **Example**:

  ```python
  player.state == PlayerState.ACTIVE
  ```

### `round_action_histories`

- **Type**: `Callable[[], List[Optional[List[dict]]]]`
- **Description**: Stores action histories for each street (`preflop`, `flop`, `turn`, `river`). Initially a lambda that returns 4 `None` values.
- **Example**:

  ```python
  player.round_action_histories()  # [None, None, None, None]
  ```

### `contribuition`

- **Type**: `int`
- **Description**: The total chips contributed by the player to the pot in the current hand.
- **Example**:

  ```python
  player.contribuition  # 200
  ```

### `action_histories`

- **Type**: `List[dict]`
- **Description**: A list of actions the player has taken during the current round.
- **Example**:

  ```python
  player.action_histories  # [{'action': Action.CALL, 'amount': 100, 'paid': 100}]
  ```

---

## Methods

### `__init__(initial_stack: int)`

- **Use Case**: Instantiates a player with a starting chip stack.
- **Example**:

  ```python
  player = Player(initial_stack=1000)
  ```

---

### `add_hole_card(cards: List[Card])`

- **Use Case**: Sets the player’s hole cards. Raises an error if already set or invalid input.
- **Example**:

  ```python
  player.add_hole_card([Card('H', 'A'), Card('S', 'K')])
  ```

---

### `clear_hole_cards()`

- **Use Case**: Empties the player's hole cards after a round ends.
- **Example**:

  ```python
  player.clear_hole_cards()
  ```

---

### `add_to_stack(amount: float | int)`

- **Use Case**: Increases the player's chip stack (e.g., after winning a pot).
- **Example**:

  ```python
  player.add_to_stack(500)
  ```

---

### `collect_bet(amount: float | int)`

- **Use Case**: Deducts a bet from the player’s stack. Raises an error if the player can't afford it.
- **Example**:

  ```python
  player.collect_bet(200)
  ```

---

### State Check Methods

Each returns a `bool` indicating the player's current state:

- `is_active()`
- `is_folded()`
- `is_allin()`
- `is_waiting()`
- `is_winner()`

**Example**:

```python
if player.is_folded():
    print("This player has folded.")
```

---

### `add_action_history(action: Action, chip_amount=0, add_amount=0, sb_amount=0, bb_amount=0)`

- **Use Case**: Records an action the player has taken, with appropriate metadata based on the action type.
- **Example**:

  ```python
  player.add_action_history(Action.CALL, chip_amount=100)
  player.add_action_history(Action.RAISE, chip_amount=300, add_amount=200)
  ```

---

### `save_round_action_histories(street: Street)`

- **Use Case**: Saves the current `action_histories` list into the appropriate index for the street.
- **Example**:

  ```python
  player.save_round_action_histories(Street.FLOP)
  ```

---

### `clear_action_histories()`

- **Use Case**: Clears both current and round-based action histories.
- **Example**:

  ```python
  player.clear_action_histories()
  ```

---

### `bet(amount)`

- **Use Case**: Deducts a bet from the player’s stack and updates total contribution.
- **Example**:

  ```python
  player.bet(150)
  ```

---

## TODO

- create test cases for the functions
