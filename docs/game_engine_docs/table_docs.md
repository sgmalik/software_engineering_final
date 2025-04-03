# `Table` Class Documentation

## Overview

The `Table` class serves as the central controller for a game of poker. It manages players, the deck, community cards, the pot, and whose turn it is. It provides helper methods for setting up a game round, dealing cards, tracking blinds, and moving through player turns. This class acts as a bridge between game logic and the visual interface.

---

## Instance Variables

### `blind_pos`

- **Type**: `int`
- **Description**: Tracks the small blind position; alternates between players in heads-up mode.
- **Example**: 
```python
# Check the current blind position
table = Table()
print(table.blind_pos)  # 0
```

---

### `community_cards`

- **Type**: `List[Card]`
- **Description**: Stores shared community cards revealed during the hand.
- **Example**: 
```python
# View the community cards
table = Table()
table.deal_community_cards(2)
print(table.community_cards)  # [Card('H', 'A'), Card('D', 'K')]
```

---

### `deck`

- **Type**: `Deck`
- **Description**: The current deck object used to deal cards.
- **Example**: 
```python
# Use the table's deck
table = Table()
card = table.deck.draw_card()
print(card)  # Example output: Card('S', 'Q')
```

---

### `pot`

- **Type**: `Pot`
- **Description**: Tracks the total chips in the pot for the current hand.
- **Example**: 
```python
# Check the pot value
table = Table()
table.pot.add_to_pot(400)
print(table.pot.value)  # 400
```

---

### `players`

- **Type**: `List[Player]`
- **Description**: List of all players at the table.
- **Example**: 
```python
# Initialize and check number of players
table = Table()
table.init_players(1000, 2)
print(len(table.players))  # 2
```

---

### `current_player`

- **Type**: `Player`
- **Description**: The player whose turn it currently is.
- **Example**: 
```python
# Check current player
table = Table()
table.init_players(1000, 2)
print(table.current_player.name)  # 'pc'
```

---

## Methods

### `__init__()`

- **Use Case**: Initializes a table with a shuffled deck, empty pot, empty player list, and default state.
- **Example**: 
```python
# Create a new table
table = Table()
print(len(table.players))  # 0
print(table.pot.value)     # 0
```

---

### `init_players(initial_stack, num_players)`

- **Use Case**: Instantiates `num_players` players with the given starting stack, names the first `"pc"`, and sets it as the current player.
- **Example**: 
```python
# Initialize players
table = Table()
table.init_players(1000, 2)
print(table.players[0].name)    # 'pc'
print(table.players[0].stack)   # 1000
```

---

### `reset_table()`

- **Use Case**: Prepares the table for a new round. (Note: currently unimplemented.)
- **Example**: 
```python
# Reset the table for a new round
table = Table()
table.reset_table()
```

---

### `next_player()`

- **Use Case**: Advances `current_player` to the next player in the list (wraps around at the end).
- **Example**: 
```python
# Move to next player
table = Table()
table.init_players(1000, 2)
current = table.current_player.name
table.next_player()
next_player = table.current_player.name
print(f"{current} -> {next_player}")  # 'pc' -> 'player2'
```

---

### `deal_hole_cards()`

- **Use Case**: Deals two private cards to each player from the deck.
- **Example**: 
```python
# Deal hole cards to players
table = Table()
table.init_players(1000, 2)
table.deal_hole_cards()
print(len(table.players[0].hole_cards))  # 2
```

---

### `set_blind_pos()`

- **Use Case**: Alternates the blind position between heads-up players.
- **Example**: 
```python
# Alternate blind position
table = Table()
initial_pos = table.blind_pos
table.set_blind_pos()
new_pos = table.blind_pos
print(f"Blind moved: {initial_pos} -> {new_pos}")  # "Blind moved: 0 -> 1"
```

---

### `deal_community_cards(num_cards)`

- **Use Case**: Deals a specified number of community cards and appends them to the table.
- **Example**: 
```python
# Deal flop
table = Table()
table.deal_community_cards(3)
print(len(table.community_cards))  # 3
```

---

### `active_players()`

- **Use Case**: Returns a list of players whose state is `ACTIVE`.
- **Example**: 
```python
# Get active players
table = Table()
table.init_players(1000, 2)
active = table.active_players()
print(len(active))  # 2
```

---

### `reset_contribution()`

- **Use Case**: Resets each player's contribution to the pot at the start of a new street.
- **Example**: 
```python
# Reset player contributions
table = Table()
table.init_players(1000, 2)
table.players[0].contribution = 100
table.reset_contribution()
print(table.players[0].contribution)  # 0
```

---

### `is_players_turn() -> bool`

- **Use Case**: Returns `True` if the current player is `"pc"` and in the `ACTIVE` state. Useful for GUI checks.
- **Example**: 
```python
# Check if it's the player's turn
table = Table()
table.init_players(1000, 2)
if table.is_players_turn():
    print("Player's turn!")  # "Player's turn!"
```

---
