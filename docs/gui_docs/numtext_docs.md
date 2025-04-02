# `NumText` Class Documentation

## Overview

The `NumText` class is a GUI component that displays numeric values using sprite-based digits. It's useful for rendering dynamic numbers like chip amounts or timers in a poker GUI. The digits are extracted from a provided spritesheet, recolored to white, scaled, and drawn on screen.

---

## Instance Variables

### `spritesheet`

- **Type**: `pygame.Surface`
- **Description**: The full image containing digit sprites from `0` to `9`.
- **Example**: 
```python
# Load number spritesheet
SCALE = 4
balance_display = NumText(
    '../assets/numbers.png',
    (160 * SCALE, 130 * SCALE),
    (SCALE, SCALE),
    player_balance[0]
)
print(f"Spritesheet loaded: {balance_display.spritesheet is not None}")
```

---

### `position`

- **Type**: `Tuple[int, int]`
- **Description**: The `(x, y)` top-left screen coordinates for drawing the number.
- **Example**: 
```python
# Position displays for player balance and pot
SCALE = 4
# Player balance at bottom right
balance_text = NumText(
    '../assets/numbers.png',
    (160 * SCALE, 130 * SCALE),  # Below player's cards
    (SCALE, SCALE),
    player_balance[0]
)
# Pot total in center
pot_text = NumText(
    '../assets/numbers.png',
    (100 * SCALE, 65 * SCALE),  # Above community cards
    (SCALE, SCALE),
    pot_total[0]
)
numtexts.extend([balance_text, pot_text])
```

---

### `scale`

- **Type**: `Tuple[float, float]`
- **Description**: Scaling factors applied to each digit sprite.
- **Example**: 
```python
# Create number displays with game's standard scaling
SCALE = 4
balance_display = NumText(
    '../assets/numbers.png',
    (160 * SCALE, 130 * SCALE),
    (SCALE, SCALE),
    player_balance[0]
)
print(f"Display scale: {balance_display.scale}")  # (4, 4)
```

---

### `number`

- **Type**: `int`
- **Description**: The numeric value currently being displayed.
- **Example**: 
```python
# Update displays when pot changes
def update_displays():
    for numtext in numtexts:
        if numtext.position[1] == 65 * SCALE:  # Pot display
            numtext.set_number(pot_total[0])
        elif numtext.position[1] == 130 * SCALE:  # Balance display
            numtext.set_number(player_balance[0])
```

---

### `label`

- **Type**: `Optional[str]`
- **Description**: Optional text label associated with the number.
- **Example**: 
```python
# Create labeled displays
SCALE = 4
balance_text = NumText(
    '../assets/numbers.png',
    (160 * SCALE, 130 * SCALE),
    (SCALE, SCALE),
    player_balance[0],
    label='balance'
)
pot_text = NumText(
    '../assets/numbers.png',
    (100 * SCALE, 65 * SCALE),
    (SCALE, SCALE),
    pot_total[0],
    label='pot'
)
```

---

### `digit_width`, `digit_height`

- **Type**: `int`
- **Description**: The width and height of each digit in the original spritesheet.
- **Example**: `self.digit_width  # 5`

---

### `digit_sprites`

- **Type**: `Dict[str, pygame.Surface]`
- **Description**: Mapping of digit characters (`'0'` to `'9'`) to scaled, white-colored sprites.
- **Example**: `self.digit_sprites['5']`

---

### `number_sprites`

- **Type**: `List[pygame.Surface]`
- **Description**: A list of surfaces representing the current number being displayed.
- **Example**: `len(self.number_sprites)  # 3` for number `150`

---

## Methods

### `__init__(spritesheet_path, position, scale, number, label=None)`

- **Use Case**: Initializes the component, loads and prepares all digit sprites.
- **Example**: 
```python
# Initialize displays for a new game
SCALE = 4
def init_game_displays():
    numtexts.clear()
    
    # Create balance display
    balance_text = NumText(
        '../assets/numbers.png',
        (160 * SCALE, 130 * SCALE),
        (SCALE, SCALE),
        player_balance[0],
        label='balance'
    )
    
    # Create pot display
    pot_text = NumText(
        '../assets/numbers.png',
        (100 * SCALE, 65 * SCALE),
        (SCALE, SCALE),
        pot_total[0],
        label='pot'
    )
    
    numtexts.extend([balance_text, pot_text])
```

---

### `recolor_sprite_white(sprite)`

- **Use Case**: Converts non-transparent pixels in a digit sprite to solid white.
- **Example**: `white_sprite = self.recolor_sprite_white(sprite)`

---

### `load_digit_sprites()`

- **Use Case**: Extracts and recolors all digit sprites from the spritesheet.
- **Example**: `sprites = self.load_digit_sprites()`

---

### `create_number_sprites(number)`

- **Use Case**: Converts an integer to its corresponding list of sprite surfaces.
- **Example**: `sprites = self.create_number_sprites(500)`

---

### `set_number(number)`

- **Use Case**: Updates the displayed number and regenerates the sprite list.
- **Example**: 
```python
# Update displays after a bet
def make_bet(amount):
    player_balance[0] -= amount
    pot_total[0] += amount
    
    # Update all displays
    for numtext in numtexts:
        if numtext.label == 'balance':
            numtext.set_number(player_balance[0])
        elif numtext.label == 'pot':
            numtext.set_number(pot_total[0])
```

---

### `draw(screen)`

- **Use Case**: Renders the number on the screen using the current digit sprites.
- **Example**: 
```python
# Draw all number displays in game loop
screen = pygame.display.set_mode((200 * SCALE, 150 * SCALE))

while RUNNING:
    screen.fill((0, 0, 0))
    screen.blit(game_background, (0, 0))
    
    # Draw all number displays
    for numtext in numtexts:
        numtext.draw(screen)
    
    pygame.display.flip()
```

---

### `handle_event(event)`

- **Use Case**: Processes any number display events (currently a placeholder).
- **Example**: 
```python
# Handle events in game loop
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            
        # Pass events to all displays
        for numtext in numtexts:
            numtext.handle_event(event)
```

---
