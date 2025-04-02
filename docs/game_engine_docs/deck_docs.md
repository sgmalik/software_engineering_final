# `Deck` Class Documentation

## Overview

The `Deck` class models a standard 52-card deck used in poker. It provides functionality for shuffling, drawing one or more cards, restoring the deck, and sorting cards by rank. The deck is automatically shuffled upon initialization.

---

## Class Constants

### `SUITS`

- **Type**: `List[str]`
- **Description**: List of valid card suits: hearts (`'H'`), diamonds (`'D'`), clubs (`'C'`), and spades (`'S'`).
- **Example**:

```python
# Access the suits constant
suits = Deck.SUITS
print(suits)  # ['H', 'D', 'C', 'S']
```

### `RANKS`

- **Type**: `List[str]`
- **Description**: List of valid card face values from `'2'` to `'A'`.
- **Example**: 

```python
# Access the ranks constant
ranks = Deck.RANKS
print(ranks)  # ['2', '3', ..., 'K', 'A']
```

---

## Instance Variables

### `cards`

- **Type**: `List[Card]`
- **Description**: The current list of remaining cards in the deck.
- **Example**: 
```python
deck = Deck()
num_cards = len(deck.cards)
print(num_cards)  # 52
```

---

## Methods

### `__init__()`

- **Use Case**: Initializes the deck with 52 cards and shuffles them.
- **Example**: 
```python
# Create a new shuffled deck
deck = Deck()
```

---

### `draw_card()`

- **Use Case**: Removes and returns one card from the top of the deck.
- **Example**: 
```python
# Draw a single card from the deck
deck = Deck()
card = deck.draw_card()
print(card)  # Example output: Card('H', 'A')
```

---

### `draw_cards(num_cards)`

- **Use Case**: Removes and returns a list of `num_cards` cards from the top of the deck.
- **Example**: 
```python
# Draw multiple cards from the deck
deck = Deck()
hand = deck.draw_cards(2)
print(hand)  # Example output: [Card('H', 'A'), Card('D', 'K')]
```

---

### `shuffle()`

- **Use Case**: Shuffles the current deck of cards using Python's `random.shuffle`.
- **Example**: 
```python
# Shuffle the deck
deck = Deck()
deck.shuffle()
```

---

### `restore()`

- **Use Case**: Resets the deck back to a full shuffled 52-card set.
- **Example**: 
```python
# Restore the deck to full 52 cards
deck = Deck()
deck.draw_cards(5)  # Draw some cards
deck.restore()      # Reset to full deck
```

---

### `sort_cards_by_rank(cards: list[Card]) -> list[Card]`

- **Use Case**: Returns the list of cards sorted by rank in descending order.
- **Example**:  
```python
# Sort cards by rank
cards = [Card('H', 'A'), Card('D', '10')]
sorted_cards = Deck.sort_cards_by_rank(cards)
print(sorted_cards)  # [Card('H', 'A'), Card('D', '10')]
```

---
