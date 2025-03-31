import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

square_size = 60
color = (0, 100, 255)

current_pos = pygame.Vector2(100, 100)
target_pos = pygame.Vector2(100, 100)
lerp_factor = 0.06
moving = False

def move(end_pos):
    global current_pos, target_pos, lerp_factor, moving
    target_pos = pygame.Vector2(end_pos)
    moving = True

moving_back = False

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_1 = (100, 100)
            pos_2 = (400, 300)
            if moving_back:
                move(pos_1)
            else:
                move(pos_2)
            moving_back = not moving_back

    if moving:
        current_pos += (target_pos - current_pos) * lerp_factor

        if (target_pos - current_pos).length() < 0.5:
            current_pos = target_pos
            moving = False

    pygame.draw.rect(screen, color, (*current_pos, square_size/2, square_size))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()