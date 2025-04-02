# `constants.py` Documentation

## Overview

This module defines several enumerations (`Enum` classes) used throughout the poker engine to represent player actions, game phases (streets), and player states. These enums ensure consistency and clarity when handling game logic and decision-making.

---

## Enums

### `Action`

Represents the various actions a player can take during a hand.

- **FOLD**: `Action.FOLD  # 0` – The player folds their hand.
- **CALL**: `Action.CALL  # 1` – The player calls the current bet.
- **RAISE**: `Action.RAISE  # 2` – The player raises the bet.
- **SMALL_BLIND**: `Action.SMALL_BLIND  # 3` – The small blind is posted.
- **BIG_BLIND**: `Action.BIG_BLIND  # 4` – The big blind is posted.
- **ANTE**: `Action.ANTE  # 5` – The player posts an ante.

---

### `Street`

Indicates the current phase of a hand in progress.

- **PREFLOP**: `Street.PREFLOP  # 0` – Before community cards are dealt.
- **FLOP**: `Street.FLOP  # 1` – First three community cards are revealed.
- **TURN**: `Street.TURN  # 2` – Fourth community card is revealed.
- **RIVER**: `Street.RIVER  # 3` – Fifth and final community card.
- **SHOWDOWN**: `Street.SHOWDOWN  # 4` – All players reveal hands.
- **FINISHED**: `Street.FINISHED  # 5` – Hand is complete.

---

### `PlayerState`

Tracks the current status of a player during a hand.

- **ACTIVE**: `PlayerState.ACTIVE  # 0` – The player is still in the hand and eligible to act.
- **FOLDED**: `PlayerState.FOLDED  # 1` – The player has folded.
- **ALLIN**: `PlayerState.ALLIN  # 2` – The player is all-in and cannot bet further.
- **WAITING**: `PlayerState.WAITING  # 3` – The player is not involved in the current hand.
- **WINNER**: `PlayerState.WINNER  # 4` – The player has won the hand.

---

## Example Usage

```python

action = Action.CALL  
if action == Action.CALL:  
    print("The player called.")
```
