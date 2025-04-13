"""Main entry point for the Poker game"""

import sys
import pygame
from gui.util import change_to_main_menu, Screen, CardType, Difficulty, gui_state, update_game, update_slider_info
from game_engine.engine import Engine 
from game_engine.cpu.baselineCPU import baselineCPU

# Connect Gui & Engine
# Gain acess to current state of game, player action, and cpu action from engine
engine = Engine(num_players=2, initial_stack=500, blind=10)
cpu = baselineCPU(500)
engine.set_cpu_player(cpu_player=cpu)
#engine.start_next_round()


# Initialize Pygame
pygame.init()
SCALE = 4

# Set up display
screen = pygame.display.set_mode((200 * SCALE, 150 * SCALE))
pygame.display.set_caption("Poker")

# Load backgrounds
main_menu_background = pygame.transform.scale(pygame.image.load(
    "../assets/poker-main-menu.png"), (200 * SCALE, 150 * SCALE))
settings_background = pygame.transform.scale(pygame.image.load(
    "../assets/poker-settings.png"), (200 * SCALE, 150 * SCALE))
game_background = pygame.transform.scale(pygame.image.load(
    "../assets/poker-board.png"), (200 * SCALE, 150 * SCALE))

# Initialize GUI elements
change_to_main_menu(SCALE, engine)

RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                change_to_main_menu(SCALE, engine)
                

        # Pass events to buttons and other GUI elements
        for button in list(gui_state["buttons"]):
            button.handle_event(event)
        for slider in gui_state["sliders"]:
            slider.handle_event(event)
        for card in list(gui_state["cards"]):
            card.handle_event(event)
        for chip in gui_state["chips"]:
            chip.handle_event(event)
        for numtext in gui_state["numtexts"]:
            numtext.handle_event(event)
    
    if(gui_state["screen"] == Screen.GAME):
        update_slider_info()
        update_game(SCALE, engine)

    # Make sure only one screen is drawn at a time
    screen.fill((0, 0, 0))  # Clear screen before drawing

    if gui_state["screen"] == Screen.HOME:
        screen.blit(main_menu_background, (0, 0))
    elif gui_state["screen"] == Screen.SETTINGS:
        screen.blit(settings_background, (0, 0))
    elif gui_state["screen"] == Screen.GAME:
        screen.blit(game_background, (0, 0))

    # Draw GUI elements
    for button in list(gui_state["buttons"]):
        button.draw(screen)
    for slider in gui_state["sliders"]:
        slider.draw(screen)
    for card in list(gui_state["cards"]):
        card.draw(screen)
    for chip in gui_state["chips"]:
        chip.draw(screen)
    for numtext in gui_state["numtexts"]:
        numtext.draw(screen)
    for spritetext in gui_state["spritetexts"]:
        spritetext.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
