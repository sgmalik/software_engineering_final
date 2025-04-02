# 🕹 `main.py` Documentation

## Overview

`main.py` serves as the entry point for the poker game, implementing a Pygame-based GUI. It manages the game's visual state, event handling, and screen transitions while maintaining separation from the core game logic.

---

## Core Initialization

### Pygame Setup
```python
import pygame
from gui.util import change_to_main_menu, Screen

# Initialize Pygame and set up display
pygame.init()
SCALE = 4
screen = pygame.display.set_mode((200 * SCALE, 150 * SCALE))
pygame.display.set_caption("Poker")
```

### Background Assets
```python
# Load and scale background images
main_menu_background = pygame.transform.scale(
    pygame.image.load("../assets/poker-main-menu.png"), 
    (200 * SCALE, 150 * SCALE)
)
settings_background = pygame.transform.scale(
    pygame.image.load("../assets/poker-settings.png"), 
    (200 * SCALE, 150 * SCALE)
)
game_background = pygame.transform.scale(
    pygame.image.load("../assets/poker-board.png"), 
    (200 * SCALE, 150 * SCALE)
)
```

---

## State Management

### Global State Variables
```python
# Screen state (mutable reference)
game_screen = [Screen.HOME]

# GUI element collections
buttons = []    # Action buttons, menu options
sliders = []    # Bet amount control
cards = []      # Player cards, community cards
chips = []      # Visual chip stacks
numtexts = []   # Numeric displays (balance, pot)

# Game state (mutable references)
player_balance = [500]  # Starting chips
pot_total = [0]        # Current pot
```

### Screen Management
The game maintains three distinct screens:

1. **HOME** (Main Menu)
   - "New Game" button
   - "Settings" button
   - Decorative background

2. **SETTINGS**
   - Difficulty options
   - Audio controls
   - Return to menu option

3. **GAME**
   - Poker table layout
   - Player/CPU cards
   - Betting controls
   - Chip displays

```python
# Screen rendering logic
if game_screen[0] == Screen.HOME:
    screen.blit(main_menu_background, (0, 0))
elif game_screen[0] == Screen.SETTINGS:
    screen.blit(settings_background, (0, 0))
elif game_screen[0] == Screen.GAME:
    screen.blit(game_background, (0, 0))
```

---

## Event Handling

### Main Event Loop
```python
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        # Quit handling
        if event.type == pygame.QUIT:
            RUNNING = False
            
        # Menu navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                change_to_main_menu(SCALE, game_screen, buttons, 
                                  sliders, cards, chips, numtexts,
                                  player_balance, pot_total)
        
        # Distribute events to GUI elements
        for button in buttons:
            button.handle_event(event)
        for slider in sliders:
            slider.handle_event(event)
        for card in cards:
            card.handle_event(event)
        for chip in chips:
            chip.handle_event(event)
        for numtext in numtexts:
            numtext.handle_event(event)
```

### Screen Transitions
Screen changes are managed through utility functions that:
1. Clear existing GUI elements
2. Initialize new elements for the target screen
3. Update game state as needed

```python
def example_transition_to_game():
    # Clear existing elements
    buttons.clear()
    sliders.clear()
    cards.clear()
    chips.clear()
    numtexts.clear()
    
    # Set up game screen
    game_screen[0] = Screen.GAME
    player_balance[0] = 500
    pot_total[0] = 0
    
    # Initialize game GUI elements...
```

---

## Rendering Pipeline

### Frame Rendering
Each frame follows this rendering order:
1. Clear screen
2. Draw background
3. Draw GUI elements in layers
4. Update display

```python
# Render frame
screen.fill((0, 0, 0))  # Clear screen

# Draw current background
if game_screen[0] == Screen.GAME:
    screen.blit(game_background, (0, 0))

# Draw GUI elements in order
for button in buttons:
    button.draw(screen)
for slider in sliders:
    slider.draw(screen)
for card in cards:
    card.draw(screen)
for chip in chips:
    chip.draw(screen)
for numtext in numtexts:
    numtext.draw(screen)

pygame.display.flip()
```

### Element Positioning
All GUI elements use the global `SCALE` factor for positioning:
```python
# Example positions for game screen elements
CARD_POSITIONS = {
    'player': (90 * SCALE, 100 * SCALE),
    'cpu': (90 * SCALE, 20 * SCALE),
    'community': (80 * SCALE, 60 * SCALE)
}

BUTTON_POSITIONS = {
    'fold': (130 * SCALE, 120 * SCALE),
    'raise': (150 * SCALE, 120 * SCALE),
    'check': (170 * SCALE, 120 * SCALE)
}
```

---

## Integration Points

### Game Engine Interface
The main loop will eventually integrate with the game engine through:
```python
# Example engine integration
def update_game_state():
    game_state = engine.current_state_of_game()
    
    # Update GUI based on state
    player_balance[0] = game_state['player_balance']
    pot_total[0] = game_state['pot_total']
    
    # Update visual elements...
```

### Asset Requirements
- All sprites must be designed for 4x scaling
- Background dimensions: 200x150 (pre-scaling)
- Consistent color palette across assets
- Transparent backgrounds for overlays

---

## Future Enhancements

### Planned Features
- Screen transition animations
- Sound effects and background music
- Enhanced betting animations
- Player statistics display
- Tournament mode support

### Performance Optimizations
- Sprite batching for card rendering
- Background caching
- Event handling optimization
- Asset preloading

---
