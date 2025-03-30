import pygame


class Chip:
    def __init__(self, spritesheet_path, position, scale, color):
        """
        Initialize the Chip.

        :param spritesheet_path: Path to the spritesheet image.
        :param position: Tuple (x, y) for the chip's position on the screen.
        :param scale: Tuple (scale_x, scale_y) to scale the chip.
        :param color: The color of the chip (e.g., "red", "blue", "green").
        """
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.position = position
        self.scale = scale
        self.color = color

        # Dimensions of a single chip sprite (before scaling)
        self.chip_width = 11
        self.chip_height = 11

        # Load the chip sprite based on the color
        self.chip_sprite = self.get_chip_sprite()


    def get_chip_sprite(self):
        """
        Get the chip sprite based on the chip's color.

        :return: A pygame.Surface representing the chip sprite.
        """
        chip_positions = {
            "white": (0, 47),
            "red": (11, 47),
            "blue": (22, 47),
            "green": (33, 47),
            "black": (44, 47)
        }
        x, y = chip_positions.get(self.color, (0, 0))
        return self.get_sprite(x, y, self.chip_width, self.chip_height)


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


    def draw(self, screen):
        """
        Draw the chip on the screen.

        :param screen: The Pygame surface to draw the chip on.
        """
        screen.blit(self.chip_sprite, self.position)


    def handle_event(self, event):
        """
        Handle Pygame events (placeholder for now).

        :param event: The Pygame event to handle.
        """
        # ADD FUTURE EVENTS HERE IF WE WANT
        pass

