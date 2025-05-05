# File: gui/spritetext.py
import pygame

SPRITESHEET_PATH = "../assets/poker-spritesheet.png"

TEXT_COORDS = {
    "sb": (82, 31, 25, 5),
    "bb": (107, 31, 25, 5),
    "check": (132, 31, 19, 5),
    "call": (151, 31, 15, 5),
    "fold": (166, 31, 15, 5),
    "raise": (181, 31, 19, 5),
    "NA": (199, 0, 1, 1)
}

class SpriteText:
    def __init__(self, text_type, position, scale):
        self.spritesheet = pygame.image.load(SPRITESHEET_PATH).convert_alpha()
        self.text_type = text_type
        self.position = position
        self.scale = scale
        self.image = self.load_image()

    def load_image(self):
        if self.text_type in TEXT_COORDS:
            x, y, w, h = TEXT_COORDS[self.text_type]
            sprite = pygame.Surface((w, h), pygame.SRCALPHA)
            sprite.blit(self.spritesheet, (0, 0), (x, y, w, h))
            return pygame.transform.scale(sprite, (w * self.scale, h * self.scale))
        else:
            # Use a small, bold font and white/yellow color, no background
            font = pygame.font.SysFont('Arial', 4 * self.scale, bold=True)
            color = (255, 255, 170)
            text_surface = font.render(self.text_type, True, color)
            return text_surface

    def draw(self, screen):
        screen.blit(self.image, self.position)
