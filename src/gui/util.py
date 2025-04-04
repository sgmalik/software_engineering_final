"""Helper functions for the GUI"""

from enum import Enum
from gui.button import Button
from gui.slider import Slider
from gui.gui_card import GUI_Card
from gui.chip import Chip
from gui.numtext import NumText

SPRITESHEET_PATH = "../assets/poker-spritesheet.png"


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



def change_to_main_menu(scale, game_screen, buttons, sliders, cards, chips, numtexts, player_balance, pot_total):

    """
    Changes the GUI elements to the ones found in the main menu screen
    """
    game_screen[0] = Screen.HOME

    buttons.clear()
    sliders.clear()
    cards.clear()
    chips.clear()
    numtexts.clear()

    new_game = Button(SPRITESHEET_PATH, (51 * scale, 79 * scale),
                      (scale, scale), 98, 22, "new game",
                      callback=lambda: change_to_game(scale, game_screen,
                                                      buttons, sliders, cards,

                                                      chips, numtexts, 
                                                      player_balance, pot_total))

    settings = Button(SPRITESHEET_PATH, (51 * scale, 113 * scale),
                      (scale, scale), 98, 22, "settings",
                      callback=lambda: change_to_settings(scale, game_screen,
                                                          buttons, sliders, cards,
                                                          chips, numtexts))

    buttons.append(new_game)
    buttons.append(settings)


def change_to_settings(scale, game_screen, buttons, sliders, cards, chips, numtexts):
    """
    Changes the GUI elements to the ones found in the settings screen
    """
    game_screen[0] = Screen.SETTINGS

    buttons.clear()
    sliders.clear()
    cards.clear()
    chips.clear()
    numtexts.clear()

    difficulty = Button(SPRITESHEET_PATH, (25 * scale, 83 * scale),
                        (scale, scale), 67, 13, "difficulty")
    change_card = Button(SPRITESHEET_PATH, (25 * scale, 109 * scale),
                         (scale, scale), 67, 13, "change card")

    buttons.append(difficulty)
    buttons.append(change_card)


def change_to_game(scale, game_screen, buttons, sliders, cards, chips, numtexts, player_balance, pot_total):
    """
    Changes the GUI elements to the ones found in the game screen
    """
    game_screen[0] = Screen.GAME

    buttons.clear()
    sliders.clear()
    cards.clear()
    chips.clear()
    numtexts.clear()

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

    # Make betting percentage buttons work 
    for i in range(len(button_names)):
        name = button_names[i]
        pos = button_positions[i]
    
    percentage_map = {
    "25%": 0.25,
    "50%": 0.50,
    "75%": 0.75,
    "all in": 1.0
}
    # Create betting buttons action 
    for i in range(len(button_names)):
        name = button_names[i]
        pos = button_positions[i]

        if name in percentage_map:
            pct = percentage_map[name]
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name,
                            callback=(lambda pct_val:
                                    lambda: bet_percentage(pct_val, player_balance, pot_total,
                                                            chips, scale, numtexts))(pct))
        else:
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name)

        buttons.append(button)


    

    for i in range(len(button_names)):
        button = Button(SPRITESHEET_PATH, button_positions[i],
                        (scale, scale), 23, 9, button_names[i])
        buttons.append(button)

    # Create slider
    sliders.append(Slider(SPRITESHEET_PATH, (183 * scale, 101 * scale),
                          (scale, scale), 9, 42, 9, 5))

    # Player Cards
    card = GUI_Card(SPRITESHEET_PATH, (80 * scale, 112 * scale), (scale, scale), "a", "spades", True)
    cards.append(card)
    card = GUI_Card(SPRITESHEET_PATH, (103 * scale, 112 * scale), (scale, scale), "q", "hearts", True)
    cards.append(card)
    card = GUI_Card(SPRITESHEET_PATH, (80 * scale, 7 * scale), (scale, scale), "10", "hearts", False)
    cards.append(card)
    card = GUI_Card(SPRITESHEET_PATH, (103 * scale, 7 * scale), (scale, scale), "4", "clubs", False)
    cards.append(card)

    # Community Cards
    card = GUI_Card(SPRITESHEET_PATH, (51 * scale, 59 * scale), (scale, scale), "2", "hearts", True)
    cards.append(card)
    card = GUI_Card(SPRITESHEET_PATH, (71 * scale, 59 * scale), (scale, scale), "k", "clubs", True)
    cards.append(card)
    card = GUI_Card(SPRITESHEET_PATH, (91 * scale, 59 * scale), (scale, scale), "10", "hearts", True)
    cards.append(card)
    card = GUI_Card(SPRITESHEET_PATH, (111 * scale, 59 * scale), (scale, scale), "4", "spades", True)
    cards.append(card)
    card = GUI_Card(SPRITESHEET_PATH, (131 * scale, 59 * scale), (scale, scale), "j", "hearts", True)
    cards.append(card)

    # Player chips, based on player_balance from main 
    distribution = get_proper_chip_distribution(player_balance[0])

    colors = ["white", "red", "blue", "green", "black"]
    x = -13
    for i in range(0, 5):
        x += 13
        y = 2
        for _ in range(0, distribution[i]):
            y -= 2
            chip = Chip(SPRITESHEET_PATH, ((9 + x) * scale, (132 + y) * scale),
                        (scale, scale), colors[i])
            chip.owner = "player"
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
            chip = Chip(SPRITESHEET_PATH, ((9 + x) * scale, (27 + y) * scale),
                        (scale, scale), colors[i])
            chips.append(chip)

    # Num texts
    bid_num = NumText(SPRITESHEET_PATH, (105, 103), (scale, scale), 0, label="bid_amount")
    numtexts.append(bid_num)
    cpu_val = NumText(SPRITESHEET_PATH, (184, 24), (scale, scale), cpu_value, label="cpu_balance")
    numtexts.append(cpu_val)
    ply_val = NumText(SPRITESHEET_PATH, (184, 32), (scale, scale), player_balance[0], label="player_balance")
    numtexts.append(ply_val)
    pot_val = NumText(SPRITESHEET_PATH, (184, 40), (scale, scale), 0, label="pot")
    numtexts.append(pot_val)

    
    
    


def update_player_chips(chips, scale, player_balance):
    """
    Rebuilds the player's chip stack to visually reflect their current balance.

    Removes all chips marked as "player", then regenerates a new distribution
    based on the remaining balance using the standard chip values.

    Parameters:
        chips (list): The master chip list used in the game.
        scale (int): The UI scaling factor for screen resolution.
        player_balance (list[int]): A one-item list tracking the player's balance.
    """
    colors = ["white", "red", "blue", "green", "black"]
    distribution = get_proper_chip_distribution(player_balance[0])

    # Remove previous player chips
    chips[:] = [chip for chip in chips if getattr(chip, "owner", "") != "player"]

    x = -13
    for i in range(5):
        x += 13
        y = 2
        for _ in range(distribution[i]):
            y -= 2
            chip = Chip(SPRITESHEET_PATH, ((9 + x) * scale, (132 + y) * scale),
                        (scale, scale), colors[i])
            chip.owner = "player"
            chips.append(chip)


def bet_percentage(percent, player_balance, pot_total, chips, scale, numtexts):
    """
    Handles betting logic triggered by the 25%, 50%, 75%, and All In buttons.

    Deducts a percentage of the player's balance, updates both the player's 
    displayed chips and the visual pot, and updates number displays.

    Parameters:
        percent (float): Fraction of the player's balance to bet (e.g., 0.25).
        player_balance (list[int]): Player’s current balance.
        pot_total (list[int]): Total value in the pot.
        chips (list): The master list of chip sprites on screen.
        scale (int): The global screen scaling factor.
        numtexts (list): List of all NumText elements to update.
    """
    if player_balance[0] <= 0:
        return

    amount_to_bet = int(player_balance[0] * percent)
    if amount_to_bet == 0 and player_balance[0] > 0:
        amount_to_bet = 1  # minimum bet if there's money

    player_balance[0] -= amount_to_bet
    pot_total[0] += amount_to_bet

    # Update display
    for num in numtexts:
        if getattr(num, "label", "") == "player_balance":
            num.set_number(player_balance[0])
        elif getattr(num, "label", "") == "pot":
            num.set_number(pot_total[0])

    # Update chips
    update_player_chips(chips, scale, player_balance)
    # Update physical pot 
    add_chips_to_pot(chips, scale, amount_to_bet)

def add_chips_to_pot(chips, scale, amount):
    """
    Visually adds chip sprites to the pot area based on the amount bet.

    Chips are placed in fixed x/y stacks by denomination to match the board layout.

    Parameters:
        chips (list): The main chip list used in the game.
        scale (int): The screen scaling factor.
        amount (int): The total dollar amount being added to the pot.
    """
    colors = ["white", "red", "blue", "green", "black"]
    distribution = get_proper_chip_distribution(amount)

    # Pot stack positions for each chip type
    chip_stack_positions = {
        "white": (167, 80),
        "red": (183, 76),
        "blue": (174, 68),
        "green": (162, 62),
        "black": (160, 56)
    }

    for i, color in enumerate(colors):
        x_base, y_base = chip_stack_positions[color]
        y_offset = 0
        for _ in range(distribution[i]):
            chip = Chip(SPRITESHEET_PATH,
                        ((x_base) * scale, (y_base - y_offset) * scale),
                        (scale, scale), color)
            chip.owner = "pot"
            chips.append(chip)
            y_offset += 2  # Stack upward

def slider_bet_callback(sliders, player_balance, pot_total, chips, scale, numtexts):
    """
    Called when the 'Bid $' button is clicked. Reads the current slider position
    and uses that percentage to place a bet.
    """
    if not sliders:
        return
    percent = sliders[0].get_value()
    bet_percentage(percent, player_balance, pot_total, chips, scale, numtexts)