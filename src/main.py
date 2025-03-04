import pygame
from gui.Button import Button
from gui.Slider import Slider
from gui.Card import Card
from gui.Chip import Chip
import sys

def create_gui_elements(scale):
    spritesheet_path = "../assets/poker-spritesheet.png"

    # Create buttons
    button_names = ["check", "call", "fold", "raise", "all in", "75%", "50%", "25%"]
    button_positions = [
    (126 * scale, 101 * scale),
    (126 * scale, 112 * scale),
    (126 * scale, 123 * scale),
    (126 * scale, 134 * scale),
    (154 * scale, 101 * scale),
    (154 * scale, 112 * scale),
    (154 * scale, 123 * scale),
    (154 * scale, 134 * scale),
    ]
    buttons = []
    for i in range(len(button_names)):
        button = Button(spritesheet_path, button_positions[i], (scale, scale), 23, 9, button_names[i])
        buttons.append(button)
    
    # Create slider
    slider = Slider(spritesheet_path, (182 * scale, 101 * scale), (scale, scale), 9, 42, 9, 5)

    # Create cards
    cards = []
    card = Card(spritesheet_path, (79 * scale, 112 * scale), (scale, scale), "a", "spades", True)
    cards.append(card)
    card = Card(spritesheet_path, (102 * scale, 112 * scale), (scale, scale), "q", "hearts", True)
    cards.append(card)
    card = Card(spritesheet_path, (80 * scale, 7 * scale), (scale, scale), "10", "hearts", False)
    cards.append(card)
    card = Card(spritesheet_path, (103 * scale, 7 * scale), (scale, scale), "4", "clubs", False)
    cards.append(card)
    
    # Create chips
    chips = []
    # chip = Chip(spritesheet_path, (77 * scale, 69 * scale), (scale, scale), "black")
    # chips.append(chip)

    return (buttons, slider, cards, chips)

# Initialize Pygame
pygame.init()
scale = 4

# Set up display
screen = pygame.display.set_mode((200 * scale, 150 * scale))
pygame.display.set_caption("Scaled Poker Board")

image = pygame.image.load("../assets/poker-board.png")
scaled_image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

spritesheet = pygame.image.load("../assets/poker-spritesheet.png")
(buttons, slider, cards, chips) = create_gui_elements(scale)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)
        slider.handle_event(event)
        for card in cards:
            card.handle_event(event)
        for chip in chips:
            chip.handle_event(event)

    screen.fill((0, 0, 0))

    # Draw the scaled background on the screen
    screen.blit(scaled_image, (0, 0))

    for button in buttons:
        button.draw(screen)
    slider.draw(screen)
    for card in cards:
        card.draw(screen)
    for chip in chips:
        chip.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
