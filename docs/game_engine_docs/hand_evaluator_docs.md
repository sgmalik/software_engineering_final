# `HandEvaluator` Class Documentation

## Overview

The `HandEvaluator` class analyzes poker hands by combining hole cards and community cards to determine hand strength. It provides detailed information for showdown evaluation, tie-breaking, and hand comparison.

---

## Core Concepts

### Hand Strength Hierarchy
The poker hand rankings from weakest (1) to strongest (10):
```python
STRENGTH_MAP = {
    'high_card': 1,
    'pair': 2,
    'two_pair': 3,
    'three_of_a_kind': 4,
    'straight': 5,
    'four_of_a_kind': 6,
    'flush': 7,
    'full_house': 8,
    'straight_flush': 9,
    'royal_flush': 10
}
```

### Card Representation
Cards are represented using the `Card` class with:
- `suit`: 'H', 'D', 'C', 'S' (Hearts, Diamonds, Clubs, Spades)
- `rank`: '2' through 'A' (Ace)

---

## Main Evaluation Method

### `hand_eval(hole_cards, community_cards)`
The primary method for evaluating a poker hand. It:
1. Combines hole cards and community cards
2. Checks for each hand type in descending strength order
3. Returns a structured dictionary containing:
   - Hand rank (1-10)
   - Primary cards that form the hand
   - Kicker cards for tie-breaking

Expected return format:
```python
{
    "strength": {
        "hand_rank": int,          # 1-10 ranking
        "primary_cards_rank": list  # Main hand forming cards
    },
    "kickers": list                # Tie-breaking cards
}
```

---

## Hand Detection Methods

Each of these methods analyzes the sorted cards to detect specific poker hands:

### `_is_royal_flush(sorted_cards)`
- Checks for Ace-high straight flush (A♠ K♠ Q♠ J♠ 10♠)
- Must be same suit and contain A,K,Q,J,10

### `_is_straight_flush(sorted_cards)`
- Checks for five sequential cards of the same suit
- Example: 8♠ 7♠ 6♠ 5♠ 4♠

### `_is_four_of_a_kind(sorted_cards)`
- Looks for four cards of the same rank
- Example: A♠ A♣ A♥ A♦

### `_is_full_house(sorted_cards)`
- Detects three of a kind plus a pair
- Example: K♠ K♣ K♥ 2♦ 2♠

### `_is_flush(sorted_cards)`
- Checks for five cards of the same suit
- Example: A♥ J♥ 8♥ 6♥ 2♥

### `_is_straight(sorted_cards)`
- Finds five sequential cards
- Handles Ace-low straight (A,2,3,4,5) special case
- Example: 8♠ 7♣ 6♥ 5♦ 4♠

### `_is_three_of_a_kind(sorted_cards)`
- Looks for three cards of the same rank
- Example: Q♠ Q♣ Q♥

### `_is_two_pair(sorted_cards)`
- Detects two different pairs
- Example: J♠ J♣ 8♥ 8♦

### `_is_pair(sorted_cards)`
- Finds two cards of the same rank
- Example: 5♠ 5♣

---

## Tie Breaking System

### Primary Cards
When hands have the same rank, primary cards are compared first:
- Pair: The rank of the paired cards
- Two Pair: Higher pair first, then lower pair
- Three/Four of a Kind: The rank of the matched cards
- Straight: The highest card in the sequence
- Flush: All five cards in descending order

### Kickers
Used when primary cards are equal:
- Highest remaining cards not part of the main hand
- Used in order until a winner is determined or all are equal
- Maximum of 5 total cards considered (main hand + kickers)

---

## Usage in Game Engine

The `HandEvaluator` integrates with the game engine for:
1. Showdown evaluation
2. Hand strength comparison
3. Winner determination in multi-way pots
4. CPU player decision making

The engine should:
1. Collect active players' hands
2. Evaluate each hand
3. Compare results to determine winner(s)
4. Handle split pots when hands are exactly equal

---

## Implementation Status

### Completed
- Basic class structure
- Hand rank definitions
- Card representation

### In Progress
- Hand type detection methods
- Kicker calculation
- Tie breaking logic

### TODO
- Implement remaining hand detection methods
- Add comprehensive unit tests
- Optimize performance for large hand comparisons
- Add hand description generator

---
