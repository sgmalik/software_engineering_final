# `util.py` GUI Utilities Documentation

## Overview

The `util.py` module contains helper functions and global constants for managing GUI states in the poker game. It handles screen transitions, creates and clears interface elements (buttons, cards, chips, etc.), and manages visual updates like betting, balance, and pot contributions. It is designed to abstract GUI layout logic from the main game loop.

---

## Constants

### `SPRITESHEET_PATH`

- **Type**: `str`
- **Description**: File path to the main sprite asset used across all GUI elements.
- **Example**: 
```python
# Load game assets
SCALE = 4
main_menu_background = pygame.transform.scale(
    pygame.image.load("../assets/poker-main-menu.png"), 
    (200 * SCALE, 150 * SCALE)
)
```

---

## Enums

### `Screen`

- **Type**: `Enum`
- **Values**: `HOME`, `SETTINGS`, `GAME`
- **Description**: Tracks which screen is currently active in the GUI.
- **Example**: 
```python
# Handle screen transitions
game_screen = [Screen.HOME]  # Using list for mutability

if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_ESCAPE:
        change_to_main_menu(SCALE, game_screen, buttons, sliders, 
                          cards, chips, numtexts, player_balance, pot_total)

# Draw current screen
if game_screen[0] == Screen.HOME:
    screen.blit(main_menu_background, (0, 0))
elif game_screen[0] == Screen.SETTINGS:
    screen.blit(settings_background, (0, 0))
elif game_screen[0] == Screen.GAME:
    screen.blit(game_background, (0, 0))
```

---

## Functions

### `get_proper_chip_distribution(user_value)`

- **Use Case**: Returns a list of chip counts representing the optimal visual distribution for a given amount.
- **Returns**: `[1_count, 5_count, 10_count, 50_count, 100_count]`
- **Example**: 
```python
# Calculate chip distribution for player balance
SCALE = 4
player_balance = [500]

def update_chip_display():
    chips.clear()
    distribution = get_proper_chip_distribution(player_balance[0])
    # [0, 0, 0, 2, 5] for 500 chips
    update_player_chips(chips, SCALE, player_balance)
```

---

### `change_to_main_menu(scale, game_screen, buttons, sliders, cards, chips, numtexts, player_balance, pot_total)`

- **Use Case**: Transitions the GUI to the home screen with "New Game" and "Settings" buttons.
- **Example**: 
```python
# Initialize game and handle menu transitions
SCALE = 4
game_screen = [Screen.HOME]
buttons = []
sliders = []
cards = []
chips = []
numtexts = []
player_balance = [500]
pot_total = [0]

# Initial setup
change_to_main_menu(SCALE, game_screen, buttons, sliders, 
                   cards, chips, numtexts, player_balance, pot_total)

# Handle escape key
if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
    change_to_main_menu(SCALE, game_screen, buttons, sliders,
                       cards, chips, numtexts, player_balance, pot_total)
```

---

### `change_to_settings(scale, game_screen, buttons, sliders, cards, chips, numtexts)`

- **Use Case**: Transitions the GUI to the settings screen with options like "Change Card" and "Difficulty".
- **Example**: `change_to_settings(2, screen_ref, btns, sliders, cards, chips, texts)`

---

### `change_to_game(scale, game_screen, buttons, sliders, cards, chips, numtexts, player_balance, pot_total)`

- **Use Case**: Configures all GUI elements for in-game play, including cards, chips, sliders, buttons, and stat tracking.
- **Example**: 
```python
# Start new game from main menu
def start_new_game():
    player_balance[0] = 500
    pot_total[0] = 0
    change_to_game(SCALE, game_screen, buttons, sliders,
                  cards, chips, numtexts, player_balance, pot_total)

# Create new game button
new_game_btn = Button(
    '../assets/buttons.png',
    (100 * SCALE, 75 * SCALE),
    (SCALE, SCALE),
    sprite_width=24,
    sprite_height=12,
    button_type='new_game',
    callback=lambda: start_new_game()
)
buttons.append(new_game_btn)
```

---

### `update_player_chips(chips, scale, player_balance)`

- **Use Case**: Rebuilds the visual chip stack for the player after betting or winning a hand.
- **Example**: 
```python
# Update chips after betting
def make_bet(amount):
    player_balance[0] -= amount
    pot_total[0] += amount
    
    # Update visual elements
    chips.clear()
    update_player_chips(chips, SCALE, player_balance)
    add_chips_to_pot(chips, SCALE, pot_total[0])
```

---

### `bet_percentage(percent, player_balance, pot_total, chips, scale, numtexts)`

- **Use Case**: Handles logic for betting 25%, 50%, 75%, or All In from the player's balance.
- **Example**: 
```python
# Create percentage bet buttons
def create_bet_buttons():
    bet_50_btn = Button(
        '../assets/buttons.png',
        (150 * SCALE, 120 * SCALE),
        (SCALE, SCALE),
        sprite_width=24,
        sprite_height=12,
        button_type='bet_half',
        callback=lambda: bet_percentage(0.5, player_balance, pot_total,
                                     chips, SCALE, numtexts)
    )
    buttons.append(bet_50_btn)
```

---

### `add_chips_to_pot(chips, scale, amount)`

- **Use Case**: Visually adds chips to the pot area in the center of the table.
- **Example**: 
```python
# Update pot display after betting
def update_pot_display():
    # Clear existing pot chips
    chips = [chip for chip in chips if chip.position[1] != 75 * SCALE]
    
    # Add new chips to represent pot
    add_chips_to_pot(chips, SCALE, pot_total[0])
    
    # Update numeric display
    for numtext in numtexts:
        if numtext.label == 'pot':
            numtext.set_number(pot_total[0])
```

---
