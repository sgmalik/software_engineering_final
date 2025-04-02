# `GameEvaluator` Class Documentation

## Overview

The `GameEvaluator` class is responsible for determining the winners of a poker hand and distributing chips from the pot accordingly. It is intended to support more complex features like side pots and multi-player evaluations in the future.

This class works closely with the `Table`, `Player`, and `HandEvaluator` classes to perform its tasks. Although many methods are still stubs, the structure has been laid out to support a fully functioning evaluation system.

---

## Methods

### `determine_winners(table: Table) -> List[Player]`

- **Purpose**: Determines the winners of a poker hand.
- **Current Behavior**: Always returns the first player for testing.
- **Future Behavior**:
  - Compares `hand_rank` of all active players.
  - If tied, compares `primary_cards_rank`.
  - If still tied, compares `kickers`.
  - Returns a list of winning players.

**Example**:
`winners = GameEvaluator.determine_winners(table)`

---

### `add_money_to_winners(table: Table, winners: List[Player])`

- **Purpose**: Distributes the pot to the winning players.
- **Status**: Not yet implemented.
- **Future Behavior**:
  - Split main pot among winners.
  - Handle leftover chips and distribute fairly.

---

### `_eligible_players(table: Table) -> List[Player]`

- **Purpose**: Filters out folded or inactive players.
- **Status**: Stubbed.
- **Expected Use**: Called internally by `determine_winners`.

---

### `_handle_pot()`

- **Purpose**: Logic for handling the pot and side pot distribution.
- **Status**: Placeholder.
- **Note**: Will be necessary for games with more than two players.

---

### `_get_side_pots()`

- **Purpose**: Computes side pots based on player contributions.
- **Status**: Placeholder.
- **Expected Output**: A list of side pots with associated eligible players.

---

## TODOs

- Implement proper hand comparison using `HandEvaluator`.
- Add logic to split pot among multiple winners.
- Handle edge cases (e.g., identical hands, all-in players).
- Build side pot support (`_get_side_pots`, `_handle_pot`).
- Add unit tests to validate win scenarios.

---
