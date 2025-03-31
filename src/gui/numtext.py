"""Class and methods for the NumText GUI element"""
import pygame


class NumText:
    """
    NumText GUI element. Used for when a number needs to be displayed
    in the GUI. Meant to be easy to set up and intuitive to use
    with minimal setup.
    """
    def __init__(self, spritesheet_path, position, scale, number, label=None):
        """
        Initialize the NumberText element.

        :param spritesheet_path: Path to the spritesheet image containing digits 1-9.
        :param position: Tuple (x, y) for the top-left position of the number on the screen.
        :param scale: Tuple (scale_x, scale_y) to scale each digit.
        :param number: The initial number to display.
        """
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.position = position
        self.scale = scale
        self.number = number

        self.digit_width = 5
        self.digit_height = 5

        self.digit_sprites = self.load_digit_sprites()
        self.number_sprites = self.create_number_sprites(number)

        self.label = label 


    def recolor_sprite_white(self, sprite):
        """
        Convert non-transparent pixels in the sprite to white.
        """
        white_sprite = sprite.copy()
        for x in range(sprite.get_width()):
            for y in range(sprite.get_height()):
                color = sprite.get_at((x, y))
                if color.a != 0:
                    white_sprite.set_at((x, y), pygame.Color(255, 255, 255, color.a))
        return white_sprite


    def load_digit_sprites(self):
        """
        Extract digit sprites (1–9) from the spritesheet.

        :return: Dictionary mapping digit strings to pygame.Surface objects.
        """
        digit_sprites = {}
        for i in range(10):  # Digits 1-9
            x = (i * self.digit_width) + 20
            y = 31
            sprite = pygame.Surface((self.digit_width, self.digit_height), pygame.SRCALPHA)
            sprite.blit(self.spritesheet, (0, 0), (x, y, self.digit_width, self.digit_height))

            # Recolor sprite to white
            white_sprite = self.recolor_sprite_white(sprite)

            # Scale it
            scaled = pygame.transform.scale(
                white_sprite,
                (self.digit_width * self.scale[0], self.digit_height * self.scale[1])
            )

            digit_sprites[str(i)] = scaled
        return digit_sprites


    def create_number_sprites(self, number):
        """
        Convert the number into a list of sprites.

        :param number: The integer number to display.
        :return: List of pygame.Surface objects.
        """
        return [self.digit_sprites[d] for d in str(number) if d in self.digit_sprites]


    def set_number(self, number):
        """
        Update the displayed number.

        :param number: The new number to display.
        """
        self.number = number
        self.number_sprites = self.create_number_sprites(number)


    def draw(self, screen):
        """
        Draw the number on the screen.

        :param screen: The Pygame surface to draw the number on.
        """
        x, y = self.position[0] * self.scale[0], self.position[1] * self.scale[1]
        for sprite in self.number_sprites:
            screen.blit(sprite, (x, y))
            x += sprite.get_width() - (1 * self.scale[0])


    def handle_event(self, event):
        """
        Handle Pygame events (placeholder).

        :param event: The Pygame event to handle.
        """
