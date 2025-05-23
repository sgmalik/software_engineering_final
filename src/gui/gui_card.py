"""Class and methods for the Card GUI element"""
import pygame
from enum import Enum


class CardType(Enum):
    """
    Represents the type of GUI card to use
    """
    RED = 0
    BLUE = 1
    GREEN = 2
    BLACK = 3


card_type = [CardType.RED]


class GUI_Card:
    """
    Card GUI element. Used for when a card needs to be displayed
    in the GUI. Meant to be easy to set up and intuitive to use
    with minimal setup.
    """
    def __init__(self, spritesheet_path, position, scale, rank, suite, revealed=False):
        """
        Initialize the Card.

        :param spritesheet_path: Path to the spritesheet image.
        :param position: Tuple (x, y) for the card's position on the screen.
        :param scale: Tuple (scale_x, scale_y) to scale the card.
        :param rank: The rank of the card (e.g., "Ace", "2", "King").
        :param suite: The suite of the card (e.g., "hearts", "diamonds").
        :param revealed: Boolean indicating whether the card is revealed.
        """
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.position = position
        self.scale = scale
        self.rank = rank
        self.suite = suite
        self.revealed = revealed

        self.card_width = 19
        self.card_height = 31

        self.set_card_color()

        # Load the open card sprite (base of the card when revealed)
        self.open_sprite = self.get_sprite(0, 0, self.card_width, self.card_height)

        # Load the suite sprite (e.g., hearts, diamonds)
        self.suite_sprite = self.get_suite_sprite()

        # Load the rank sprite (e.g., Ace, King)
        self.rank_sprite = self.get_rank_sprite()


    def set_card_color(self):
        match card_type[0]:
            case CardType.RED:
                self.back_sprite = self.get_sprite(19, 0, self.card_width, self.card_height)
            case CardType.BLUE:
                self.back_sprite = self.get_sprite(38, 0, self.card_width, self.card_height)
            case CardType.GREEN:
                self.back_sprite = self.get_sprite(57, 0, self.card_width, self.card_height)
            case CardType.BLACK:
                self.back_sprite = self.get_sprite(76, 0, self.card_width, self.card_height)


    def get_sprite(self, x, y, width, height):
        """
        Extract a sprite from the spritesheet at the given coordinates.

        :param x: X coordinate in the spritesheet.
        :param y: Y coordinate in the spritesheet.
        :param width: Width of the sprite.
        :param height: Height of the sprite.
        :return: A scaled pygame.Surface representing the sprite.
        """
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return pygame.transform.scale(sprite, (width * self.scale[0], height * self.scale[1]))


    def get_suite_sprite(self):
        """
        Get the suite sprite based on the card's suite.

        :return: A pygame.Surface representing the suite sprite.
        """
        suite_positions = {
            "D": (0, 36),
            "H": (11, 36),
            "C": (22, 36),
            "S": (33, 36),
        }
        x, y = suite_positions.get(self.suite, (0, 0))
        return self.get_sprite(x, y, 11, 11)


    def get_rank_sprite(self):
        """
        Get the rank sprite based on the card's rank.

        :return: A pygame.Surface representing the rank sprite.
        """
        rank_positions = {
            "A": (0, 31),
            "K": (5, 31),
            "Q": (10, 31),
            "J": (15, 31),
            "2": (30, 31),
            "3": (35, 31),
            "4": (40, 31),
            "5": (45, 31),
            "6": (50, 31),
            "7": (55, 31),
            "8": (60, 31),
            "9": (65, 31),
            "10": (70, 31)
        }
        x, y = rank_positions.get(self.rank, (0, 0))
        return self.get_sprite(x, y, 5, 5)


    def draw(self, screen):
        """
        Draw the card on the screen.

        :param screen: The Pygame surface to draw the card on.
        """
        if not self.revealed:
            # Draw the back of the card
            screen.blit(self.back_sprite, self.position)
        else:
            # Draw the open card sprite
            screen.blit(self.open_sprite, self.position)

            # Draw the suite sprite
            suite_x = self.position[0] + (self.card_width * self.scale[0] -
                                          self.suite_sprite.get_width()) // 2
            suite_y = self.position[1] + (self.card_height * self.scale[1] -
                                          self.suite_sprite.get_height()) // 2
            screen.blit(self.suite_sprite, (suite_x, suite_y))

            # Draw the top left rank sprite
            top_left_rank_x = self.position[0] + 3 * self.scale[0]
            top_left_rank_y = self.position[1] + 3 * self.scale[1]
            screen.blit(self.rank_sprite, (top_left_rank_x, top_left_rank_y))

            # Draw the bottom right rank sprite
            flipped_rank_sprite = pygame.transform.flip(self.rank_sprite, True, True)

            sprite_width = flipped_rank_sprite.get_width()
            sprite_height = flipped_rank_sprite.get_height()

            draw_x = self.position[0] + (16 * self.scale[0]) - sprite_width
            draw_y = self.position[1] + (28 * self.scale[1]) - sprite_height

            screen.blit(flipped_rank_sprite, (draw_x, draw_y))


    def handle_event(self, event):
        """
        Handle Pygame events (placeholder for now).

        :param event: The Pygame event to handle.
        """
        # ADD EVENT HANDLING IF WE WANT IT IN THE FUTURE
