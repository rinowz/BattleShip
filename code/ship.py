import pygame


class Ship(pygame.sprite.Sprite):
    """ Корабль - объект игрока или противника"""

    def __init__(self, pos, groups, image=pygame.Surface((50, 50))):

        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # вектор скорости корабля с максимальным значением
        self.velocity = pygame.math.Vector2()
        self.max_speed = 15
        # модуль ускорения при попытке корабля изменить скорость в некотором направлении
        self.acceleration = 0.3
