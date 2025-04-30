"""Helper functions for the GUI"""

from enum import Enum
from gui.button import Button
from gui.slider import Slider
from gui.gui_card import GUI_Card, CardType, card_type
from gui.chip import Chip
from gui.numtext import NumText
from gui.spritetext import SpriteText, TEXT_COORDS
from game_engine.engine import Engine, Difficulty
from game_engine.constants import Action
import pygame

SPRITESHEET_PATH = "../assets/poker-spritesheet.png"

class Screen(Enum):
    """
    Represents the screen being displayed
    """
    HOME  = 0
    SETTINGS  = 1
    GAME = 2


difficulty = [Difficulty.EASY]
gui_state = {
        "screen": Screen.HOME,
        "buttons": [],
        "sliders": [],
        "cards": [],
        "chips": [],
        "numtexts": [],
        "spritetexts": [],
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


def change_to_main_menu(scale, engine):
    """
    Changes the GUI elements to the ones found in the main menu screen
    """
    gui_state["screen"] = Screen.HOME

    gui_state["buttons"].clear()
    gui_state["sliders"].clear()
    gui_state["cards"].clear()
    gui_state["chips"].clear()
    gui_state["numtexts"].clear()
    gui_state["spritetexts"].clear()

    new_game = Button(SPRITESHEET_PATH, (51 * scale, 79 * scale),
                      (scale, scale), 98, 22, "new game",
                      callback=lambda: change_to_game(scale, engine))

    settings = Button(SPRITESHEET_PATH, (51 * scale, 113 * scale),
                      (scale, scale), 98, 22, "settings",
                      callback=lambda: change_to_settings(scale, engine))

    gui_state["buttons"].append(new_game)
    gui_state["buttons"].append(settings)


def change_to_settings(scale, engine):
    """
    Changes the GUI elements to the ones found in the settings screen
    """
    gui_state["screen"] = Screen.SETTINGS

    gui_state["buttons"].clear()
    gui_state["sliders"].clear()
    gui_state["cards"].clear()
    gui_state["chips"].clear()
    gui_state["numtexts"].clear()
    gui_state["spritetexts"].clear()

    difficulty_button = Button(SPRITESHEET_PATH, (25 * scale, 83 * scale),
                        (scale, scale), 67, 13, "difficulty",
                               callback=lambda: toggle_difficulty(scale, difficulty, engine))
    change_card = Button(SPRITESHEET_PATH, (25 * scale, 109 * scale),
                         (scale, scale), 67, 13, "change card",
                         callback=lambda: toggle_card_type(scale, card_type, engine))

    back = Button(SPRITESHEET_PATH, (11 * scale, 12 * scale),
                        (scale, scale), 13, 13, "back",
                        callback=lambda: change_to_main_menu(scale, engine))

    card = GUI_Card(SPRITESHEET_PATH, (96 * scale, 109 * scale), (scale, scale), "A", "S")
    gui_state["cards"].append(card)

    diff_string = "easy"
    match difficulty[0]:
        case Difficulty.MEDIUM:
            diff_string = "medium"
        case Difficulty.HARD:
            diff_string = "hard"
    difficulty_display = Button(SPRITESHEET_PATH, (96 * scale, 83 * scale),
                                (scale, scale), 41, 13, diff_string)
    gui_state["buttons"].append(difficulty_display)

    gui_state["buttons"].append(difficulty_button)
    gui_state["buttons"].append(change_card)
    gui_state["buttons"].append(back)


def change_to_game(scale, engine):
    """
    Changes the GUI elements to the ones found in the game screen
    """
    engine.start_next_round() # Start game

    gui_state["screen"] = Screen.GAME

    gui_state["buttons"].clear()
    gui_state["sliders"].clear()
    gui_state["cards"].clear()
    gui_state["chips"].clear()
    gui_state["numtexts"].clear()
    gui_state["spritetexts"].clear()

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
                        callback=lambda: confirm_bid(scale, engine))

        elif name in percentage_map:
            pct = percentage_map[name]
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name,
                        callback=(lambda pct_val: 
                                  lambda: bet_percentage(scale, pct_val, engine))(pct_val=pct))

        elif name == "fold":
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name,
                        callback=lambda: send_action(Action.FOLD, engine))

        elif name == "call":
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name,
                        callback=lambda: send_action(Action.CALL, engine))

        elif name == "check":
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name,
                        callback=lambda: send_action(Action.CHECK, engine))

        else:
            button = Button(SPRITESHEET_PATH, pos, (scale, scale), 23, 9, name)

        gui_state["buttons"].append(button)
    
    #for i in range(len(button_names)):
        #button = Button(SPRITESHEET_PATH, button_positions[i],
                        #(scale, scale), 23, 9, button_names[i])
        #gui_state["buttons"].append(button)

    # Back button
    back = Button(SPRITESHEET_PATH, (1 * scale, 1 * scale),
                        (scale, scale), 13, 13, "back",
                        callback=lambda: change_to_main_menu(scale, engine))
    gui_state["buttons"].append(back)

    # Create slider
    gui_state["sliders"].append(Slider(SPRITESHEET_PATH, (183 * scale, 101 * scale),
                          (scale, scale), 9, 42, 9, 5))

    # Num texts
    bid_num = NumText(SPRITESHEET_PATH, (105, 103), (scale, scale), 0, label="bid_amount")
    gui_state["numtexts"].append(bid_num)
    cpu_val = NumText(SPRITESHEET_PATH, (184, 24), (scale, scale), 0, label="cpu_balance")
    gui_state["numtexts"].append(cpu_val)
    ply_val = NumText(SPRITESHEET_PATH, (184, 32), (scale, scale), 0, label="player_balance")
    gui_state["numtexts"].append(ply_val)
    pot_val = NumText(SPRITESHEET_PATH, (184, 40), (scale, scale), 0, label="pot")
    gui_state["numtexts"].append(pot_val)


def update_game(scale, engine):
    """
    Handles the updating of the game. Everything related to engine/gui
    compatibility will be in this function.
    """
    gui_state["cards"].clear()
    gui_state["chips"].clear()
    gui_state["spritetexts"].clear()

    # Engine updating
    state = engine.current_state_of_game()

    # Update spritetexts
    action = get_last_cpu_action(state["action_histories"])
    cpu_action = SpriteText(action, (162 * scale, 17 * scale), scale)
    gui_state["spritetexts"].append(cpu_action)

    # Update cpu and player cards
    ply_cards = state["players"][0]["hole_cards"]
    cpu_cards = state["players"][1]["hole_cards"]

    card = GUI_Card(SPRITESHEET_PATH, (80 * scale, 112 * scale),
                    (scale, scale), ply_cards[0][:-1], ply_cards[0][-1], True)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (103 * scale, 112 * scale),
                    (scale, scale), ply_cards[1][:-1], ply_cards[1][-1], True)
    gui_state["cards"].append(card)
    
    show_cpu = state["round_over"] or state["showdown"]

    card = GUI_Card(SPRITESHEET_PATH, (80 * scale, 7 * scale), (scale, scale),
                    cpu_cards[0][:-1], cpu_cards[0][-1], show_cpu)
    gui_state["cards"].append(card)
    card = GUI_Card(SPRITESHEET_PATH, (103 * scale, 7 * scale), (scale, scale),
                    cpu_cards[1][:-1], cpu_cards[1][-1], show_cpu)
    gui_state["cards"].append(card)

    # Update community cards
    community_cards = state["community_cards"]
    community_card_positions = ((51 * scale, 59 * scale),
                                (71 * scale, 59 * scale),
                                (91 * scale, 59 * scale),
                                (111 * scale, 59 * scale),
                                (131 * scale, 59 * scale))
    
    # Update player chips
    ply_value = state["players"][0]["stack"]
    gui_state["ply_distribution"] = get_proper_chip_distribution(ply_value)

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
    
    # Update cpu chips
    cpu_value = state["players"][1]["stack"]
    gui_state["cpu_distribution"] = get_proper_chip_distribution(cpu_value)

    x = -13
    for i in range(0, 5):
        x += 13
        y = 2
        for _ in range(0, gui_state["cpu_distribution"][i]):
            y -= 2
            chip = Chip(SPRITESHEET_PATH, ((9 + x) * scale, (27 + y) * scale),
                        (scale, scale), colors[i])
            chip.owner = "cpu"
            gui_state["chips"].append(chip)


    for i in range(len(community_cards)):
        card = GUI_Card(SPRITESHEET_PATH, community_card_positions[i],
                        (scale, scale), community_cards[i][:-1], community_cards[i][-1], True)
        gui_state["cards"].append(card)
        
    # Update pot chips
    pot_value = gui_state["pot_stack"]
    gui_state["pot_distribution"] = get_proper_chip_distribution(pot_value)

    colors = ["black", "green", "blue", "red", "white"]
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
        for _ in range(gui_state["pot_distribution"][len(gui_state["pot_distribution"]) - i - 1]):
            chip = Chip(SPRITESHEET_PATH,
                        ((x_base) * scale, (y_base - y_offset) * scale),
                        (scale, scale), color)
            chip.owner = "pot"
            gui_state["chips"].append(chip)
            y_offset += 2  # Stack upward


    # Update numtexts
    gui_state["numtexts"][1].set_number(gui_state["cpu_stack"]) # Cpu balance
    gui_state["numtexts"][2].set_number(gui_state["ply_stack"]) # Player balance
    gui_state["numtexts"][3].set_number(gui_state["pot_stack"]) # Pot

    # Update to next phase of round depending on state
    if state["round_over"]:
        engine.start_next_round()
        update_gui_state(engine)

    elif state["betting_over"]:
        engine.start_next_street()
        update_gui_state(engine)

    elif not state["players_turn"]:
        pygame.time.wait(1500)
        engine.cpu_action()
        update_gui_state(engine)

    elif state["game_over"]:
        change_to_main_menu(scale, engine)


def update_gui_state(engine):
    state = engine.current_state_of_game()
    print("state", state)
    gui_state["pot_stack"] = state["pot"]
    gui_state["ply_stack"] = state["players"][0]["stack"]
    gui_state["cpu_stack"] = state["players"][1]["stack"]


def update_slider_info():
    # SLIDER UPDATING
    slider = gui_state["sliders"][0]
    percent = slider.get_value()
    bid_amount = int(gui_state["ply_stack"] * percent)

    # Update the Bid $ display
    for num in gui_state["numtexts"]:
        if getattr(num, "label", "") == "bid_amount":
            num.set_number(bid_amount)


def bet_percentage(scale, percent, engine):
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
    state = engine.current_state_of_game()
    max_bet = state["players"][0]["max_bet"]

    if max_bet <= 0:
        return

    amount_to_bet = int(max_bet * percent)
    if amount_to_bet == 0 and max_bet > 0:
        amount_to_bet = 1  # minimum bet if there's money

    gui_state["previewed_bet"] = amount_to_bet
    gui_state["sliders"][0].set_thumb(max_bet, gui_state["previewed_bet"])

    # Update display
    """
    for num in gui_state["numtexts"]:
        if getattr(num, "label", "") == "bid_amount":
            num.set_number(gui_state["previewed_bet"])
    """


def confirm_bid(scale, engine):
    """
    Finalizes the player's previewed bet.

    Deducts the previewed bet from the player's stack, adds it to the pot,
    updates the visual chips, and refreshes number text displays.
    """
    slider = gui_state["sliders"][0]
    percent = slider.get_value()

    state = engine.current_state_of_game()
    max_bet = state["players"][0]["max_bet"]
    bet = int(max_bet * percent)

    if bet <= 0:
        return

    engine.player_action(Action.RAISE, raise_amount=bet)
    gui_state["previewed_bet"] = 0

    for num in gui_state["numtexts"]:
        if getattr(num, "label", "") == "player_balance":
            num.set_number(gui_state["ply_stack"])
        elif getattr(num, "label", "") == "pot":
            num.set_number(gui_state["pot_stack"])
        elif getattr(num, "label", "") == "bid_amount":
            num.set_number(0)

def send_action(action, engine):
    """
    Sends a fold, call, or check action to the engine.
    Params: action: action player or CPU makes
            engine: game engine object
    """
    try:
        engine.player_action(action)
    except ValueError as e:
        print(f"Ignored invalid action: {e}")


def slider_bet_callback(scale):
    """
    Called when the 'Bid $' button is clicked. Reads the current slider position
    and uses that percentage to place a bet.
    """
    if not gui_state["sliders"]:
        return
    percent = gui_state["sliders"][0].get_value()
    bet_percentage(scale, percent)


def toggle_card_type(scale, card_type, engine):
    enum_type = type(card_type[0])
    members = list(enum_type)
    index = members.index(card_type[0])
    next_index = (index + 1) % len(members)
    card_type[0] = members[next_index]

    change_to_settings(scale, engine)


def toggle_difficulty(scale, difficulty, engine):
    enum_type = type(difficulty[0])
    members = list(enum_type)
    index = members.index(difficulty[0])
    next_index = (index + 1) % len(members)
    difficulty[0] = members[next_index]

    change_to_settings(scale, engine)


def get_last_cpu_action(action_histories):
    cpu_name = "baselineCPU"
    rounds = ["river", "turn", "flop", "preflop"]

    for round_name in rounds:
        actions = action_histories.get(round_name, [])
        for action in reversed(actions):
            if action.get("name") == cpu_name:
                return action["action"]

    return "NA"  # No CPU action found

