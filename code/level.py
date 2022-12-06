import pygame
from player import Player
from settings import *


class Level:
    """ Уровень - происходит процесс "игры" игры"""

    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()

        # создание игрока
        self.player = Player(
            (WIDTH//2, HEIGHT//2),
            [self.visible_sprites],
            pygame.transform.rotate(pygame.image.load("../graphics/playerShip1_orange.png").convert_alpha(), -90))

    def run(self):
        """ Обновляет и рисует игру"""

        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
