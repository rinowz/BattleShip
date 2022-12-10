""" Настройки игры"""
import pygame

DEFAULT_STATE = "play"
WIDTH = 1280
HEIGHT = 750
FPS = 600

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

PLAYER_POSITION = [WIDTH//2, HEIGHT//2]
BACKGROUND_POSITION = [0, 0]

# граница, за которую не должны заходить спрайты ((x_min, x_max), (y_min, y_max))
BORDERS = ((-1000, 1000), (-1000, 1000))