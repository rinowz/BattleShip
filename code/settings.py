""" Настройки игры"""
import os
import pygame

DEFAULT_STATE = "main_menu"
WIDTH = 1280
HEIGHT = 750
FPS = 600

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ALMOST_WHITE = (1, 0, 0)

LANGUAGE = 'english'

FULLSCREEN = True

CONTROLS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "shoot": pygame.K_SPACE,
    "fullscreen": pygame.K_TAB,
    "nuclear_launch": pygame.K_b
}

PLAYER_IMAGE = os.path.join(os.getcwd(), '..', 'graphics', 'ships', 'ship2.0.png')
PLAYER_POSITION = [WIDTH//2, HEIGHT//2]
BACKGROUND_POSITION = [-WIDTH//2, -HEIGHT//2]
# Скорость снарядов, запускаемых игроком
BULLET_SPEED = 2000
# Кулдаун выстрелов игрока
PLAYER_COOLDOWN = 500
# Максимальная скорость игрока
PLAYER_MAX_SPEED = 1000
# модуль ускорения при попытке корабля изменить скорость в некотором направлении
PLAYER_ACCELERATION = 2000
# Урон, наносимый выстрелами игрока
PLAYER_DAMAGE = 10

# граница, за которую не должны заходить спрайты ((x_min, x_max), (y_min, y_max))
BORDERS = ((-4500, 4500), (-4500, 4500))

# UI
HEALTH_BAR_POS = (30, 20)
NUCLEAR_BAR_POS = (30, 50)
NUCLEAR_COUNT_POS = (30, 80)
HEALTH_BAR_WIDTH = 250
HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_COLOR = RED
BORDER_WIDTH = 2
BORDER_COLOR = (48, 50, 64)

TURRET_SIZE = 90
TURRET_OFFSET = (-18, 0)

TARGET_POS = (2500, 2500)
