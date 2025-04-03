# `Chip` Class Documentation

## Overview

The `Chip` class represents a visual chip element for the poker GUI, built with Pygame. It supports sprite extraction from a spritesheet based on chip color and can be drawn at a specified location with scaling. This class is designed for simple, modular integration into the game's graphical interface.

---

## Instance Variables

### `spritesheet`

- **Type**: `pygame.Surface`
- **Description**: The loaded image containing all chip variations.
- **Example**: 
```python
# Load chip spritesheet
SCALE = 4
chip = Chip('../assets/chips.png', 
            (100 * SCALE, 75 * SCALE),
            (SCALE, SCALE), 'red')
print(f"Spritesheet loaded: {chip.spritesheet is not None}")
```

---

### `position`

- **Type**: `Tuple[int, int]`
- **Description**: The `(x, y)` coordinates where the chip will be drawn on screen.
- **Example**: 
```python
# Position chips for player's stack
SCALE = 4
player_chips = [
    Chip('../assets/chips.png',
         (160 * SCALE, 120 * SCALE),  # Bottom right for player stack
         (SCALE, SCALE), 'blue'),
    Chip('../assets/chips.png',
         (165 * SCALE, 120 * SCALE),  # Slightly offset for stacked appearance
         (SCALE, SCALE), 'blue')
]
chips.extend(player_chips)
```

---

### `scale`

- **Type**: `Tuple[float, float]`
- **Description**: Scaling factors applied to the chip image.
- **Example**: 
```python
# Create chips with game's standard scaling
SCALE = 4
pot_chip = Chip('../assets/chips.png',
                (100 * SCALE, 75 * SCALE),  # Center for pot
                (SCALE, SCALE), 'red')
print(f"Chip scale: {pot_chip.scale}")  # (4, 4)
chips.append(pot_chip)
```

---

### `color`

- **Type**: `str`
- **Description**: The color identifier for the chip. Determines sprite selection.
- **Example**: 
```python
# Create chips for different denominations
SCALE = 4
denominations = {
    'blue': 10,
    'red': 25,
    'green': 100
}

for color, value in denominations.items():
    chip = Chip('../assets/chips.png',
                (100 * SCALE, 75 * SCALE),
                (SCALE, SCALE), color)
    chips.append(chip)
```

---

### `chip_width`, `chip_height`

- **Type**: `int`
- **Description**: The original (unscaled) dimensions of the chip sprite.
- **Example**: 
```python
# Check chip dimensions
SCALE = 4
chip = Chip('../assets/chips.png', (100 * SCALE, 75 * SCALE), (SCALE, SCALE), 'red')
print(f"Original size: {chip.chip_width}x{chip.chip_height}")  # 11x11
print(f"Scaled size: {chip.chip_width * SCALE}x{chip.chip_height * SCALE}")  # 44x44
```

---

### `chip_sprite`

- **Type**: `pygame.Surface`
- **Description**: The scaled chip sprite image used for rendering.
- **Example**: `screen.blit(self.chip_sprite, self.position)`

---

## Methods

### `__init__(spritesheet_path, position, scale, color)`

- **Use Case**: Initializes the chip object and loads the correct sprite based on color.
- **Example**: 
```python
# Create pot chips based on current pot value
SCALE = 4
def update_pot_chips():
    chips.clear()  # Remove old chips
    
    # Add chips to represent pot_total[0]
    if pot_total[0] >= 100:
        pot_chip = Chip('../assets/chips.png',
                       (100 * SCALE, 75 * SCALE),
                       (SCALE, SCALE), 'green')
        chips.append(pot_chip)
    elif pot_total[0] >= 25:
        pot_chip = Chip('../assets/chips.png',
                       (100 * SCALE, 75 * SCALE),
                       (SCALE, SCALE), 'red')
        chips.append(pot_chip)
```

---

### `get_chip_sprite()`

- **Use Case**: Extracts the correct sprite from the spritesheet based on the chip's color.
- **Example**: `sprite = self.get_chip_sprite()`

---

### `get_sprite(x, y, width, height)`

- **Use Case**: Extracts and scales a sub-image from the spritesheet.
- **Example**: `scaled = self.get_sprite(22, 47, 11, 11)`

---

### `draw(screen)`

- **Use Case**: Draws the chip to the specified screen surface.
- **Example**: 
```python
# Draw all chips in the game loop
screen = pygame.display.set_mode((200 * SCALE, 150 * SCALE))

while RUNNING:
    screen.fill((0, 0, 0))
    screen.blit(game_background, (0, 0))
    
    # Draw all chips
    for chip in chips:
        chip.draw(screen)
    
    pygame.display.flip()
```

---

### `handle_event(event)`

- **Use Case**: Processes any chip-related events (currently a placeholder).
- **Example**: 
```python
# Handle chip events in the game loop
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            
        # Pass events to all chips
        for chip in chips:
            chip.handle_event(event)
```

---
