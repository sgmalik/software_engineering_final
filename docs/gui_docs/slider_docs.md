# `Slider` Class Documentation

## Overview

The `Slider` class is a GUI component that allows users to interactively slide a thumb control vertically along a track. It is useful for adjusting game parameters such as bet size or volume. The class supports dragging, bounding logic, and uses sprites from a custom spritesheet.

---

## Instance Variables

### `spritesheet`

- **Type**: `pygame.Surface`
- **Description**: The full image containing the slider base and thumb graphics.
- **Example**: 
```python
# Load slider spritesheet
SCALE = 4
bet_slider = Slider(
    '../assets/slider.png',
    (170 * SCALE, 100 * SCALE),
    (SCALE, SCALE),
    10, 100, 10, 20
)
print(f"Spritesheet loaded: {bet_slider.spritesheet is not None}")
```

---

### `position`

- **Type**: `Tuple[int, int]`
- **Description**: The `(x, y)` position of the top-left corner of the slider base on the screen.
- **Example**: 
```python
# Position bet slider in game interface
SCALE = 4
bet_slider = Slider(
    '../assets/slider.png',
    (170 * SCALE, 100 * SCALE),  # Right side of screen for bet control
    (SCALE, SCALE),
    10, 100, 10, 20
)
sliders.append(bet_slider)
```

---

### `scale`

- **Type**: `Tuple[float, float]`
- **Description**: Scale factors for both the base and the thumb.
- **Example**: 
```python
# Create slider with game's standard scaling
SCALE = 4
bet_slider = Slider(
    '../assets/slider.png',
    (170 * SCALE, 100 * SCALE),
    (SCALE, SCALE),  # Match game's global scale
    10, 100, 10, 20
)
print(f"Slider scale: {bet_slider.scale}")  # (4, 4)
```

---

### `scaled_base_width`, `scaled_base_height`

- **Type**: `float`
- **Description**: Scaled dimensions of the slider base.
- **Example**: `self.scaled_base_height  # 100.0`

---

### `scaled_thumb_width`, `scaled_thumb_height`

- **Type**: `float`
- **Description**: Scaled dimensions of the slider thumb.
- **Example**: `self.scaled_thumb_height  # 20.0`

---

### `base_sprite`, `thumb_sprite`

- **Type**: `pygame.Surface`
- **Description**: Sprites used to render the slider base and thumb.
- **Example**: `screen.blit(self.thumb_sprite, self.thumb_position)`

---

### `thumb_position`

- **Type**: `Tuple[int, int]`
- **Description**: Current position of the slider thumb on the screen.
- **Example**: 
```python
# Update bet amount based on slider position
def get_bet_amount(slider):
    # Convert slider position to bet amount
    min_bet = 10
    max_bet = min(100, player_balance[0])
    position_ratio = (slider.thumb_position[1] - slider.min_y) / (slider.max_y - slider.min_y)
    bet = min_bet + position_ratio * (max_bet - min_bet)
    return int(bet)
```

---

### `min_y`, `max_y`

- **Type**: `int`
- **Description**: Y-axis bounds for dragging the thumb vertically.
- **Example**: `self.min_y  # 150`, `self.max_y  # 250`

---

### `dragging`

- **Type**: `bool`
- **Description**: Whether the thumb is currently being dragged by the user.
- **Example**: 
```python
# Check if slider is being adjusted
def update_bet_display():
    for slider in sliders:
        if slider.dragging:
            current_bet = get_bet_amount(slider)
            # Update bet display...
```

---

## Methods

### `__init__(...)`

- **Use Case**: Initializes the slider, loads sprites, sets dimensions, and positions the thumb.
- **Example**: 
```python
# Initialize bet slider for game
SCALE = 4
def init_bet_slider():
    sliders.clear()
    
    bet_slider = Slider(
        spritesheet='../assets/slider.png',
        position=(170 * SCALE, 100 * SCALE),
        scale=(SCALE, SCALE),
        base_width=10,
        base_height=100,
        thumb_width=10,
        thumb_height=20
    )
    sliders.append(bet_slider)
```

---

### `get_sprite(x, y, width, height)`

- **Use Case**: Extracts a sprite from the spritesheet at the given coordinates and scales it.
- **Example**: `sprite = self.get_sprite(0, 76, 10, 100)`

---

### `handle_event(event)`

- **Use Case**: Manages mouse interaction for dragging the slider thumb within bounds.
- **Example**: 
```python
# Handle slider events in game loop
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        
        # Pass events to all sliders
        for slider in sliders:
            slider.handle_event(event)
            if slider.dragging:
                # Update bet amount based on slider position
                current_bet = get_bet_amount(slider)
                # Update displays...
```

---

### `draw(screen)`

- **Use Case**: Draws both the slider base and the thumb to the screen.
- **Example**: 
```python
# Draw all sliders in game loop
screen = pygame.display.set_mode((200 * SCALE, 150 * SCALE))

while RUNNING:
    screen.fill((0, 0, 0))
    screen.blit(game_background, (0, 0))
    
    # Draw all sliders
    for slider in sliders:
        slider.draw(screen)
    
    pygame.display.flip()
```

---
