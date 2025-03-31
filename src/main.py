"""Main entry point for the Poker game"""

import sys
import pygame
from gui.util import change_to_main_menu, Screen

# Initialize Pygame
pygame.init()
SCALE = 4
game_screen = [Screen.HOME] # Using list because Enums are immutable on their own

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

# Global GUI element lists
buttons = []
sliders = []
cards = []
chips = []
numtexts = []
# Innitialize the players money and pot 
player_balance = [500]
pot_total = [0]
# Initialize GUI elements
change_to_main_menu(SCALE, game_screen, buttons, sliders, cards, chips, numtexts, player_balance, pot_total)


RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                change_to_main_menu(SCALE, game_screen, buttons, sliders, cards, chips, numtexts, player_balance, pot_total)

        # Pass events to buttons and other GUI elements
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

    # Make sure only one screen is drawn at a time
    screen.fill((0, 0, 0))  # Clear screen before drawing

    if game_screen[0] == Screen.HOME:
        screen.blit(main_menu_background, (0, 0))
    elif game_screen[0] == Screen.SETTINGS:
        screen.blit(settings_background, (0, 0))
    elif game_screen[0] == Screen.GAME:
        screen.blit(game_background, (0, 0))

    # Draw GUI elements
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

pygame.quit()
sys.exit()
