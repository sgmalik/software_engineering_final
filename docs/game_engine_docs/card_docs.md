# `Card` Class Documentation

## Overview

The `Card` class models a standard playing card with a suit and value. It includes operator overloading to support comparison operations, which are particularly useful in modules like `game_evaluator` and `hand_evaluator`. Each card is associated with a numerical rank based on traditional poker values (`2`–`A`).

---

## Instance Variables

### `suit`

- **Type**: `str`
- **Description**: A single-character string representing the card’s suit (e.g., `'H'` for hearts, `'D'` for diamonds).
- **Example**:

```python

card.suit  # 'H'

```

---

### `card_val`

- **Type**: `str`
- **Description**: A string representing the face value of the card (`'2'`–`'10'`, `'J'`, `'Q'`, `'K'`, `'A'`).
- **Example**:

```python

card.card_val  # 'A'

```

---

## Class Constants

### `CARD_RANK_MAP`

- **Type**: `Dict[str, int]`
- **Description**: A mapping from card face values to numerical ranks, used for evaluating card strength.
- **Example**:

```python

Card.CARD_RANK_MAP['Q']  # 12

```

---

## Methods

### `__init__(suit: str, card_val: str)`

- **Use Case**: Creates a card given its suit and value.
- **Example**:

```python

card = Card('H', 'A')  # Ace of Hearts

```

---

### Operator Overloads

#### `__eq__(other_card)`

- **Use Case**: Checks if two cards are equal by comparing both suit and value.
- **Example**:

```python

Card('H', 'A') == Card('H', 'A')  # True

```

#### `__lt__`, `__gt__`, `__ge__`, `__le__`

- **Use Case**: Intended to compare card ranks for sorting or evaluating hand strength.
- **Note**: These are currently unimplemented and should be defined using `get_card_rank()`.

---

### `__str__()` / `__repr__()`

- **Use Case**: Returns a readable string representation of the card.
- **Example**:

```python

str(Card('S', 'Q'))  # 'Q of S'
repr(Card('D', '10'))  # '10 of D'

```

---

### `get_card_rank() -> int`

- **Use Case**: Returns the numeric rank of the card using `CARD_RANK_MAP`.
- **Raises**: `AssertionError` if `card_val` is not in the map.
- **Example**:

```python

card = Card('C', 'K')
card.get_card_rank()  # 13

```

---

## TODO

- Implement comparison operators: `__lt__`, `__gt__`, `__ge__`, `__le__`
