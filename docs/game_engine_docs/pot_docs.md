# `Pot` Class Documentation

## Overview

The `Pot` class represents the central pot in a hand of poker. It is responsible for tracking the total amount of chips contributed by players. This is a minimal utility class used by the game engine to manage betting rounds and determine payouts.

---

## Instance Variables

### `value`

- **Type**: `int`
- **Description**: The current total number of chips in the pot.
- **Example**: 
```python
# Create a pot and check its value
pot = Pot()
pot.add_to_pot(150)
print(pot.value)  # 150
```

---

## Methods

### `__init__()`

- **Use Case**: Initializes a new pot with a value of 0.
- **Example**: 
```python
# Create a new empty pot
pot = Pot()
print(pot.value)  # 0
```

---

### `add_to_pot(amount)`

- **Use Case**: Increments the pot by a given amount of chips.
- **Example**:  
```python
# Add chips to the pot
pot = Pot()
pot.add_to_pot(100)
print(pot.value)  # 100

# Add more chips
pot.add_to_pot(50)
print(pot.value)  # 150
```

---
