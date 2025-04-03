# `Button` Class Documentation

## Overview

The `Button` class defines a custom button GUI element for use with Pygame. It handles loading sprites from a spritesheet, scaling, drawing to screen, and detecting click events. It supports various button types used in the poker game interface (e.g., `"check"`, `"raise"`, `"new_game"`, `"settings"`).

---

## Instance Variables

### `spritesheet`

- **Type**: `pygame.Surface`
- **Description**: The image file containing all button sprites.
- **Example**: 
```python
# Load and check spritesheet
button = Button('../assets/buttons.png', (100 * SCALE, 75 * SCALE), 
                (SCALE, SCALE), 24, 12, 'new_game')
print(f"Spritesheet loaded: {button.spritesheet is not None}")
```

---

### `position`

- **Type**: `Tuple[int, int]`
- **Description**: The `(x, y)` position of the button on screen.
- **Example**: 
```python
# Position a raise button in the player action area
SCALE = 4
raise_button = Button('../assets/buttons.png', 
                     (150 * SCALE, 120 * SCALE),  # Bottom right for actions
                     (SCALE, SCALE), 24, 12, 'raise')
print(f"Button position: {raise_button.position}")
```

---

### `scale`

- **Type**: `Tuple[float, float]`
- **Description**: Scale factors for width and height of the sprite.
- **Example**: 
```python
# Create a button with game's standard scaling
SCALE = 4
button = Button('../assets/buttons.png', 
                (100 * SCALE, 75 * SCALE),
                (SCALE, SCALE), 24, 12, 'check')
print(f"Button scale: {button.scale}")  # (4, 4)
```

---

### `sprite_width`, `sprite_height`

- **Type**: `int`
- **Description**: Dimensions of the unscaled sprite in the spritesheet.
- **Example**: 
```python
# Check unscaled sprite dimensions
button = Button('sprites.png', (100, 300), (2, 2), 24, 12, 'raise')
print(f"Width: {button.sprite_width}")  # Width: 24
print(f"Height: {button.sprite_height}")  # Height: 12
```

---

### `scaled_width`, `scaled_height`

- **Type**: `int`
- **Description**: Final rendered dimensions after scaling.
- **Example**: 
```python
# Check scaled dimensions
button = Button('sprites.png', (100, 300), (2, 2), 24, 12, 'raise')
print(f"Scaled width: {button.scaled_width}")   # Scaled width: 48
print(f"Scaled height: {button.scaled_height}") # Scaled height: 24
```

---

### `callback`

- **Type**: `Optional[Callable]`
- **Description**: Function to call when button is clicked.
- **Example**: 
```python
# Create a settings button that changes screens
def to_settings():
    game_screen[0] = Screen.SETTINGS
    buttons.clear()
    # Initialize settings screen elements...

settings_button = Button(
    '../assets/buttons.png',
    (180 * SCALE, 20 * SCALE),
    (SCALE, SCALE), 24, 12,
    'settings',
    callback=lambda: to_settings()
)
buttons.append(settings_button)
```

---

### `unpressed_sprite`, `pressed_sprite`

- **Type**: `pygame.Surface`
- **Description**: Two versions of the sprite for visual feedback on press.
- **Example**: 
```python
# Switch between button states
button = Button('sprites.png', (100, 300), (2, 2), 24, 12, 'raise')
button.current_sprite = button.pressed_sprite
print("Button is now pressed")
button.current_sprite = button.unpressed_sprite
print("Button is now unpressed")
```

---

### `rect`

- **Type**: `pygame.Rect`
- **Description**: Used for collision detection and click hitbox.
- **Example**: 
```python
# Create a fold button with click detection
def player_fold():
    game_screen[0] = Screen.HOME
    buttons.clear()
    # Reset game state...

fold_button = Button(
    '../assets/buttons.png',
    (130 * SCALE, 120 * SCALE),
    (SCALE, SCALE), 24, 12,
    'fold',
    callback=lambda: player_fold()
)
buttons.append(fold_button)

# In game loop:
for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        if fold_button.rect.collidepoint(event.pos):
            fold_button.callback()
```

---

## Methods

### `__init__(...)`

- **Use Case**: Initializes the button with proper scaling and position for the poker interface.
- **Example**: 
```python
# Create a new game button for the main menu
def start_new_game():
    game_screen[0] = Screen.GAME
    buttons.clear()
    player_balance[0] = 500
    pot_total[0] = 0
    # Initialize game elements...

new_game_btn = Button(
    spritesheet='../assets/buttons.png',
    position=(100 * SCALE, 75 * SCALE),
    scale=(SCALE, SCALE),
    sprite_width=24,
    sprite_height=12,
    button_type='new_game',
    callback=lambda: start_new_game()
)
buttons.append(new_game_btn)
```

---

### `handle_event(event)`

- **Use Case**: Processes mouse events for button interactions.
- **Example**: 
```python
# Handle button events in the game loop
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        
        # Pass events to all buttons
        for button in buttons:
            button.handle_event(event)
```

---

### `draw(screen)`

- **Use Case**: Renders the button to the game screen.
- **Example**: 
```python
# Draw all buttons in the game loop
screen = pygame.display.set_mode((200 * SCALE, 150 * SCALE))

while RUNNING:
    screen.fill((0, 0, 0))
    
    # Draw appropriate background
    if game_screen[0] == Screen.GAME:
        screen.blit(game_background, (0, 0))
    
    # Draw all buttons
    for button in buttons:
        button.draw(screen)
    
    pygame.display.flip()
```

---
