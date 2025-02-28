import pygame

class Slider:
    def __init__(self, spritesheet_path, position, scale, base_width, base_height, thumb_width, thumb_height):
        """
        Initialize the Slider.

        :param spritesheet_path: Path to the spritesheet image.
        :param position: Tuple (x, y) for the slider's position on the screen.
        :param scale: Tuple (scale_x, scale_y) to scale the slider.
        :param base_width: Width of the slider base in the spritesheet.
        :param base_height: Height of the slider base in the spritesheet.
        :param thumb_width: Width of the slider thumb in the spritesheet.
        :param thumb_height: Height of the slider thumb in the spritesheet.
        """
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.position = position
        self.scale = scale

        # Scaled dimensions
        self.scaled_base_width = base_width * scale[0]
        self.scaled_base_height = base_height * scale[1]
        self.scaled_thumb_width = thumb_width * scale[0]
        self.scaled_thumb_height = thumb_height * scale[1]

        # Slider base sprite
        self.base_sprite = self.get_sprite(0, 76, base_width, base_height)

        # Slider thumb sprite
        self.thumb_sprite = self.get_sprite(9, 76, thumb_width, thumb_height)

        # Thumb position (relative to the slider base)
        self.thumb_position = (position[0], position[1] + (self.scaled_base_height - self.scaled_thumb_height) // 2)

        # Thumb movement bounds (scaled)
        self.min_y = position[1]
        self.max_y = position[1] + self.scaled_base_height - self.scaled_thumb_height

        # Track if the thumb is being dragged
        self.dragging = False


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


    def handle_event(self, event):
        """
        Handle Pygame events (e.g., mouse clicks and dragging).

        :param event: The Pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            thumb_rect = pygame.Rect(self.thumb_position[0], self.thumb_position[1], self.scaled_thumb_width, self.scaled_thumb_height)
            if thumb_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_y = event.pos[1] - (self.scaled_thumb_height // 2)
            new_y = max(self.min_y, min(new_y, self.max_y))  # Clamp within bounds
            self.thumb_position = (self.thumb_position[0], new_y)


    def draw(self, screen):
        """
        Draw the slider on the screen.

        :param screen: The Pygame surface to draw the slider on.
        """
        screen.blit(self.base_sprite, self.position)
        screen.blit(self.thumb_sprite, self.thumb_position)

