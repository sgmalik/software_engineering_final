# `GUI_Card` Class Documentation

## Overview

The `GUI_Card` class is a graphical UI component for rendering playing cards in the poker game interface. It handles card positioning, scaling, sprite extraction from a spritesheet, and conditional rendering based on whether the card is face-up (`revealed`) or hidden.

---

## Instance Variables

### `spritesheet`

- **Type**: `pygame.Surface`
- **Description**: The full card spritesheet used to extract graphical assets.
- **Example**: 
```python
# Load card spritesheet
card = GUI_Card('../assets/cards.png', 
                (90 * SCALE, 100 * SCALE),
                (SCALE, SCALE), 'a', 'hearts')
print(f"Spritesheet loaded: {card.spritesheet is not None}")
```

---

### `position`

- **Type**: `Tuple[int, int]`
- **Description**: The `(x, y)` coordinates where the card is drawn on the screen.
- **Example**: 
```python
# Position player's hole cards
SCALE = 4
player_card1 = GUI_Card(
    '../assets/cards.png',
    (90 * SCALE, 100 * SCALE),  # Bottom center for player
    (SCALE, SCALE), 'a', 'hearts',
    revealed=True
)
player_card2 = GUI_Card(
    '../assets/cards.png',
    (110 * SCALE, 100 * SCALE),  # Slightly right of first card
    (SCALE, SCALE), 'k', 'hearts',
    revealed=True
)
cards.extend([player_card1, player_card2])
```

---

### `scale`

- **Type**: `Tuple[float, float]`
- **Description**: Scaling factors for rendering the card.
- **Example**: 
```python
# Check card scaling
card = GUI_Card('../assets/cards.png', (90 * SCALE, 100 * SCALE), (SCALE, SCALE), 'a', 'hearts')
print(card.scale)  # (4.0, 4.0)
print(f"Width scale: {card.scale[0]}x, Height scale: {card.scale[1]}x")
```

---

### `revealed`

- **Type**: `bool`
- **Description**: Whether the card is shown face-up or as a back card.
- **Example**: 
```python
# Create opponent's hidden cards
opponent_card1 = GUI_Card(
    '../assets/cards.png',
    (90 * SCALE, 20 * SCALE),  # Top center for opponent
    (SCALE, SCALE), 'q', 'spades',
    revealed=False  # Face down
)
opponent_card2 = GUI_Card(
    '../assets/cards.png',
    (110 * SCALE, 20 * SCALE),
    (SCALE, SCALE), '10', 'clubs',
    revealed=False  # Face down
)
cards.extend([opponent_card1, opponent_card2])
```

---

### `rank`, `suite`

- **Type**: `str`
- **Description**: Card identity used to determine which sprites to load.
- **Example**: 
```python
# Create community cards (flop)
flop_cards = [
    GUI_Card('../assets/cards.png', 
            (70 * SCALE, 60 * SCALE),
            (SCALE, SCALE), '7', 'diamonds', True),
    GUI_Card('../assets/cards.png', 
            (90 * SCALE, 60 * SCALE),
            (SCALE, SCALE), 'j', 'clubs', True),
    GUI_Card('../assets/cards.png', 
            (110 * SCALE, 60 * SCALE),
            (SCALE, SCALE), '2', 'hearts', True)
]
cards.extend(flop_cards)
```

---

### `card_width`, `card_height`

- **Type**: `int`
- **Description**: Original (unscaled) sprite size in pixels.
- **Example**: 
```python
# Check card dimensions
card = GUI_Card('../assets/cards.png', (90 * SCALE, 100 * SCALE), (SCALE, SCALE), 'a', 'hearts')
print(f"Original width: {card.card_width}")   # Original width: 19
print(f"Original height: {card.card_height}") # Original height: 31
print(f"Scaled width: {card.card_width * card.scale[0]}")   # Scaled width: 76
print(f"Scaled height: {card.card_height * card.scale[1]}") # Scaled height: 124
```

---

### `back_sprite`, `open_sprite`, `suite_sprite`, `rank_sprite`

- **Type**: `pygame.Surface`
- **Description**: Sprites used for rendering the card in various layers.
- **Example**: 
```python
# Check sprite dimensions
card = GUI_Card('../assets/cards.png', (90 * SCALE, 100 * SCALE), (SCALE, SCALE), 'a', 'hearts')
print(f"Back sprite height: {card.back_sprite.get_height()}")
print(f"Open sprite height: {card.open_sprite.get_height()}")
print(f"Suite sprite height: {card.suite_sprite.get_height()}")
print(f"Rank sprite height: {card.rank_sprite.get_height()}")
```

---

## Methods

### `__init__(...)`

- **Use Case**: Initializes a card with proper scaling and position for the poker table.
- **Example**: 
```python
# Deal turn card
turn_card = GUI_Card(
    spritesheet='../assets/cards.png',
    position=(130 * SCALE, 60 * SCALE),  # Right of flop
    scale=(SCALE, SCALE),
    rank='8',
    suite='spades',
    revealed=True
)
cards.append(turn_card)
```

---

### `get_sprite(x, y, width, height)`

- **Use Case**: Extracts and scales a specific portion of the spritesheet.
- **Example**: 
```python
# Extract a sprite from the spritesheet
card = GUI_Card('../assets/cards.png', (90 * SCALE, 100 * SCALE), (SCALE, SCALE), 'a', 'hearts')
sprite = card.get_sprite(0, 0, 19, 31)
print(f"Extracted sprite dimensions: {sprite.get_width()}x{sprite.get_height()}")
```

---

### `get_suite_sprite()`

- **Use Case**: Extracts the icon sprite for the card's suite (hearts, diamonds, etc.).
- **Example**: 
```python
# Get the suite icon
card = GUI_Card('../assets/cards.png', (90 * SCALE, 100 * SCALE), (SCALE, SCALE), 'a', 'hearts')
suite_icon = card.get_suite_sprite()
print(f"Suite sprite dimensions: {suite_icon.get_width()}x{suite_icon.get_height()}")
```

---

### `get_rank_sprite()`

- **Use Case**: Extracts the symbol sprite for the card's rank (e.g., `'a'`, `'k'`, `'10'`).
- **Example**: 
```python
# Get the rank symbol
card = GUI_Card('../assets/cards.png', (90 * SCALE, 100 * SCALE), (SCALE, SCALE), 'k', 'spades')
rank_symbol = card.get_rank_sprite()
print(f"Rank sprite dimensions: {rank_symbol.get_width()}x{rank_symbol.get_height()}")
```

---

### `draw(screen)`

- **Use Case**: Renders the card to the game screen.
- **Example**: 
```python
# Draw all cards in the game loop
screen = pygame.display.set_mode((200 * SCALE, 150 * SCALE))

while RUNNING:
    screen.fill((0, 0, 0))
    screen.blit(game_background, (0, 0))
    
    # Draw all cards
    for card in cards:
        card.draw(screen)
    
    pygame.display.flip()
```

---

### `handle_event(event)`

- **Use Case**: Processes any card-related events (currently a placeholder).
- **Example**: 
```python
# Handle card events in the game loop
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            
        # Pass events to all cards
        for card in cards:
            card.handle_event(event)
```

---
