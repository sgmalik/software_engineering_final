"""Class and methods for the Button GUI element"""
import pygame


class Button:
    """
    Button GUI element. Used for when a button is necessary somwhere
    in the GUI. Meant to be easy to set up and intuitive to use with minimal
    setup.
    """
    def __init__(self, spritesheet_path, position, scale,
                 sprite_width, sprite_height, button_type,
                 callback=None):
        """
        Initialize the Button.

        :param spritesheet_path: Path to the spritesheet image.
        :param position: Tuple (x, y) for the button's position on the screen.
        :param scale: Tuple (scale_x, scale_y) to scale the button.
        :param sprite_width: Width of a single sprite in the spritesheet.
        :param sprite_height: Height of a single sprite in the spritesheet.
        :param callback: Function to execute when the button is clicked.
                        FUNCTION MUST BE PASSED AS A LAMBDA FUNCTION
        """
        self.clickable = True
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.position = position
        self.scale = scale
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.callback = callback  # Store the callback function

        # Calculate the scaled dimensions
        self.scaled_width = int(sprite_width * scale[0])
        self.scaled_height = int(sprite_height * scale[1])

        # Define the two sprites (unpressed and pressed)
        self.set_sprites(button_type)

        # Button action
        self.action = button_type

        # Current sprite (default to unpressed)
        self.current_sprite = self.unpressed_sprite

        # Rect for collision detection
        self.rect = pygame.Rect(position[0], position[1], self.scaled_width,
                                self.scaled_height)


    def set_sprites(self, button_type):
        """
        Based on the button_type, set the pressed and unpressed sprites
        for the button

        :param button_type: String of the button type the button should be
        """
        match button_type:
            case "check":
                self.unpressed_sprite = self.get_sprite(0, 58)
                self.pressed_sprite = self.get_sprite(92, 58)
            case "call":
                self.unpressed_sprite = self.get_sprite(23, 58)
                self.pressed_sprite = self.get_sprite(115, 58)
            case "fold":
                self.unpressed_sprite = self.get_sprite(46, 58)
                self.pressed_sprite = self.get_sprite(138, 58)
            case "raise":
                self.unpressed_sprite = self.get_sprite(69, 58)
                self.pressed_sprite = self.get_sprite(161, 58)
            case "25%":
                self.unpressed_sprite = self.get_sprite(0, 67)
                self.pressed_sprite = self.get_sprite(92, 67)
            case "50%":
                self.unpressed_sprite = self.get_sprite(23, 67)
                self.pressed_sprite = self.get_sprite(115, 67)
            case "75%":
                self.unpressed_sprite = self.get_sprite(46, 67)
                self.pressed_sprite = self.get_sprite(138, 67)
            case "all in":
                self.unpressed_sprite = self.get_sprite(69, 67)
                self.pressed_sprite = self.get_sprite(161, 67)
            case "new game":
                self.unpressed_sprite = self.get_sprite(0, 118)
                self.pressed_sprite = self.get_sprite(98, 118)
            case "settings":
                self.unpressed_sprite = self.get_sprite(0, 140)
                self.pressed_sprite = self.get_sprite(98, 140)
            case "difficulty":
                self.unpressed_sprite = self.get_sprite(0, 162)
                self.pressed_sprite = self.get_sprite(67, 162)
            case "change card":
                self.unpressed_sprite = self.get_sprite(0, 175)
                self.pressed_sprite = self.get_sprite(67, 175)
            case "easy":
                self.unpressed_sprite = self.get_sprite(0, 188)
                self.pressed_sprite = self.get_sprite(0, 188)
            case "medium":
                self.unpressed_sprite = self.get_sprite(41, 188)
                self.pressed_sprite = self.get_sprite(41, 188)
            case "hard":
                self.unpressed_sprite = self.get_sprite(82, 188)
                self.pressed_sprite = self.get_sprite(82, 188)
            case "back":
                self.unpressed_sprite = self.get_sprite(134, 162)
                self.pressed_sprite = self.get_sprite(147, 162)


    def get_sprite(self, x, y):
        """
        Extract a sprite from the spritesheet at the given coordinates.

        :param x: X coordinate in the spritesheet.
        :param y: Y coordinate in the spritesheet.
        :return: A scaled pygame.Surface representing the sprite.
        """
        sprite = pygame.Surface((self.sprite_width, self.sprite_height),
                                pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, self.sprite_width,
                                               self.sprite_height))
        return pygame.transform.scale(sprite, (self.scaled_width,
                                               self.scaled_height))


    def handle_event(self, event):
        """
        Handle Pygame events (e.g., mouse clicks).

        :param event: The Pygame event to handle.
        """
        if not self.clickable:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # IF BUTTON IS CLICKED, DO WHATEVER WE NEED TO DO HERE
                self.current_sprite = self.pressed_sprite
                print("CLICKED")
                if self.callback:
                    self.callback() # Call provided function when clicked
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.current_sprite = self.unpressed_sprite


    def draw(self, screen):
        """
        Draw the button on the screen.

        :param screen: The Pygame surface to draw the button on.
        """
        screen.blit(self.current_sprite, self.position)
