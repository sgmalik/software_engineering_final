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


gui_state = {
        "screen": Screen.HOME,
        "buttons": [],
        "sliders": [],
        "cards": [],
        "chips": [],
        "numtexts": [],
        "cpu_turn": [],
        "ply_stack": 500,
        "cpu_stack": 500,
        "pot_stack": 0,
        "ply_distribution": [], # Being updated
        "cpu_distribution": [], # Being updated
        "pot_distribution": [], # NOT being updated currently
        "previewed_bet": 0
        }


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


def change_to_main_menu(scale):
    """
    Changes the GUI elements to the ones found in the main menu screen
    """
    gui_state["screen"] = Screen.HOME

    gui_state["buttons"].clear()
    gui_state["sliders"].clear()
    gui_state["cards"].clear()
    gui_state["chips"].clear()
    gui_state["numtexts"].clear()

    new_game = Button(SPRITESHEET_PATH, (51 * scale, 79 * scale),
                      (scale, scale), 98, 22, "new game",
                      callback=lambda: change_to_game(scale))

    settings = Button(SPRITESHEET_PATH, (51 * scale, 113 * scale),
                      (scale, scale), 98, 22, "settings",
                      callback=lambda: change_to_settings(scale))

    gui_state["buttons"].append(new_game)
    gui_state["buttons"].append(settings)


def change_to_settings(scale):
    """
    Changes the GUI elements to the ones found in the settings screen
    """
    gui_state["screen"] = Screen.SETTINGS

    gui_state["buttons"].clear()
    gui_state["sliders"].clear()
    gui_state["cards"].clear()
    gui_state["chips"].clear()
    gui_state["numtexts"].clear()

    difficulty = Button(SPRITESHEET_PATH, (25 * scale, 83 * scale),
                        (scale, scale), 67, 13, "difficulty")
    change_card = Button(SPRITESHEET_PATH, (25 * scale, 109 * scale),
                         (scale, scale), 67, 13, "change card")

    gui_state["buttons"].append(difficulty)
    gui_state["buttons"].append(change_card)


def change_to_game(scale):
    """
    Changes the GUI elements to the ones found in the game screen
    """
    gui_state["screen"] = Screen.GAME

    gui_state["buttons"].clear()
    gui_state["sliders"].clear()
    gui_state["cards"].clear()
    gui_state["chips"].clear()
    gui_state["numtexts"].clear()

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

        if name == "raise":
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name,
                            callback=lambda: confirm_bid(scale))

        elif name in percentage_map:
            pct = percentage_map[name]
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name,
                            callback=(lambda pct_val:
                                    lambda: bet_percentage(scale, pct_val))(pct))
        else:
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name)

        gui_state["buttons"].append(button)
    
    for i in range(len(button_names)):
        button = Button(SPRITESHEET_PATH, button_positions[i],
                        (scale, scale), 23, 9, button_names[i])
        gui_state["buttons"].append(button)

    # Create slider
    gui_state["sliders"].append(Slider(SPRITESHEET_PATH, (183 * scale, 101 * scale),
                          (scale, scale), 9, 42, 9, 5))

    # Player Cards
    card = GUI_Card(SPRITESHEET_PATH, (80 * scale, 112 * scale), (scale, scale), "a", "spades", True)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (103 * scale, 112 * scale), (scale, scale), "q", "hearts", True)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (80 * scale, 7 * scale), (scale, scale), "10", "hearts", False)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (103 * scale, 7 * scale), (scale, scale), "4", "clubs", False)
    gui_state["cards"].append(card)

    # Community Cards
    card = GUI_Card(SPRITESHEET_PATH, (51 * scale, 59 * scale), (scale, scale), "2", "hearts", True)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (71 * scale, 59 * scale), (scale, scale), "k", "clubs", True)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (91 * scale, 59 * scale), (scale, scale), "10", "hearts", True)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (111 * scale, 59 * scale), (scale, scale), "4", "spades", True)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (131 * scale, 59 * scale), (scale, scale), "j", "hearts", True)
    gui_state["cards"].append(card)

    # Player chips, based on player_balance from main 
    gui_state["ply_distribution"] = get_proper_chip_distribution(gui_state["ply_stack"])

    colors = ["white", "red", "blue", "green", "black"]
    x = -13
    for i in range(0, 5):
        x += 13
        y = 2
        for _ in range(0, gui_state["ply_distribution"][i]):
            y -= 2
            chip = Chip(SPRITESHEET_PATH, ((9 + x) * scale, (132 + y) * scale),
                        (scale, scale), colors[i])
            chip.owner = "player"
            gui_state["chips"].append(chip)

    # CPU chips
    cpu_value = 500
    gui_state["cpu_distribution"] = get_proper_chip_distribution(cpu_value)

    x = -13
    for i in range(0, 5):
        x += 13
        y = 2
        for _ in range(0, gui_state["cpu_distribution"][i]):
            y -= 2
            chip = Chip(SPRITESHEET_PATH, ((9 + x) * scale, (27 + y) * scale),
                        (scale, scale), colors[i])
            gui_state["chips"].append(chip)

    # Num texts
    bid_num = NumText(SPRITESHEET_PATH, (105, 103), (scale, scale), 0, label="bid_amount")
    gui_state["numtexts"].append(bid_num)
    cpu_val = NumText(SPRITESHEET_PATH, (184, 24), (scale, scale), cpu_value, label="cpu_balance")
    gui_state["numtexts"].append(cpu_val)
    ply_val = NumText(SPRITESHEET_PATH, (184, 32), (scale, scale), gui_state["ply_stack"], label="player_balance")
    gui_state["numtexts"].append(ply_val)
    pot_val = NumText(SPRITESHEET_PATH, (184, 40), (scale, scale), 0, label="pot")
    gui_state["numtexts"].append(pot_val)


def update_game():
    slider = gui_state["sliders"][0]
    percent = slider.get_value()
    bid_amount = int(gui_state["ply_stack"] * percent)

    # Update the Bid $ display
    for num in gui_state["numtexts"]:
        if getattr(num, "label", "") == "bid_amount":
            num.set_number(bid_amount)


def update_player_chips(scale):
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
    distribution = get_proper_chip_distribution(gui_state["ply_stack"])

    # Remove previous player chips
    gui_state["chips"][:] = [chip for chip in gui_state["chips"] if getattr(chip, "owner", "") != "player"]

    x = -13
    for i in range(5):
        x += 13
        y = 2
        for _ in range(distribution[i]):
            y -= 2
            chip = Chip(SPRITESHEET_PATH, ((9 + x) * scale, (132 + y) * scale),
                        (scale, scale), colors[i])
            chip.owner = "player"
            gui_state["chips"].append(chip)


def bet_percentage(scale, percent):
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
    if gui_state["ply_stack"] <= 0:
        return

    amount_to_bet = int(gui_state["ply_stack"] * percent)
    if amount_to_bet == 0 and gui_state["ply_stack"] > 0:
        amount_to_bet = 1  # minimum bet if there's money

    gui_state["previewed_bet"] = amount_to_bet
    gui_state["sliders"][0].set_thumb(gui_state["ply_stack"], gui_state["previewed_bet"])

    # Update display
    """
    for num in gui_state["numtexts"]:
        if getattr(num, "label", "") == "bid_amount":
            num.set_number(gui_state["previewed_bet"])
    """


def add_chips_to_pot(scale, amount):
    """
    Visually adds chip sprites to the pot area based on the amount bet.

    Chips are placed in fixed x/y stacks by denomination to match the board layout.

    Parameters:
        chips (list): The main chip list used in the game.
        scale (int): The screen scaling factor.
        amount (int): The total dollar amount being added to the pot.
    """
    colors = ["black", "green", "blue", "red", "white"]
    
    distribution = get_proper_chip_distribution(amount)

    # Pot stack positions for each chip type
    chip_stack_positions = {
        "white": (167, 79),
        "red": (183, 76),
        "blue": (173, 69),
        "green": (163, 62),
        "black": (179, 59)
    }

    for i, color in enumerate(colors):
        x_base, y_base = chip_stack_positions[color]
        y_offset = 0
        for _ in range(distribution[len(distribution) - i - 1]):
            chip = Chip(SPRITESHEET_PATH,
                        ((x_base) * scale, (y_base - y_offset) * scale),
                        (scale, scale), color)
            chip.owner = "pot"
            gui_state["chips"].append(chip)
            y_offset += 2  # Stack upward


def confirm_bid(scale):
    """
    Finalizes the player's previewed bet.

    Deducts the previewed bet from the player's stack, adds it to the pot,
    updates the visual chips, and refreshes number text displays.
    """
    slider = gui_state["sliders"][0]
    percent = slider.get_value()
    bet = int(gui_state["ply_stack"] * percent)

    # Safety checks
    if bet <= 0 or bet > gui_state["ply_stack"]:
        return

    # Transfer bet to pot
    gui_state["ply_stack"] -= bet
    gui_state["pot_stack"] += bet
    gui_state["previewed_bet"] = 0  # Reset previewed bet

    # Update numtexts
    for num in gui_state["numtexts"]:
        if getattr(num, "label", "") == "player_balance":
            num.set_number(gui_state["ply_stack"])
        elif getattr(num, "label", "") == "pot":
            num.set_number(gui_state["pot_stack"])
        elif getattr(num, "label", "") == "bid_amount":
            num.set_number(0)

    # Rebuild chips
    update_player_chips(scale)
    add_chips_to_pot(scale, bet)


def slider_bet_callback(scale):
    """
    Called when the 'Bid $' button is clicked. Reads the current slider position
    and uses that percentage to place a bet.
    """
    if not gui_state["sliders"]:
        return
    percent = gui_state["sliders"][0].get_value()
    bet_percentage(scale, percent)
