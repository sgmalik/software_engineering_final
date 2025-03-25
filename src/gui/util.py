from gui.button import Button
from gui.slider import Slider
from gui.card import Card
from gui.chip import Chip
from enum import Enum

spritesheet_path = "../assets/poker-spritesheet.png"


class Screen(Enum):
    """
    Represents the screen being displayed
    """
    HOME  = 0
    SETTINGS  = 1
    GAME = 2


def get_proper_chip_distribution(user_value):
    """
    Given the users current balance, return a distribution of chips that
    are able to represent any value from (0-user_value), while also
    adding up to the users current balance

    Primarily a visual thing, doesn't actually serve much of a logical
    thing, just makes the game look polished and beautiful.
    """
    distribution = [0, 0, 0, 0, 0]

    # First, get an even distribution of chips, starting from
    # the ones, going to the 100s. This ensures we have enough of
    # each denomination to reach all values
    while user_value >= 1 and distribution[0] < 4:
        distribution[0] += 1
        user_value -= 1
    while user_value >= 5 and distribution[1] < 4:
        distribution[1] += 1
        user_value -= 5
    while user_value >= 10 and distribution[2] < 4:
        distribution[2] += 1
        user_value -= 10
    while user_value >= 50 and distribution[3] < 4:
        distribution[3] += 1
        user_value -= 50
    while user_value >= 100 and distribution[4] < 4:
        distribution[4] += 1
        user_value -= 100

    # Then, with the remaining chips, start from 100 going to 1 adding
    # the remaining chips
    while user_value >= 100:
        distribution[4] += 1
        user_value -= 100
    while user_value >= 50:
        distribution[3] += 1
        user_value -= 50
    while user_value >= 10:
        distribution[2] += 1
        user_value -= 10
    while user_value >= 5:
        distribution[1] += 1
        user_value -= 5
    while user_value >= 1:
        distribution[0] += 1
        user_value -= 1

    return distribution # (1, 5, 10, 50, 100)


def change_to_main_menu(scale, game_screen, buttons, sliders, cards, chips):
    game_screen[0] = Screen.HOME
    
    buttons.clear()
    sliders.clear()
    cards.clear()
    chips.clear()

    new_game = Button(spritesheet_path, (51 * scale, 79 * scale), (scale, scale), 98, 22, "new game", callback=lambda: change_to_game(scale, game_screen, buttons, sliders, cards, chips))
    settings = Button(spritesheet_path, (51 * scale, 113 * scale), (scale, scale), 98, 22, "settings", callback=lambda: change_to_settings(scale, game_screen, buttons, sliders, cards, chips))
    
    buttons.append(new_game)
    buttons.append(settings)


def change_to_settings(scale, game_screen, buttons, sliders, cards, chips):
    game_screen[0] = Screen.SETTINGS
    
    buttons.clear()
    sliders.clear()
    cards.clear()
    chips.clear()
    
    difficulty = Button(spritesheet_path, (25 * scale, 83 * scale), (scale, scale), 67, 13, "difficulty")
    change_card = Button(spritesheet_path, (25 * scale, 109 * scale), (scale, scale), 67, 13, "change card")
    
    buttons.append(difficulty)
    buttons.append(change_card)


def change_to_game(scale, game_screen, buttons, sliders, cards, chips):
    game_screen[0] = Screen.GAME
    
    buttons.clear()
    sliders.clear()
    cards.clear()
    chips.clear()
    
    # Create buttons
    button_names = ["check", "call", "fold", "raise", "all in", "75%", "50%", "25%"]
    button_positions = [
    (127 * scale, 101 * scale),
    (127 * scale, 112 * scale),
    (127 * scale, 123 * scale),
    (127 * scale, 134 * scale),
    (155 * scale, 101 * scale),
    (155 * scale, 112 * scale),
    (155 * scale, 123 * scale),
    (155 * scale, 134 * scale),
    ]
    for i in range(len(button_names)):
        button = Button(spritesheet_path, button_positions[i], (scale, scale), 23, 9, button_names[i])
        buttons.append(button)
    
    # Create slider
    sliders.append(Slider(spritesheet_path, (183 * scale, 101 * scale), (scale, scale), 9, 42, 9, 5))

    # Player Cards
    card = Card(spritesheet_path, (80 * scale, 112 * scale), (scale, scale), "a", "spades", True)
    cards.append(card)
    card = Card(spritesheet_path, (103 * scale, 112 * scale), (scale, scale), "q", "hearts", True)
    cards.append(card)
    card = Card(spritesheet_path, (80 * scale, 7 * scale), (scale, scale), "10", "hearts", False)
    cards.append(card)
    card = Card(spritesheet_path, (103 * scale, 7 * scale), (scale, scale), "4", "clubs", False)
    cards.append(card)
    
    # Community Cards
    card = Card(spritesheet_path, (51 * scale, 59 * scale), (scale, scale), "2", "hearts", True)
    cards.append(card)
    card = Card(spritesheet_path, (71 * scale, 59 * scale), (scale, scale), "k", "clubs", True)
    cards.append(card)
    card = Card(spritesheet_path, (91 * scale, 59 * scale), (scale, scale), "10", "hearts", True)
    cards.append(card)
    card = Card(spritesheet_path, (111 * scale, 59 * scale), (scale, scale), "4", "spades", True)
    cards.append(card)
    card = Card(spritesheet_path, (131 * scale, 59 * scale), (scale, scale), "j", "hearts", True)
    cards.append(card)
    
    # Player chips
    player_value = 500
    distribution = get_proper_chip_distribution(player_value)
    
    colors = ["white", "red", "blue", "green", "black"]
    x = -13
    for i in range(0, 5):
        x += 13
        y = 2
        for _ in range(0, distribution[i]):
            y -= 2
            chip = Chip(spritesheet_path, ((9 + x) * scale, (132 + y) * scale), (scale, scale), colors[i])
            chips.append(chip)

    # CPU chips
    cpu_value = 500
    distribution = get_proper_chip_distribution(cpu_value)
    
    x = -13
    for i in range(0, 5):
        x += 13
        y = 2
        for _ in range(0, distribution[i]):
            y -= 2
            chip = Chip(spritesheet_path, ((9 + x) * scale, (27 + y) * scale), (scale, scale), colors[i])
            chips.append(chip)
    

