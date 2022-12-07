import pygame

DEFAULT_STATE = "play"
WIDTH = 1280
HEIGHT = 750
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

LANGUAGE = 'english'

CONTROLS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d
}

PLAYER_POSITION = pygame.math.Vector2(WIDTH//2, HEIGHT//2)
